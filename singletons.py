from yaml import load, dump
from pathlib import Path


# noinspection PyMethodMayBeStatic
class Vendor:
    obj = None
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

    def __new__(cls, *args, **kwargs):
        if cls.obj is None:
            cls.obj = object.__new__(cls)
        return cls.obj

    def __init__(self):
        self.paths = self._prepare_paths()
        self.data = self._prepare_data()

    def _prepare_paths(self):
        paths = {
            Vendor.FONTS: Path('res/fonts.yaml'),
            Vendor.STYLES: Path('res/styles.yaml'),
            Vendor.POSITIONS: Path('res/positions.yaml'),
            Vendor.RESULTS: Path('res/results.yaml'),
            Vendor.APP: Path('res/app.yaml'),
            Vendor.MAIN_MENU: Path('res/main_menu.yaml'),
            Vendor.SUMMARY_MENU: Path('res/summary_menu.yaml'),
            Vendor.INFO_MENU: Path('res/info_menu.yaml'),
            Vendor.HELP_MENU: Path('res/help_menu.yaml'),
            Vendor.GAME: Path('res/game.yaml')
        }
        self._resolve(paths)
        return paths

    def _resolve(self, paths):
        for path in paths.values():
            if not path.exists():
                self.dump('', path)

    def _prepare_data(self):
        return {k: self.load(v) for k, v, in self.paths.items()}

    def __getitem__(self, key):
        return self.data[key]

    def load(self, path):
        with open(path) as stream:
            return load(stream)

    def dump(self, data, path):
        with open(path, 'w') as stream:
            dump(data, stream, default_flow_style=False)


class Cache:
    obj = None

    def __new__(cls, *args, **kwargs):
        if cls.obj is None:
            cls.obj = object.__new__(cls)
        return cls.obj

    def __init__(self, vendor):
        self.vendor = vendor
        self.data = {}

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def update(self, key, updates, updater):
        self[key] = updater(self[key], updates)

    def save(self, key, path):
        self.vendor.dump(self[key], path)


class Forge:
    obj = None

    def __new__(cls, *args, **kwargs):
        if cls.obj is None:
            cls.obj = object.__new__(cls)
        return cls.obj

    def __init__(self, vendor):
        self.vendor = vendor
        pass
