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
        choices=["run"],
        help="The command to execute. Currently, only 'run' is supported."
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
    
    if args.command == "run":
        if not args.config.is_file():
            print(f"Error: Configuration file not found at '{args.config}'")
            return

        try:
            print(f"Loading configuration from: {args.config}")
            config = load_config(args.config)
            
            engine = CleaningEngine(config, dry_run=args.dry_run)
            engine.run_jobs()
            
            print("\nAll jobs completed.")
            
        except Exception as e:
            print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()