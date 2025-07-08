from typing import override

import notify2

from ConfigManager import ConfigManager
from notification.NotificationInterface import NotificationInterface


class Notification(NotificationInterface):
    def __init__(self, config_manager: ConfigManager) -> None:
        super().__init__(config_manager)

    @override
    def send_notification(self) -> None:
        notify2.Notification("Daily notification to enter data").show()
