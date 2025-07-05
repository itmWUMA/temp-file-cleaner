"""
Action to permanently delete a file or directory.
"""
import shutil
from pathlib import Path

from .base import Action

class DeleteAction(Action):
    """Action to permanently delete a file or directory."""

    def execute(self, file_path: Path, dry_run: bool = False):
        print(f"[DRY-RUN] Deleting permanently: {file_path}" if dry_run else f"Deleting permanently: {file_path}")
        if not dry_run:
            try:
                if file_path.is_dir():
                    shutil.rmtree(file_path)
                else:
                    file_path.unlink()
            except Exception as e:
                print(f"Error while deleting {file_path}: {e}")