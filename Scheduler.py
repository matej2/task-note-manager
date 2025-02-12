from apscheduler.schedulers.background import BackgroundScheduler

from ConfigManager import ConfigManager


class Scheduler:
    def __init__(self, trigger_notification: callable, counter_notification: callable, config_manager: ConfigManager):
        self.scheduler = BackgroundScheduler()
        job = self.scheduler.add_job(trigger_notification, "interval", hours=config_manager.frequency)
        self.scheduler.add_job(lambda: counter_notification(job.next_run_time), "interval", minutes=1)

        self.scheduler.start()
