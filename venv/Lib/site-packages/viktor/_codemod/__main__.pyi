from pathlib import Path

U_MIN: int

class PrintStyle:
    RED: str
    GREEN: str
    BOLD: str
    END: str

def fix(root_dir: Path, upgrades: list[int], apply: bool, keep_original: bool):
    """ Initiates the codemod for specified upgrade id.

    :param root_dir: path to the app's root directory.
    :param upgrades: Upgrade IDs to be fixed.
    :param apply: If True, user prompt is skipped and all diffs are applied.
    :param keep_original: If True, the source of modified files is stored in the corresponding .orig.py files.
    """
def fix_upgrade(root_dir: Path, upgrade_id: int, apply: bool, keep_original: bool, patched_files: list) -> None: ...
