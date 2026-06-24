"""Parse Target.RP fixed-width text files and extract flagged compounds."""
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import re

FLAGGED_REVIEW_CODES = {"Udel", "Udelete", "dubious", "E-Code"}
UNKNOWN_TOKEN_EXCLUSIONS = {"Okay"}

@dataclass
class FlaggedCompound:
    """A compound row from Target.RP with a flagged review code."""
    name: str
    review_code: str
    sample_id: Optional[str] = None
    has_quad_error: bool = False

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
    on_column_start = None

    lines = content.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]

        if "REVIEW CODE" in line and "Compounds" in line:
            on_column_start = _find_on_column_position(line)
            i += 1
            if i < len(lines) and "===" in lines[i]:
                i += 1
                while i < len(lines):
                    data_line = lines[i]
                    if not data_line.strip() or "===" in data_line or "Page" in data_line:
                        break

                    compound = _parse_compound_row(data_line, on_column_start)
                    if compound:
                        if compound.review_code in FLAGGED_REVIEW_CODES or compound.has_quad_error:
                            compound.sample_id = sample_id
                            flagged.append(compound)
                        elif compound.review_code and compound.review_code not in UNKNOWN_TOKEN_EXCLUSIONS:
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

def _find_on_column_position(header_line: str) -> Optional[int]:
    """Find the starting column position of ON-COLUMN from header line.

    Scans for 'ON-COLUMN' text and returns its starting position.
    """
    match = re.search(r"ON-COLUMN", header_line)
    if match:
        return match.start()
    return None

def _parse_compound_row(line: str, on_column_start: Optional[int] = None) -> Optional[FlaggedCompound]:
    """Parse a single compound data row using fixed-width column positions.

    Compound name: columns ~10-40 (after row number, before numeric data).
    Review code: far right, look for known codes in the last tokens.
    ON-COLUMN: extract by position and check if numerical (Quad Erronious if not).
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

    tokens = line_stripped.split()
    review_code = ""
    has_quad_error = False

    if tokens:
        last_token = tokens[-1]
        if last_token in FLAGGED_REVIEW_CODES:
            review_code = last_token
        elif not _is_data_value(last_token):
            review_code = last_token

    # Check ON-COLUMN for non-numerical values
    if on_column_start is not None:
        on_column_value = _extract_on_column_value(line_stripped, on_column_start)
        if on_column_value is not None and not _is_on_column_numerical(on_column_value):
            has_quad_error = True
            review_code = "Quad Erronious"

    return FlaggedCompound(name=name, review_code=review_code, has_quad_error=has_quad_error)

def _extract_on_column_value(line: str, on_column_start: int) -> Optional[str]:
    """Extract ON-COLUMN value from a data line using fixed-width position.

    ON-COLUMN is followed by FINAL concentration. Extract the substring starting
    at on_column_start and ending before the next major column (approximately 13-15 chars).
    """
    if on_column_start >= len(line):
        return None

    on_column_section = line[on_column_start:on_column_start + 15].strip()
    if not on_column_section:
        return None

    return on_column_section

def _is_on_column_numerical(value: str) -> bool:
    """Check if ON-COLUMN value is numerical (valid concentration or empty).

    Returns True if value is:
    - Empty/whitespace only
    - A valid float number
    - A float with optional qualifier suffix like (M) or (QM)

    Returns False if value contains non-numerical text.
    """
    if not value or not value.strip():
        return True

    value_clean = re.sub(r"\([A-Za-z]+\)$", "", value).strip()
    if not value_clean:
        return True

    try:
        float(value_clean)
        return True
    except ValueError:
        return False

def _is_data_value(token: str) -> bool:
    """Check if token is a FINAL-concentration value, not a review code.

    REVIEW CODE is the last column in Target.RP — when it's blank, the last
    whitespace-separated token is actually the FINAL concentration, which
    carries an optional qualifier suffix glued directly to the number
    (e.g. "0.0764(M)", "0.128(QM)") with no separating space.
    """
    if re.match(r"^\([A-Za-z]+\)$", token):
        return True
    token_clean = re.sub(r"\([A-Za-z]+\)$", "", token).strip("()")
    try:
        float(token_clean)
        return True
    except ValueError:
        return False
