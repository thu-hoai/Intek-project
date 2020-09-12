#!/usr/bin/env python3
"""QR code FINDER in PURE PYTHON"""
import logging
import math
import itertools
import numpy as np
from PIL import Image
import exifread
from spriteutils import SpriteSheet, Sprite
from .constant import (
    TAG_ORIENTATION, IMAGE_ROTATION,
    VERSION, SQUARE_TOLERANCE,
    DENSITY_THRESHOLD, SIMILAR_SIZE_THRESHOLD,
    SIMILAR_DISTANCE_THRESHOLD, ORTHOGONALITY_THRESHOLD,
    SIMILAR_DISTANCE, POSITION, MIN_SURFACE_AREA)
from .utils import (
    _calculate_new_vertices_after_rotation,
    _calculate_distance_between_two_points,
    _calculate_relative_difference,
    _calculate_angle_between_three_points)

# Set logging
logging.basicConfig(level=logging.INFO, filemode='w')


# WP1: Load Image and Correct Orientation
def load_image_and_correct_orientation(file_path_name):
    """ Load Image and Correct Orientation
    Arguments:
        file_path_name (str): an file path name of a photo
    Returns:
        An object image of the photo which orientation
            have been corrected.
    """
    if not isinstance(file_path_name, str):
        raise TypeError("Not a file name path")

    image = Image.open(file_path_name)
    tags = {}

    # Open image file for reading binary mode
    with open(file_path_name, 'rb') as _file:
        # Get Exif tags without processing makernotes or extract thumbnail img
        tags = exifread.process_file(_file, details=False)

    # In case existing Exif
    if tags:
        orientation = tags[TAG_ORIENTATION]
        # Get tag values
        val = orientation.values

        if val[0] in IMAGE_ROTATION:
            rotation_lst = IMAGE_ROTATION[val[0]]
            for rotation in rotation_lst:
                image = image.transpose(rotation)

    return image


# WP2: Convert Image to Monochrome
def monochromize_image(image, brightness=0.5):
    """Convert Image to Monochrome
    Arguments:
        image (image object): an obj Image
    Keyword Arguments:
        brightness (float): th brightness value from 0.0 to 1.0
            used as a threshold (default: {0.0})
    Returns:
        (Image object): other object Image corresponding to
            the monochrome version of the given image
    """
    if not isinstance(image, Image.Image):
        raise ValueError("Not an Image object")
    if brightness:
        if not isinstance(brightness, float):
            raise TypeError("Brightness must be a float number")
        if brightness > 1.0 or brightness < 0.0:
            raise ValueError("Brightness value must be in [0.0, 1.0]")

    # Get threshold based on given brightness
    threshold = 255 * brightness

    # Convert image to grayscale first
    if image.mode != 'L':
        grayscale_image = image.convert("L")
    else:
        grayscale_image = image
    # Map pixel values of the image as follow:
    #  <= the threshold are converted to black (0)
    #  > the threshold are converted to white (255)
    monochrome_image = grayscale_image.point(
        lambda x: 0 if x <= threshold else 255, mode='1')

    return monochrome_image


# WP3: Determine Image Brightness
def calculate_brightness(image):
    """Calculate brightness of the image
    Arguments: image (an Image object)
    Returns: float: brightness of the image range 0.0 - 1.0
    """
    if not isinstance(image, Image.Image):
        raise ValueError("Not an Image object")
    # Take a list of pixel counts for each band present in the img
    histogram = image.convert('L').histogram()
    brightness = scale = len(histogram)
    # Finding mean values brightness level in image
    for i in range(scale):
        brightness += histogram[i] * (i - scale) / sum(histogram)
    return 1 if brightness == 255 else brightness / scale


# WP4: Filter Visible Sprites
def filter_visible_sprites(sprites, min_surface_area=MIN_SURFACE_AREA):
    """Filter Visible Sprites
    Arguments:
        sprites (list): a list of sprite objects
        min_surface_area (int): the minimal surface area of
            a sprite's bounding box to consider this sprite as visible.
    Returns:
        (list): list of the Sprite objects which surface area
            is equal to or larger than the specified minimal surface
    """
    if not isinstance(sprites, list):
        raise ValueError("Sprites is not a list")
    if not isinstance(min_surface_area, int):
        raise ValueError("min_surface_area must be an integer")
    return [sprite for sprite in sprites
            if sprite.surface > min_surface_area]


# Waypoint 5: Filter Square Sprites
def filter_square_sprites(sprites, similarity_threshold=SQUARE_TOLERANCE):
    """Find square sprites
    Arguments:
        sprites (list) list of sprite objects
        similarity_threshold (float): the relative difference of
            the width and height of the sprite's boundary box over
            which the sprite is not considered as a square.
    Returns:
        (list) a list of the Sprite objects
            which boundary box is almost a square.
    """
    if not isinstance(sprites, list):
        raise ValueError("Sprites is not a list")
    if not isinstance(similarity_threshold, float):
        raise ValueError("similarity_threshold must be an float num")
    if similarity_threshold > 1.0 or similarity_threshold < 0.0:
        raise ValueError("Brightness value must be in [0.0, 1.0]")

    return [sprite for sprite in sprites
            if _calculate_relative_difference(sprite.height, sprite.width)
            <= similarity_threshold]


# Waypoint 6: Filter Dense Sprites
def filter_dense_sprites(sprites, density_threshold=DENSITY_THRESHOLD):
    """Filter Dense Sprites
    Arguments:
        sprites (list) list of sprite objects
        density_threshold (float): the relative difference between
            the number of pixels of a sprite and the surface area
            of the boundary box of this sprite, over which the sprite
            is considered as dense.
    Returns:
        (list) a list of the Sprite objects that are dense.
    """
    if not isinstance(sprites, list):
        raise ValueError("Sprites is not a list")
    if not isinstance(density_threshold, float):
        raise ValueError("similarity_threshold must be an float num")
    if density_threshold > 1.0 or density_threshold < 0.0:
        raise ValueError("Brightness value must be in [0.0, 1.0]")

    return [sprite for sprite in sprites if sprite.density >= density_threshold]


def group_sprites_by_similar_size(sprites, similar_size_threshold):
    """Group Sprites by Similar Size
    Arguments:
        sprites (list) -- a list of sprite objects
        similar_size_threshold (float) -- the relative difference between
            the sizes (surface areas) of two sprites below which these sprites
            are considered similar.
    Returns:
        (dict): a dictionary with key is an integer and values is a list
            of similar size
            Ex: [[sprite1, sprite2, sprite3], [sprite4, sprite5]]
    """
    # Group sprites by similar size first
    similar_size_groups = {}
    lst_of_compared_size_sprites = []
    for i, sprite1 in enumerate(sprites):
        # Skip if catch a sprite which was compared
        if i in lst_of_compared_size_sprites:
            continue
        for j, sprite2 in enumerate(sprites):
            if j <= i:
                continue
            # Skip if catch a sprite which was compared
            if j in lst_of_compared_size_sprites:
                continue
            # Calculate size ratio betweem two sprite
            size_threshold = _calculate_relative_difference(
                sprite1.total_pixels_count,
                sprite2.total_pixels_count)
            # Filter as given similar_size_threshold
            if size_threshold > similar_size_threshold:
                continue
            # record indexs of sprites which were compared their size
            lst_of_compared_size_sprites.append(i)
            lst_of_compared_size_sprites.append(j)
            similar_size_groups.setdefault(i, []).append(sprite2)
            if sprite1 not in similar_size_groups[i]:
                similar_size_groups[i].append(sprite1)

    logging.debug("The number of similar size groups %s", len(similar_size_groups))
    return similar_size_groups


# Waypoint 7: Group Sprites by Similar Size and Distance
def group_sprites_by_similar_size_and_distance(
        sprites,
        similar_size_threshold=SIMILAR_SIZE_THRESHOLD,
        similar_distance_threshold=SIMILAR_DISTANCE_THRESHOLD):
    """Group Sprites by Similar Size and Distance
    Arguments:
        sprites (list) -- a list of sprite objects
        similar_size_threshold (float) -- the relative difference between
            the sizes (surface areas) of two sprites below which these sprites
            are considered similar.
        similar_distance_threshold (float) -- the relative difference between
            the distances from the sprites of 2 pairs below which these pairs
            are considered having similar distance.
    Returns:
        (list) a list of groups (lists) of pairs of sprites
        Ex: [((obj1, obj2), (obj1, obj3)), ((obj3, obj4), (obj4, obj5)),...]
    """

    # Group sprites by similar size first
    similar_size_groups = group_sprites_by_similar_size(
        sprites, similar_size_threshold)

    # Group Sprites by similar distance afterward
    similar_distance_groups = {}
    for key in similar_size_groups:
        similar_distance_groups.setdefault(key, [])

    for key, sprites_list in similar_size_groups.items():
        # Skip a lisch only have 1 or two sprites
        if len(sprites_list) < 3:
            continue

        # Group a list of elements into pairs
        list_of_tuple_pairs = list(itertools.combinations(sprites_list, 2))

        # Compare each of pairs
        for i, sprite_pair1 in enumerate(list_of_tuple_pairs):
            for j, sprite_pair2 in enumerate(list_of_tuple_pairs):
                if j <= i:
                    continue
                # Only add pairs which contain a common sprite object
                if set(sprite_pair1) & set(sprite_pair2):
                    distance1 = _calculate_distance_between_two_sprites(
                        sprite_pair1[0], sprite_pair1[1])
                    distance2 = _calculate_distance_between_two_sprites(
                        sprite_pair2[0], sprite_pair2[1])
                    # cal relative difference of distance betweent two pairs
                    distance_threshold = _calculate_relative_difference(
                        distance1, distance2)
                    # filter as given similar_distance_threshold
                    if distance_threshold <= similar_distance_threshold:
                        similar_distance_groups[key].append(
                            (sprite_pair1, sprite_pair2))

    return list(similar_distance_groups.values())


# Waypoint 8: Search Position Detection Patterns
def search_position_detection_patterns(
        sprite_pairs,
        orthogonality_threshold=ORTHOGONALITY_THRESHOLD):
    """Search Position Detection Patterns
    Arguments:
        sprite_pairs (list) -- A list of pairs of pairs sprites.
            For ex: [
                ((obj1, obj2), (obj3, obj2)),
                ((obj4, obj5), (obj5, obj6))]
            * NOTE that existing one commont element in each sprite pairs
        orthogonality_threshold {float} -- the relative difference between
            the angle of two pairs of sprites less or equal which the two pairs
            are considered orthogonal.
    Returns:
        list -- a list of 3 sprites (a tuple upper_left_sprite,
            upper_right_sprite, lower_left_sprite) that possibly corresponds to
            the position detection patterns of a QR code
    """

    if not isinstance(sprite_pairs, list):
        raise ValueError("sprite_pairs is not a list")
    if any([not isinstance(sprite_pair, tuple) for sprite_pair in sprite_pairs]):
        raise ValueError("sprite_pairs must be a list of pairs of a pair sprite")
    if any([len(sprite_pair) != 2 for sprite_pair in sprite_pairs]):
        raise ValueError("Each element of sprite_pairs must be a 2-element tuple")
    if not isinstance(orthogonality_threshold, float):
        raise ValueError("orthogonality_threshold must be an float num")
    if orthogonality_threshold > 1.0 or orthogonality_threshold < 0.0:
        raise ValueError("orthogonality_threshold must be in [0.0, 1.0]")

    # Intialize lists
    position_patterns_list = []  # to store patterns result
    upper_left_list = []  # temp list to check
    for pair in sprite_pairs:
        # Define upper_left_sprite by union two set of pairs
        upper_left_sprite = list(set(pair[0]) & set(pair[1]))[0]
        # upper_right_sprite, lower_left_sprite arbitrarily chosen
        upper_right_sprite = list(set(pair[0]) - set(pair[1]))[0]
        lower_left_sprite = list(set(pair[1]) - set(pair[0]))[0]

        if upper_left_sprite not in upper_left_list:
            # Calculate the angle of three center points
            angle = (_calculate_angle_between_three_points(
                upper_right_sprite.centroid,
                upper_left_sprite.centroid,
                lower_left_sprite.centroid))

            # Define exactly upper_right_sprite and lower_left_sprite
            if angle > 180:
                (upper_right_sprite, lower_left_sprite) \
                    = (lower_left_sprite, upper_right_sprite)
                angle = 360 - angle

            # Calculate orthogonal between the angle of two pairs of sprites
            orthogonality_ratio = _calculate_relative_difference(abs(angle), 90)
            # Filter as given orthogonality_threshold
            if orthogonality_ratio <= orthogonality_threshold:
                position_patterns_list.append(
                    (upper_left_sprite, upper_right_sprite, lower_left_sprite))
                upper_left_list.append(upper_left_sprite)

    return position_patterns_list


# Waypoint 9: Filter Matching Inner and Outer Finder Patterns
def filter_matching_inner_outer_finder_patterns(finder_patterns):
    """Filter Matching Inner and Outer Finder Patterns
    Arguments:
        finder_patterns: (list) -- a list of 3 sprites
            (a tuple upper_left_sprite, upper_right_sprite,
            lower_left_sprite) that possibly corresponds to
            the position detection patterns of a QR code
    Returns:
        (list): a list of tuples corresponding to the outer finder patterns.
    """
    # Loop to compare relative difference between centroid points
    # of each upper_left_ratio upper_right_sprite lower_left_sprite
    # of each pattern.
    # The centroid point positions of outer sprite and inner sprite nearly match

    for i, pattern1 in enumerate(finder_patterns):
        for j, pattern2 in enumerate(finder_patterns):
            if i >= j:
                continue
            # Calculate relative difference between centroid points
            # to define outer and inner sprite
            upper_left_ratio = _calculate_relative_difference(
                pattern1[POSITION["upper_left_sprite"]].centroid[0],
                pattern2[POSITION["upper_left_sprite"]].centroid[0])
            if upper_left_ratio > SIMILAR_DISTANCE:
                continue

            # Skip if upper_right_sprite of pattern1 match
            #  upper_right_sprite of pattern2
            if pattern1[POSITION["upper_right_sprite"]] == \
                    pattern2[POSITION["upper_right_sprite"]]:
                continue
            upper_right_ratio = _calculate_relative_difference(
                pattern1[POSITION["upper_right_sprite"]].centroid[0],
                pattern2[POSITION["upper_right_sprite"]].centroid[0])
            if upper_right_ratio > SIMILAR_DISTANCE:
                continue

            # Skip if lower_left_sprite of pattern1 match
            #  lower_left_sprite of pattern2
            if pattern1[POSITION["lower_left_sprite"]] == \
                    pattern2[POSITION["lower_left_sprite"]]:
                continue
            lower_left_ratio = _calculate_relative_difference(
                pattern1[POSITION["lower_left_sprite"]].centroid[0],
                pattern2[POSITION["lower_left_sprite"]].centroid[0])
            if lower_left_ratio > SIMILAR_DISTANCE:
                continue

            # Define pattern position as outer sprites
            if (pattern1[POSITION["lower_left_sprite"]].top_left >
                    pattern2[POSITION["lower_left_sprite"]].top_left)\
                and pattern1[POSITION["lower_left_sprite"]].bottom_right\
                < pattern2[POSITION["lower_left_sprite"]].bottom_right:

                return pattern2

            return pattern1


# Waypoint 10: Crop the QR Code Image Portion
def _update_new_outer_patterns(image, pattern_tuple):
    """Crop the QR Code Image Portion
    Arguments:
        image (PIL.Image): photo where the QR code has been found
        pattern_tuple (tuple):
            (upper_left_sprite, upper_right_sprite, lower_left_sprite)
            upper_left_sprite: A Sprite object corresponding to
                the Position Detection Pattern located at
                the upper left corner of the QR code.
            upper_right_sprite: A Sprite object corresponding to
                the Position Detection Pattern located at
                the upper right corner of the QR code.
            lower_left_sprite: A Sprite object corresponding to
                the Position Detection Pattern located at
                the lower left corner of the QR code.
    Returns:
        (PIL.Image) image corresponding to the portion of
            the QR code rotated and cropped from image.
        (list): a list of tuples corresponding to the UPDATED outer finder
            patterns (upper_left_sprite, upper_right_sprite, lower_left_sprite)
    """
    angle = _calculate_the_angel_to_rotate(pattern_tuple)

    # # Counter-clockwise rotation to get Original Image Rotated
    # rotated_image = image.rotate(angle)

    # Convert degree to radians
    radians = math.pi * angle / 180

    # the coordinates of the center point
    center_x, center_y = image.width / 2, image.height / 2

    # Init a list to define new position pattern
    new_outer_patterns = []
    # Loop through 3 patterns (upper_left, upper_right, lower_left)
    for i in range(3):
        # Calculate new coordinates of after rotation
        x_top_left, y_top_left = _calculate_new_vertices_after_rotation(
            center_x, center_y, radians, pattern_tuple[i])
        x_bottom_right, y_bottom_right = _calculate_new_vertices_after_rotation(
            center_x, center_y, radians, pattern_tuple[i], is_top_left=False)

        # Define new upper_left_sprite, upper_right_ratio, lower_left_sprite
        sprite = Sprite(i, x_top_left, y_top_left, x_bottom_right, y_bottom_right)
        new_outer_patterns.append(sprite)

    return new_outer_patterns


def crop_qr_code_image(image, pattern_tuple):
    """Crop the QR Code Image Portion
    Arguments:
        image (PIL.Image): photo where the QR code has been found
        pattern_tuple (tuple):
            (upper_left_sprite, upper_right_sprite, lower_left_sprite)
            which WERE UPDATED after rotation:
                upper_left_sprite: A Sprite object corresponding to
                    the Position Detection Pattern located at
                    the upper left corner of the QR code.
                upper_right_sprite: A Sprite object corresponding to
                    the Position Detection Pattern located at
                    the upper right corner of the QR code.
                lower_left_sprite: A Sprite object corresponding to
                    the Position Detection Pattern located at
                    the lower left corner of the QR code.
    Returns:
        (PIL.Image) image corresponding to the portion of
            the QR code rotated and cropped from image.
    """
    # Calculate angle to rotate
    angle = _calculate_the_angel_to_rotate(pattern_tuple)

    # Counter-clockwise rotation to get Original Image Rotated
    rotated_image = image.rotate(angle)

    # Get new coordinates of outer patterns
    new_outer_patterns = _update_new_outer_patterns(image, pattern_tuple)

    # Crop qr code fom Original Image Rotated based on
    cropped_qrcode = rotated_image.crop(
        (new_outer_patterns[0].top_left[0], #top_upper_left_x
         new_outer_patterns[0].top_left[1], #top_upper_left_y
         new_outer_patterns[1].bottom_right[0], #bottom_upper_right_x
         new_outer_patterns[2].bottom_right[1]) #bottom_lower_left_y
        )

    # Support trimming off more precisely
    pixels_arr = np.array(cropped_qrcode)
    coordinater_arrays = np.where(pixels_arr == 0)
    # Get new coordinates to trim
    top_upper_left_x = np.amin(coordinater_arrays[1])
    top_upper_left_y = np.amin(coordinater_arrays[0])
    bottom_upper_right_x = np.amax(coordinater_arrays[1])
    bottom_lower_left_y = np.amax(coordinater_arrays[0])
    precisely_trimmed_qr_image = cropped_qrcode.crop(
        (top_upper_left_x, top_upper_left_y,
         bottom_upper_right_x, bottom_lower_left_y)
        )

    return precisely_trimmed_qr_image


def _find_outer_pattern(image):

    # Find the number of sprites of provided image
    sprites = _get_sprites_object(image)
    logging.debug("Found total %s sprites", len(sprites))

    # Calculate min surface
    min_surface = _calculate_min_surface(image)

    # Find all visible sprites of provided image
    visible_sprites = filter_visible_sprites(
        sprites,
        min_surface_area=min_surface)
    logging.debug("The number of visible sprites: %s", len(visible_sprites))

    # Filter square sprites, only retain sprites who have a square shape
    square_sprites = filter_square_sprites(visible_sprites)
    logging.debug(" The number of square sprites: %s", len(square_sprites))

    # Filter dense sprites
    dense_sprites = filter_dense_sprites(square_sprites)
    logging.debug("The number of dense sprites: %s", len(dense_sprites))

    # Filter sprites by similar size and distance
    similar_groups = group_sprites_by_similar_size_and_distance(dense_sprites)

    # Initial a list of position pattern
    pattens_list = []
    for similar_group in similar_groups:
        # Filter position pattern
        position_patterns = search_position_detection_patterns(similar_group)
        for position_pattern in position_patterns:
            pattens_list.append(position_pattern)

    # Detect outer pattern
    outer_pattern = filter_matching_inner_outer_finder_patterns(pattens_list)

    return outer_pattern


# Resize provided image as needed
def _resize_image(image):
    width = image.width
    height = image.height
    if width > 1024 and height > 1024:
        ratio = max(width, height) / (1024 * 1.5)
        size = width // ratio, height // ratio
        # Get the thumbail
        image.thumbnail(size, Image.ANTIALIAS)


def _convert_to_monochrome_image(file_path_name, is_resize=True):
    image = Image.open(file_path_name)
    if is_resize:
        _resize_image(image)
    # Caculate the brightness of the image
    brightess = calculate_brightness(image)
    # Convert image to monochrome version
    monochrome_image = monochromize_image(image, brightess)
    return monochrome_image


# Caculate the angle to rotate
def _calculate_the_angel_to_rotate(pattern_tuple):
    # Get centroid coordinates of the upper_left_sprite
    point1 = pattern_tuple[POSITION['upper_left_sprite']].centroid
    # Get centroid coordinates of the upper_left_sprite
    point2 = pattern_tuple[POSITION['upper_right_sprite']].centroid

    # Calculate the angle between QR code and coordinate axis
    angle = _calculate_angle_between_three_points(point2, point1,
                                                  (0, point1[1]))

    return 180 - angle


def _get_sprites_object(monochrome_image):
    """Get a list of sprite objects from provided `monochrome_image`
    Arguments: image: an image object mono version
    Returns: list: a list of objects
    """
    # Create object Spritesheet and find all sprites
    sprite_sheet = SpriteSheet(monochrome_image, background_color=255)
    # Get a dict of all sprites of provided image
    sprites = sprite_sheet.find_sprites()[0]

    return list(sprites.values())


# Calculate relative distance difference between two sprites (Sprite object)
def _calculate_distance_between_two_sprites(sprite1, sprite2):
    # Calculate distance between 2 center points
    centerx_1, centery_1 = sprite1.centroid
    centerx_2, centery_2 = sprite2.centroid
    distance = _calculate_distance_between_two_points(
        centerx_1, centerx_2, centery_1, centery_2)

    return distance


# Calculate minimal surface area of a sprite bounding box to consider
#  all sprites of position detection Patterns as visible
def _calculate_min_surface(image, version=VERSION):
    # Estimate QR code area in provided image
    qr_code_area = image.width * image.height * 1 / 25
    # Estimate inner pattern area
    return int(qr_code_area * 9 / (17 + 4 * version) ** 2)
