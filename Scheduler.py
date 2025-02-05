from apscheduler.schedulers.background import BackgroundScheduler


class Scheduler:
    def __init__(self, function: callable, frequency: int = 3):
        self.frequency = frequency
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(function, 'interval', hours=6)
        self.scheduler.start()
