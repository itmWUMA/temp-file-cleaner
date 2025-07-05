"""
Action to move a file or directory to the system's trash.
"""
from pathlib import Path

import send2trash

from .base import Action

class TrashAction(Action):
    """Action to move a file or directory to the system's trash."""

    def execute(self, file_path: Path, dry_run: bool = False):
        print(f"[DRY-RUN] Trashing: {file_path}" if dry_run else f"Trashing: {file_path}")
        if not dry_run:
            try:
                send2trash.send2trash(file_path)
            except Exception as e:
                print(f"Error while trashing {file_path}: {e}")