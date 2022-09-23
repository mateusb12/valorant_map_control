import pygame


def rotate(surface, input_angle, input_pivot, input_offset):
    """Rotate the surface around the pivot point.

    Args:
        surface (pygame.Surface): The surface that is to be rotated.
        input_angle (float): Rotate by this angle.
        input_pivot (tuple, list, pygame.math.Vector2): The pivot point.
        input_offset (pygame.math.Vector2): This vector is added to the pivot.
    """
    rotated_image_a = pygame.transform.rotozoom(surface, -input_angle, 1)  # Rotate the image.
    rotated_offset = input_offset.rotate(input_angle)  # Rotate the offset vector.
    # Add the offset vector to the center/pivot point to shift the rect.
    transformed_rect = rotated_image_a.get_rect(center=input_pivot + rotated_offset)
    return rotated_image_a, transformed_rect  # Return the rotated image and shifted rect.
