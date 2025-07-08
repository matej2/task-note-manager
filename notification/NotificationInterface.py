from ConfigManager import ConfigManager


class NotificationInterface:
    def __init__(self, config_manager: ConfigManager) -> None:
        self.config_manager = config_manager

    def send_notification(self) -> None:
        raise NotImplementedError
