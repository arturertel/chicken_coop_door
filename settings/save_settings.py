import ujson


class Settings:

    file_name = 'settings/settings.json'

    def __init__(self, open_time, close_time):
        self.open = open_time
        self.close = close_time

    @staticmethod
    def getDefault():
        return Settings([06, 30], [18, 30])

    def save(self):
        if self.open == self.close:
            print("Öffnungs- und Schließzeit dürfen nicht gleich sein!")
            return
        settings_json = ujson.dumps(self.__dict__)
        print('Saving:', settings_json)
        try:
            f = open(Settings.file_name, 'w')
            f.write(settings_json)
            f.close()
            return True
        except:
            return False

    @staticmethod
    def load():
        try:
            f = open(Settings.file_name, 'r')
            settings_string = f.read()
            f.close()
            print('Got settings:', settings_string)
            settings_dict = ujson.loads(settings_string)
            result = Settings.getDefault()
            for setting in settings_dict:
                print("Setting:", setting)
                setattr(result, setting, settings_dict[setting])
            return result
        except:
            print('Settings file load failed')
            return Settings.getDefault()
