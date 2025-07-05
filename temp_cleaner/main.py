"""
Main entry point for the TempCleaner command-line interface (CLI).
"""
import argparse
import sys
from pathlib import Path

from .engine import CleaningEngine, load_config

def main():
    """The main function for the CLI."""
    parser = argparse.ArgumentParser(
        description="TempCleaner: An automated file cleaning utility."
    )
    
    parser.add_argument(
        "command",
        choices=["run", "check-schedule", "on-startup", "on-shutdown"],
        help="The command to execute."
    )
    
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config.yaml"),
        help="Path to the configuration file (default: config.yaml in the current directory)."
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the cleaning process without actually deleting or moving files."
    )
    
    args = parser.parse_args()
    
    try:
        # Determine the base path of the executable to resolve relative paths
        if getattr(sys, 'frozen', False):
            # If running in a PyInstaller bundle
            base_path = Path(sys.executable).parent
        else:
            # If running as a normal script
            base_path = Path(__file__).parent.parent

        # Resolve the config path against the base path
        config_path = args.config
        if not config_path.is_absolute():
            config_path = base_path / config_path

        if not config_path.is_file():
            print(f"Error: Configuration file not found at '{config_path}'")
            return

        print(f"Loading configuration from: {config_path}")
        config = load_config(config_path)
        engine = CleaningEngine(config, dry_run=args.dry_run)

        if args.command == "run":
            print("--- Running all jobs manually ---")
            engine.run_jobs()
            print("\nManual run completed.")
        elif args.command == "check-schedule":
            engine.run_scheduled_jobs()
            print("\nScheduled job check completed.")
        elif args.command == "on-startup":
            engine.run_startup_jobs()
            print("\nStartup job check completed.")
        elif args.command == "on-shutdown":
            engine.run_shutdown_jobs()
            print("\nShutdown job check completed.")

    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()