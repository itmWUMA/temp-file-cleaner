"""
Main entry point for the TempCleaner command-line interface (CLI).
"""
import argparse
from pathlib import Path

from .engine import CleaningEngine, load_config

def main():
    """The main function for the CLI."""
    parser = argparse.ArgumentParser(
        description="TempCleaner: An automated file cleaning utility."
    )
    
    parser.add_argument(
        "command",
        choices=["run", "check-schedule"],
        help="The command to execute: 'run' for manual execution, 'check-schedule' for scheduled tasks."
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
        if not args.config.is_file():
            print(f"Error: Configuration file not found at '{args.config}'")
            return

        print(f"Loading configuration from: {args.config}")
        config = load_config(args.config)
        engine = CleaningEngine(config, dry_run=args.dry_run)

        if args.command == "run":
            engine.run_jobs()
            print("\nAll manual jobs completed.")
        elif args.command == "check-schedule":
            engine.run_scheduled_jobs()
            print("\nScheduled job check completed.")

    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()