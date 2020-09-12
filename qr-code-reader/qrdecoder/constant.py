#!/usr/bin/env python3
"""Constants for qrdecoder"""
from PIL import Image

# Exifread orientation tag
TAG_ORIENTATION = "Image Orientation"


IMAGE_ROTATION = {
    2: [Image.FLIP_LEFT_RIGHT],
    3: [Image.ROTATE_180],
    4: [Image.FLIP_TOP_BOTTOM],
    5: [Image.TRANSPOSE],
    6: [Image.ROTATE_270],
    7: [Image.TRANSVERSE],
    8: [Image.ROTATE_90]
}
# Predicted Version of QR code
VERSION = 10


# Threshold
MIN_SURFACE_AREA = 100
SQUARE_TOLERANCE = 0.13
DENSITY_THRESHOLD = 0.25
SIMILAR_SIZE_THRESHOLD = 0.18
SIMILAR_DISTANCE_THRESHOLD = 0.1
ORTHOGONALITY_THRESHOLD = 0.13
SIMILAR_DISTANCE = 0.04


# Position of 3-point pattern in list
POSITION = {"upper_left_sprite": 0, "upper_right_sprite": 1,
            "lower_left_sprite": 2}

# QR Code info
#  A module with a light area corresponds to the bit 0
WHITE = 0
# A module with a dark area corresponds to the bit 1
BLACK = 1
# The number of modules of each outer pattern position
PATTERN_SIZE = 7

# Len of Endcoding Mode
ENCODING_LEN = 4

# Encoding mode
MODE = {
    '0001': 'NUMERIC',
    '0010': 'ALPHANUMERIC',
    '0100':'BYTE'
    }

EC_LEVEL = {
    '11': 'L',
    '10': 'M',
    '01': 'Q',
    '00': 'H',
}
TERMINATOR_SEQ = '0000'

# Row/Column coordinates of center module
ALIGNMENT_POSITIONS = [
    [], #1
    [6, 18], #2
    [6, 22], #3
    [6, 26], #4
    [6, 30], #5
    [6, 34], #6
    [6, 22, 38], #7
    [6, 24, 42], #8
    [6, 26, 46], #9
    [6, 28, 50]  #10
    ]
