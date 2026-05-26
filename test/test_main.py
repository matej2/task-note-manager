import unittest

from src.main import Application


class TestMain(unittest.TestCase):

    def test_init(self):
        application_under_test = Application()

        self.assertIsNotNone(application_under_test.config_manager)

        self.assertIsNotNone(application_under_test.file_manager)
        self.assertIsNotNone(application_under_test.note_factory)
        self.assertIsNotNone(application_under_test.notification_manager)

        self.assertIsNotNone(application_under_test.data_manager)
        self.assertIsNotNone(application_under_test.export_manager)




