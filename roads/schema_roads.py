import typing_extensions as typing


class Schema(typing.TypedDict):
    tree: bool
    crosswalk: bool
    stop_sign: bool
    traffic_light: bool
    chinese_calligraphy: bool
    bike_lane: bool
    fire_hydrant: bool
    sidewalk: bool
