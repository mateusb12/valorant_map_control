from pathlib import Path


def get_assets_folder():
    return Path(Path(__file__).parent / "assets")


def get_obstacle_behavior_folder():
    return Path(Path(__file__).parent / "obstacle_behavior")


def get_obstacles_folder():
    return Path(Path(__file__).parent / "obstacle_behavior" / "obstacles")


def get_corners_folder():
    return Path(Path(__file__).parent / "obstacle_behavior" / "corners")


def get_zone_control_folder():
    return Path(Path(__file__).parent / "obstacle_behavior" / "zone_control")
