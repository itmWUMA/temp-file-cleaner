"""
Implements the 'schedule' trigger using cron expressions.
"""
from datetime import datetime
from croniter import croniter, CroniterBadCronError
from .base import Trigger

class ScheduleTrigger(Trigger):
    """
    A trigger that fires based on a cron-style schedule.
    """

    def __init__(self, schedule: str):
        """
        Initializes the trigger with a cron expression.

        Args:
            schedule: A string representing the cron schedule (e.g., "0 0 * * *").

        Raises:
            ValueError: If the cron expression is invalid.
        """
        try:
            # Check if the expression is valid upon initialization
            self._schedule_iterator = croniter(schedule, datetime.now())
            self._schedule_str = schedule
        except CroniterBadCronError as e:
            raise ValueError(f"Invalid cron expression '{schedule}': {e}")

    def should_run(self, current_time: datetime) -> bool:
        """
        Checks if a job should run by comparing the current time to the last
        and next scheduled run times.

        This logic ensures that if the script is run slightly after the exact
        cron time, it still executes. It assumes the check runs frequently
        (e.g., every few minutes).
        """
        # Reset the iterator to the current time for accurate comparison
        self._schedule_iterator.set_current(current_time)
        
        # Get the previously scheduled run time
        prev_run = self._schedule_iterator.get_prev(datetime)
        
        # We consider the job should run if the current time is within
        # one minute past the scheduled time. This handles cases where
        # the scheduler isn't perfectly on the second.
        return (current_time - prev_run).total_seconds() <= 60

    def __repr__(self) -> str:
        return f"ScheduleTrigger(schedule='{self._schedule_str}')"
