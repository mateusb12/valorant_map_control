from pathlib import Path


def get_assets_folder():
    return Path(Path(__file__).parent / "assets")


def get_obstacle_behavior_folder():
    return Path(Path(__file__).parent / "obstacle_behavior")
