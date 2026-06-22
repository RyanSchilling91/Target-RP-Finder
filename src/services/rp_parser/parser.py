"""Parse Target.RP fixed-width text files and extract flagged compounds."""
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import re

FLAGGED_REVIEW_CODES = {"Udel", "Udelete", "dubious"}

@dataclass
class FlaggedCompound:
    """A compound row from Target.RP with a flagged review code."""
    name: str
    review_code: str
    sample_id: Optional[str] = None

def parse_target_rp(file_path: str | Path) -> tuple[list[FlaggedCompound], list[str]]:
    """Parse a Target.RP file and extract flagged compounds.

    Returns:
        (flagged_compounds, unknown_tokens): List of FlaggedCompound objects and any
        non-standard review code tokens encountered.
    """
    file_path = Path(file_path)
    if not file_path.exists():
        return [], []

    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
    except (IOError, OSError):
        return [], []

    sample_id = _extract_sample_id(content)
    flagged = []
    unknown_tokens = set()

    lines = content.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]

        if "REVIEW CODE" in line and "Compounds" in line:
            i += 1
            if i < len(lines) and "===" in lines[i]:
                i += 1
                while i < len(lines):
                    data_line = lines[i]
                    if not data_line.strip() or "===" in data_line or "Page" in data_line:
                        break

                    compound = _parse_compound_row(data_line)
                    if compound:
                        if compound.review_code in FLAGGED_REVIEW_CODES:
                            compound.sample_id = sample_id
                            flagged.append(compound)
                        elif compound.review_code:
                            unknown_tokens.add(compound.review_code)

                    i += 1
                continue

        i += 1

    return flagged, sorted(unknown_tokens)

def _extract_sample_id(content: str) -> Optional[str]:
    """Extract the Lab Smp Id from the file header."""
    match = re.search(r"Lab Smp Id:\s+(\S+)", content)
    if match:
        return match.group(1)
    return None

def _parse_compound_row(line: str) -> Optional[FlaggedCompound]:
    """Parse a single compound data row using fixed-width column positions.

    Compound name: columns ~10-40 (after row number, before numeric data).
    Review code: far right, look for known codes in the last tokens.
    """
    if not line.strip():
        return None

    line_stripped = line.rstrip()
    if len(line_stripped) < 20:
        return None

    match = re.match(r"^\s*[*$]?\s*\d+\s+(.{0,30})", line_stripped)
    if not match:
        return None

    name = match.group(1).strip()
    if not name:
        return None

    review_code = ""
    tokens = line_stripped.split()

    for i in range(len(tokens) - 1, -1, -1):
        token = tokens[i]
        if token in FLAGGED_REVIEW_CODES:
            review_code = token
            break
        elif _is_known_code_or_anomaly(token):
            review_code = token
            break

    return FlaggedCompound(name=name, review_code=review_code)

def _is_known_code_or_anomaly(token: str) -> bool:
    """Check if token is a flagged code or log-worthy anomaly."""
    if token in FLAGGED_REVIEW_CODES:
        return True
    if token in {"(M)", "(Q)", "(QM)"}:
        return False
    if _is_numeric_token(token):
        return False
    return len(token) > 0 and token[0].isalpha()

def _is_numeric_token(token: str) -> bool:
    """Check if a token is a number (possibly with scientific notation or parentheses)."""
    token_clean = token.strip("()")
    try:
        float(token_clean)
        return True
    except ValueError:
        return False
