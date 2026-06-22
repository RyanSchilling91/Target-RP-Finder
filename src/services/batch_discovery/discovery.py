"""Discover and classify .d folders in a .b batch folder."""
from pathlib import Path
from dataclasses import dataclass
from typing import Literal
import re

FolderType = Literal["sample", "calibration", "ccv", "tpc", "idl", "blank", "prep_blank", "surrogate", "unclassified"]

@dataclass
class ClassifiedFolder:
    """Result of classifying a .d folder."""
    name: str
    folder_type: FolderType
    path: Path

def classify_folder(folder_name: str) -> FolderType:
    """Classify a .d folder by name using case-insensitive prefix matching and numeric rules.

    Rules (applied in order):
    1. Prefix (case-insensitive): cal → calibration, ccv → ccv, cstpc/tpc → tpc, idl → idl, peb → blank
    2. 11-digit numeric (with optional .d suffix): YYYY (year) + DDD (Julian day) + 4-digit run number
       - Thousands digit of run number: 9 → prep_blank, 8 → surrogate, else → sample
    3. Else → unclassified
    """
    name_lower = folder_name.lower()
    name_clean = folder_name.rstrip('.d') if folder_name.endswith('.d') else folder_name

    if name_lower.startswith("cal"):
        return "calibration"
    if name_lower.startswith("ccv"):
        return "ccv"
    if name_lower.startswith("cstpc") or name_lower.startswith("tpc"):
        return "tpc"
    if name_lower.startswith("idl"):
        return "idl"
    if name_lower.startswith("peb"):
        return "blank"

    if re.match(r"^\d{11}$", name_clean):
        run_number_str = name_clean[7:11]
        thousands_digit = int(run_number_str[0])

        if thousands_digit == 9:
            return "prep_blank"
        if thousands_digit == 8:
            return "surrogate"
        return "sample"

    return "unclassified"

def discover_samples(batch_folder: str | Path) -> list[ClassifiedFolder]:
    """Scan a .b batch folder, classify all .d subfolders, return only samples.

    Returns a list of ClassifiedFolder objects with folder_type == "sample".
    Skips any folders that cannot be opened or are not directories.
    """
    batch_path = Path(batch_folder)
    if not batch_path.is_dir():
        return []

    samples = []
    try:
        for item in batch_path.iterdir():
            if not item.is_dir():
                continue

            folder_type = classify_folder(item.name)
            if folder_type == "sample":
                samples.append(ClassifiedFolder(
                    name=item.name,
                    folder_type=folder_type,
                    path=item
                ))
    except (PermissionError, OSError):
        pass

    return sorted(samples, key=lambda x: x.name)
