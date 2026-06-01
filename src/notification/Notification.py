from win11toast import toast, notify

from src.manager.ConfigManager import ConfigManager
from src.notification.NotificationInterface import NotificationInterface


class Notification(NotificationInterface):
    def __init__(self, config_manager: ConfigManager) -> None:
        super().__init__(config_manager)

    @staticmethod
    def send_info_notification(text: str):
        toast("Task Note Manager", text)

    def send_notification(self) -> None:
        toast("Task Note Manager", "Daily notification to enter data", scenario='reminder')
