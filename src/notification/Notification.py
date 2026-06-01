import notify2
from typing_extensions import override

from src.manager.ConfigManager import ConfigManager
from src.notification.NotificationInterface import NotificationInterface


class Notification(NotificationInterface):
    def __init__(self, config_manager: ConfigManager) -> None:
        super().__init__(config_manager)
        notify2.init("Task Note Manager")

    @staticmethod
    def send_info_notification(text: str):
        notification = notify2.Notification(text)
        notification.set_timeout(5000)
        notification.show()

    @override
    def send_notification(self) -> None:
        notify2.Notification("Daily notification to enter data").show()
