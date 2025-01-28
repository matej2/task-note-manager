from apscheduler.schedulers.background import BackgroundScheduler


class Scheduler:
    def __init__(self, function: callable):
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(function, 'interval', hours=3)
        self.scheduler.start()
