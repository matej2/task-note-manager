from win11toast import toast

from ConfigManager import ConfigManager
from notification.NotificationInterface import NotificationInterface


class Notification(NotificationInterface):
    def __init__(self, config_manager: ConfigManager) -> None:
        super().__init__(config_manager)

    def send_notification(self) -> None:
        toast("Enter data", "Daily notification to enter data")
