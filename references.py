from pathlib import Path


def get_assets_folder():
    return Path(Path(__file__).parent / "assets")