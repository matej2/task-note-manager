from apscheduler.schedulers.background import BackgroundScheduler


class Scheduler:
    def __init__(self, task_list):
        self.scheduler = BackgroundScheduler()