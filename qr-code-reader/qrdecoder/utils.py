#!/usr/bin/env python3
"""The Utility Of QR Code Finder And Decoder"""
import math

# Calculate new vertice of `sprite` of a rotated square
# after rotation arround a point `(x0, y0)` by `rad_angle`
def _calculate_new_vertices_after_rotation(x0, y0, rad_angle, sprite,
                                           is_top_left=True):
    # Get center point coordinates of provided sprite
    center_point = sprite.centroid

    # Get new coordinates of center points of sprite after rotation `rad_angle`
    new_center_x, new_center_y = _get_new_coordinates(
        center_point[0], center_point[1],
        x0, y0, rad_angle)
    # Calculate coordinates of bounding box's sprite
    # In case provided point is upper left sprites
    if is_top_left:
        return new_center_x - sprite.width // 2,\
            new_center_y - sprite.height // 2

    return new_center_x + sprite.width // 2,\
        new_center_y + sprite.height // 2



# Calculate distance between two poins
def _calculate_distance_between_two_points(x1, x2, y1, y2):
    # (x1, y1): coordidates of the first point
    # (x2, y2): coordidates of the second point
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# Get new coordinates of a point `(x, y)` after rotation `rad_angle`
# around a point `(x0, y0)`
# rad_angle is in radians
def _get_new_coordinates(x, y, x0, y0, rad_angle):
    new_x_coordinate = int(
        (x - x0) * math.cos(rad_angle) +
        (y - y0) * math.sin(rad_angle) + x0)
    new_y_coordinate = int(
        -(x - x0) * math.sin(rad_angle) +
        (y - y0) * math.cos(rad_angle) + y0)

    return new_x_coordinate, new_y_coordinate


# Calculate relative difference between two values
def _calculate_relative_difference(value1, value2):
    return abs(value1 - value2) / ((value1 + value2) / 2)


# Calculate angle (degrees) between 3 points
def _calculate_angle_between_three_points(point1, point2, point3):
    # #------------------------------------------>x
    # #|        A(point3)
    # #|        /
    # #|       /
    # #|      /
    # #|     /__________
    # #|   B(point2)    C(point1)
    # #V y
    #     point1 (tuple) -- C(x, y)coordinates of the point1
    #     point2 (tuple) -- B(x, y)coordinates of the point2
    #     point3 (tuple) -- A(x, y)coordinates of the point3

    angle = math.degrees(
        math.atan2(point3[1] - point2[1], point3[0] - point2[0])
        - math.atan2(point1[1] - point2[1], point1[0] - point2[0]))
    return angle + 360 if angle < 0 else angle


# Convert a binary list to character
# For [0,1,1,0,1,0,0,0] --> 'h'
def _convert_binary_to_character(binary_list):
    if not all([bit in(0, 1) for bit in binary_list]):
        raise ValueError('Either 0 or 1 exists in binary list')
    # Get binary string
    binary_string = ''.join(str(char) for char in binary_list)
    # Return character follow ASCII
    return chr(int(binary_string, 2))
