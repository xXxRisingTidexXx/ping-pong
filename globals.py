from yaml import load, dump


# noinspection PyMethodMayBeStatic
class Rm:
    FONTS = 'fonts'
    STYLES = 'styles'
    POSITIONS = 'positions'
    RESULTS = 'results'
    APP = 'app'
    MAIN_MENU = 'main_menu'
    SUMMARY_MENU = 'summary_menu'
    INFO_MENU = 'info_menu'
    HELP_MENU = 'help_menu'
    GAME = 'game'
    PATHS = {
        FONTS: 'res/fonts.yaml',
        STYLES: 'res/styles.yaml',
        POSITIONS: 'res/positions.yaml',
        RESULTS: 'res/results.yaml',
        APP: 'res/app.yaml',
        MAIN_MENU: 'res/main_menu.yaml',
        SUMMARY_MENU: 'res/summary_menu.yaml',
        INFO_MENU: 'res/info_menu.yaml',
        HELP_MENU: 'res/help_menu.yaml',
        GAME: 'res/game.yaml'
    }

    def __init__(self):
        self.data = {k: self.read(v) for k, v in Rm.PATHS.items()}

    def __getitem__(self, res):
        return self.data[res]

    def read(self, path):
        with open(path) as stream:
            return load(stream)

    def write(self, data, path):
        with open(path, 'w') as stream:
            dump(data, stream, default_flow_style=False)


RM = Rm()


class Cache:
    def __init__(self, rm):
        self.rm = rm
        self.data = {Rm.RESULTS: self.rm[Rm.RESULTS]}

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def update(self, key, value, updater):
        self[key] = updater(self[key], value)

    def save(self, key, path):
        self.rm.write(self[key], path)


CACHE = Cache(RM)


class Screen:
    def __init__(self, tk, name):
        self.tk = tk
        self.data = RM[name]
