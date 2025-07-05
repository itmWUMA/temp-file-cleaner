"""
The core engine that loads configuration, runs jobs, applies filters,
and executes actions.
"""
import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional

from . import models
from . import filesystem
from . import filters

def _parse_filter_config(filter_list: List[Dict[str, Any]]) -> List[models.FilterConfig]:
    """Parses raw filter dictionaries into FilterConfig objects."""
    parsed_filters = []
    for f in filter_list:
        filter_type = list(f.keys())[0]
        filter_value = f[filter_type]
        
        args = {}
        if isinstance(filter_value, str):
            # Handles simple cases like 'pattern: "*.log"' or 'age: older_than: "30d"'
            # For age, we need to parse the inner string
            if ':' in filter_value:
                key, val = [x.strip() for x in filter_value.split(':', 1)]
                args[key] = val.strip('"\'')
            else:
                # for pattern
                args['pattern'] = filter_value

        else:
            args = filter_value

        parsed_filters.append(models.FilterConfig(type=filter_type, args=args))
    return parsed_filters

def load_config(config_path: Path) -> models.Config:
    """Loads and validates the YAML configuration file."""
    with open(config_path, 'r', encoding='utf-8') as f:
        raw_config = yaml.safe_load(f)

    if not raw_config or 'jobs' not in raw_config:
        raise ValueError("Configuration must contain a 'jobs' section.")

    job_list = []
    for name, details in raw_config['jobs'].items():
        job = models.Job(
            name=name,
            paths=details.get('paths', []),
            filters=_parse_filter_config(details.get('filters', [])),
            actions=[models.ActionConfig(type=a) for a in details.get('actions', [])],
            triggers=details.get('triggers', [])
        )
        job_list.append(job)
    
    return models.Config(jobs=job_list)


class CleaningEngine:
    """The main engine to execute cleaning jobs."""

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

    def _run_single_job(self, job: models.Job):
        """Runs one specific cleaning job."""
        print(f"\n--- Running Job: {job.name} ---")

        # 1. Find all files based on paths and pattern filters
        initial_files = self._find_initial_files(job)
        if not initial_files:
            print("No files found matching path/pattern criteria.")
            return

        # 2. Apply remaining filters (e.g., age)
        other_filters = [f for f in job.filters if f.type != 'pattern']
        files_to_clean = filters.apply_filters(initial_files, other_filters)

        if not files_to_clean:
            print("All initial files were filtered out. Nothing to clean.")
            return

        # 3. Execute actions on the filtered files
        print(f"Found {len(files_to_clean)} item(s) to clean:")
        for file_path in files_to_clean:
            self._execute_actions(file_path, job.actions)
        
        print(f"--- Job {job.name} Finished ---")

    def _find_initial_files(self, job: models.Job) -> List[Path]:
        """Finds files based on `paths` and `pattern` filters."""
        all_files = []
        # There should be exactly one pattern filter per job as per PRD logic
        pattern_filter = next((f for f in job.filters if f.type == 'pattern'), None)
        if not pattern_filter:
            print(f"Warning: Job '{job.name}' has no pattern filter. It will not match any files.")
            return []
        
        pattern = pattern_filter.args.get('pattern', '')

        for path_str in job.paths:
            base_path = filesystem.resolve_path(path_str)
            print(f"Scanning in '{base_path}' for pattern '{pattern}'...")
            all_files.extend(filesystem.find_files(base_path, pattern))
        
        return list(set(all_files)) # Return unique paths

    def _execute_actions(self, file_path: Path, actions: List[models.ActionConfig]):
        """Executes the defined actions on a single file."""
        for action in actions:
            if action.type == 'trash':
                filesystem.trash_item(file_path, self.dry_run)
            elif action.type == 'delete':
                filesystem.delete_item(file_path, self.dry_run)
            else:
                print(f"Warning: Unknown action type '{action.type}' for file {file_path}")