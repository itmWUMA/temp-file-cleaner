"""
The core engine that loads configuration, runs jobs, applies filters,
and executes actions.
"""
import yaml
from pathlib import Path
from typing import List
from datetime import datetime

from . import models
from . import filesystem
from . import registry

def load_config(config_path: Path) -> models.Config:
    """Loads, parses, and transforms the YAML configuration into structured objects."""
    with open(config_path, 'r', encoding='utf-8') as f:
        raw_config = yaml.safe_load(f)

    if not raw_config or 'jobs' not in raw_config:
        raise ValueError("Configuration must contain a 'jobs' section.")

    job_list = []
    for name, details in raw_config['jobs'].items():
        # Use the registry to create action and filter objects
        raw_actions = details.get('actions', [])
        actions = [registry.create_action(a) for a in raw_actions]

        # Separate pattern filter from other filters
        raw_filters = details.get('filters', [])
        pattern_config = next((f for f in raw_filters if 'pattern' in f), None)
        other_filters_config = [f for f in raw_filters if 'pattern' not in f]
        
        filters = [registry.create_filter(f) for f in other_filters_config]

        raw_triggers = details.get('triggers', [])
        triggers = [registry.create_trigger(t) for t in raw_triggers]

        job = models.Job(
            name=name,
            paths=details.get('paths', []),
            pattern=pattern_config['pattern'] if pattern_config else None,
            filters=filters,
            actions=actions,
            triggers=triggers
        )
        job_list.append(job)
    
    return models.Config(jobs=job_list)


class CleaningEngine:
    """The main engine to execute cleaning jobs using strategy objects."""

    def __init__(self, config: models.Config, dry_run: bool = False):
        self.config = config
        self.dry_run = dry_run
        print(f"Engine initialized. Dry run: {'Enabled' if dry_run else 'Disabled'}")

    def run_jobs(self):
        """Executes all jobs defined in the configuration."""
        if not self.config.jobs:
            print("No jobs found in configuration. Nothing to do.")
            return

        print(f"Found {len(self.config.jobs)} job(s) to process.")
        for job in self.config.jobs:
            self._run_single_job(job)

    def run_scheduled_jobs(self):
        """
        Executes jobs that are due to run based on their 'schedule' trigger.
        """
        if not self.config.jobs:
            print("No jobs found in configuration.")
            return

        print("Checking for scheduled jobs to run...")
        now = datetime.now()
        
        for job in self.config.jobs:
            for trigger in job.triggers:
                # We only care about triggers that implement should_run
                if hasattr(trigger, 'should_run') and trigger.should_run(now):
                    print(f"Trigger activated for job '{job.name}'.")
                    self._run_single_job(job)
                    # A job should only run once per check, even if it has multiple triggers.
                    break

    def _run_single_job(self, job: models.Job):
        """Runs one specific cleaning job."""
        print(f"\n--- Running Job: {job.name} ---")

        # 1. Find all files based on paths and the primary pattern filter.
        initial_files = self._find_initial_files(job)
        if not initial_files:
            print("No files found matching path/pattern criteria.")
            return

        # 2. Apply all secondary filters (strategy objects).
        files_to_clean = self._apply_secondary_filters(initial_files, job.filters)

        if not files_to_clean:
            print("All initial files were filtered out. Nothing to clean.")
            return

        # 3. Execute actions on the filtered files.
        print(f"Found {len(files_to_clean)} item(s) to clean:")
        for file_path in files_to_clean:
            self._execute_actions(file_path, job.actions)
        
        print(f"--- Job {job.name} Finished ---")

    def _find_initial_files(self, job: models.Job) -> List[Path]:
        """Finds files based on `paths` and the primary `pattern` filter."""
        if not job.pattern:
            print(f"Warning: Job '{job.name}' has no pattern filter. It will not match any files.")
            return []
        
        all_files = set()
        for path_str in job.paths:
            base_path = filesystem.resolve_path(path_str)
            print(f"Scanning in '{base_path}' for pattern '{job.pattern}'...")
            found = filesystem.find_files(base_path, job.pattern)
            all_files.update(found)
        
        return list(all_files)

    def _apply_secondary_filters(self, files: List[Path], filters: List[models.Filter]) -> List[Path]:
        """Applies a list of filter objects to a list of files."""
        filtered_files = files
        for f in filters:
            # The engine doesn't know what kind of filter it is, it just calls `matches`.
            filtered_files = [path for path in filtered_files if f.matches(path)]
        return filtered_files

    def _execute_actions(self, file_path: Path, actions: List[models.Action]):
        """Executes the defined action objects on a single file."""
        for action in actions:
            # The engine doesn't know what kind of action it is, it just calls `execute`.
            action.execute(file_path, self.dry_run)