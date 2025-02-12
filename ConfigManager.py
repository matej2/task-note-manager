import os


class ConfigManager:
    def __init__(self):
        self.font_family = "Arial"
        self.font_size_small = 8
        self.font_size_normal = 10
        self.font_size_large = 12
        self.date_format = "%d %b, %Y"
        self.frequency = 6

        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.full_path = os.path.join(self.current_dir, "demofile2.txt")

    def __str__(self):
        return """
Font family: {}
Font size: {}
Date format: {}
Frequency: {}
Output file: {}""".format(self.font_family, self.font_size_normal, self.date_format, self.frequency, self.full_path)
