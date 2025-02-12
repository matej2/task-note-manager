class ConfigManager:
    def __init__(self):
        self.font_family = "Arial"
        self.font_size_small = 8
        self.font_size_normal = 10
        self.font_size_large = 12
        self.date_format = "%d %b, %Y"
        self.frequency = 6

    def __str__(self):
        return """
Font family: {}
Font size: {}
Date format: {}
Frequency: {}""".format(self.font_family, self.font_size_normal, self.date_format, self.frequency)
