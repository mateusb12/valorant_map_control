def rectangle_parameters_from_coordinates(top_left: tuple[int, int], top_right: tuple[int, int],
                                          bottom_left: tuple[int, int],
                                          bottom_right: tuple[int, int]) -> tuple[int, int, int, int]:
    width = top_right[0] - top_left[0]
    height = bottom_left[1] - top_left[1]
    return top_left[0], top_left[1], width, height
