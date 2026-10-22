import asyncio

from desktop_notifier import DesktopNotifier

from src.manager.ConfigManager import ConfigManager
from src.notification.NotificationInterface import NotificationInterface


class Notification(NotificationInterface):
    def __init__(self, config_manager: ConfigManager) -> None:
        super().__init__(config_manager)
        self.notifier = DesktopNotifier(app_name="Task Note Manager")

    async def send_info_notification(self, text: str):
        await self.notifier.send(
            title="Task Note Manager",
            message=text
        )

    def send_notification(self) -> None:
        asyncio.run(self.send_info_notification(text="Daily notification to enter data"))
