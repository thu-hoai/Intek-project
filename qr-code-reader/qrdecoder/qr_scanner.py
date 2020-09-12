#!/usr/bin/env python3
"""QR code Information Scanner in PURE PYTHON"""
import logging
import itertools
from PIL import Image
import numpy as np
from qrdecoder.constant import (
    PATTERN_SIZE, WHITE, BLACK, ALIGNMENT_POSITIONS, EC_LEVEL)
from qrdecoder.qr_finder import (
    _find_outer_pattern, crop_qr_code_image,
    _convert_to_monochrome_image,
    _update_new_outer_patterns)
from qrdecoder.qr_zig_zag import _get_data_and_error_correction_area_coordinaters
from qrdecoder.utils import (
    _calculate_distance_between_two_points)
from qrdecoder.exception import (
    NoMaskIdException,
    NotCorrectVersionException)


# Set logging
logging.basicConfig(level=logging.DEBUG, filemode='w')


class QRCodeInfo:
    """Class QRCodeInfo represent the information of a QR Symbol"""
    def __init__(self, version):
        if not isinstance(version, int):
            raise ValueError('Version must an integer value')
        if version < 0 or version > 40:
            raise NotCorrectVersionException('Version must in [0, 40]')

        self.__version = version
        self.__qr_width = 17 + 4 * self.__version
        self.__mask_id = None
        self.__error_level = None


    @property
    def mask_id(self):
        """int: Represent mask id of QR code"""
        return self.__mask_id

    @property
    def version(self):
        """int: Represent version of QR code"""
        return self.__version

    @property
    def qr_width(self):
        """int: Represent the number of modules
            on one row of the QR code symbol)"""
        return self.__qr_width

    @mask_id.setter
    def mask_id(self, mask_id):
        self.__mask_id = mask_id

    @property
    def error_level(self):
        """int: Represent Error correction level of QR code"""
        return self.__error_level


    def read_format_information(self, bit_matrix):
        """Update mask id and error correction level

        Arguments:
            bit_matrix {numpy.darray} : modules matrix
        """

        if not isinstance(bit_matrix, np.ndarray) and \
            not isinstance(bit_matrix, list):
            raise ValueError("bit matrix must be an array or  list type")

        # Get the binary string format informatrion
        # Upwards in lower-left corner
        format_info_chain1 = [bit_matrix[i, 8] for i in \
            range(self.qr_width - 7, self.qr_width)]

        # Left-to_right in the upper-right corner
        format_info_chain2 = [bit_matrix[8, i] for i in \
            range(0, 7)]

        # format_ec = tuple(format_info_chain1[0:2])
        mask_pattern = format_info_chain1[2:5]
        # ec_level = format_info_chain1[5:7]
        mask_str = ''.join(str(char) for char in mask_pattern)
        # ec_level = ''.join(str(char) for char in ec_level)
        ec_lst = format_info_chain2[:2]
        ec_string = ''.join(str(c) for c in ec_lst)
        ec_level = EC_LEVEL[ec_string]
        # Update mask it to object
        mask_id = int(mask_str, 2)
        if mask_id > 7 or mask_id < 0:
            raise NoMaskIdException
        self.__mask_id = mask_id
        self.__error_level = ec_level


    def __str__(self):
        return f"Version {self.version}, qr_width {self.qr_width}, " + \
            f"mask {self.mask_id}, EC_level {self.error_level}"


class QRCodeImage:
    """Class QRCodeImage represent information of a QR Code Image"""

    def __init__(self, file_path_name):
        """ The constructor of QRCodeImage class

        Parameters:
            file_path_name: A PIL.Image obj, a filename (str), pathlib.Path
                object or a file object. The file object must implement
                read(), seek(), and tell() methods, and be opened in
                binary mode.
        """
        if not isinstance(file_path_name, Image.Image):
            image = _convert_to_monochrome_image(file_path_name, is_resize=True)
            logging.debug('------Detecting QR Code------')
        else:
            image = file_path_name

            logging.debug('------Scanning QR Code------')

        self.__image = image
        self.__position_detection_patterns = _find_outer_pattern(self.__image)
        self.__qr_image = image
        self.__bit_matrix = None
        self.__info = None
        self.__all_data_matrix = None


    @property
    def image(self):
        """PIL.Image obj: Represent image object"""
        return self.__image

    @property
    def qr_image(self):
        """PIL.Image obj: Represent image obj of the QR code"""
        return self.__qr_image

    @property
    def info(self):
        """QRCodeInfo obj: Represent function patterns of symbol"""
        return self.__info

    @property
    def bit_matrix(self):
        """numpy array: Represent a bit(module) matrix of QR code"""
        return self.__bit_matrix

    @property
    def data_matrix(self):
        """numpy array: Represent a data matrix which was released masking) of
            QR code"""
        return self.__all_data_matrix

    @info.setter
    def info(self, information):
        self.__info = information
        return information


    def find_qr_codes(self):
        """Find QR Code from provided image `file_path_name`

        Arguments: file_path_name (str): file name path of the image

        Returns: PIL.Image: object PIL.Image of only QR Code
        """

        pattern_tuple = self.__position_detection_patterns

        # Crop QR code
        self.__qr_image = crop_qr_code_image(self.__image, pattern_tuple)

        # Update position detection patterns
        new_outer_patterns = _update_new_outer_patterns(self.__image, pattern_tuple)
        self.__position_detection_patterns = new_outer_patterns

        return self.__qr_image


    # @staticmethod
    # def test(image):
    #     position_detection_patterns = _find_outer_pattern(image)
    #     return position_detection_patterns

    # Waypoint 11: Find QR Code Symbol Version
    def find_qr_code_version(self):
        """Find QR Code version

        Returns:
            (tuple) a tuple of two integers (version, width)
                corresponding respectively to the version of
                this QR code symbol and the number of modules
                (on one row of the QR code symbol).
        """
        qr_info = self._get_object_qr_symbol()
        return qr_info.version, qr_info.qr_width


    # Waypoint 12: Convert a QR Code Symbol to an Array of Bits
    def convert_qr_code_to_bit_array(self):
        """Convert a QR Code Symbol to an Array of Bits

        Returns:
            (list) -- returns an array of integers 0 and 1 representing
                the modules of the QR code symbol.
        """

        # Find version, width and module size of qr code
        if self.__info is None:
            qr_info = self._get_object_qr_symbol()

        # Resize the image to qr code 's width
        resized_image = self.qr_image.resize((qr_info.qr_width, qr_info.qr_width))

        # Initialize array of zeros to store modules
        self.__bit_matrix = np.zeros(
            (qr_info.qr_width, qr_info.qr_width), dtype=np.int)

        # Get an array of colors of the qr_code image which was resized
        arr = np.array(resized_image, dtype=np.int)

        # Change values: A module with a dark area corresponds to the bit 1,
        # while module with a light area corresponds to the bit 0
        self.__bit_matrix[arr == WHITE] = BLACK

        return self.__bit_matrix


    # Calculate module size (the number of pixels of one edge of the module)
    def _get_module_size(self):

        # Calculate vesion and al X dimension of the symbol
        upper_left = self.__position_detection_patterns[0]
        upper_right = self.__position_detection_patterns[1]

        # The number of pixels of each module
        module_size = (
            upper_left.height + upper_right.height
            + self.__position_detection_patterns[2].height) / (3 * PATTERN_SIZE)

        return round(module_size)

    # Calculate version of QR code, then return object QRCodeInfo
    def _get_object_qr_symbol(self):
        # Calculate vesion and al X dimension of the symbol
        upper_left = self.__position_detection_patterns[0]
        upper_right = self.__position_detection_patterns[1]
        module_size = self._get_module_size()

        # calculate distance_between_two_centers_of_upper_left_and_upper_right
        distance = _calculate_distance_between_two_points(
            upper_left.centroid[0], upper_right.centroid[0],
            upper_left.centroid[1], upper_right.centroid[1])

        # Define version
        version = round(((distance / module_size) - 10) / 4)
        # Create ofject QRCodeInfo
        qr_info = QRCodeInfo(version)

        return qr_info

    # Read information to update mask id and EC level of the info object
    # Return QRCodeInfo which is updated mask_id and ec_level
    def _update_qr_code_info(self):

        # Get bit matrix
        if self.__bit_matrix is None:
            self.__bit_matrix = self.convert_qr_code_to_bit_array()

        # Get info object
        if self.__info is None:
            self.info = self._get_object_qr_symbol()

        # Update mask id and EC level of the object `QRCodeInfo`
        # then update the attribute `info` of the `QRCodeImage`
        self.info.read_format_information(self.__bit_matrix)

        return self.__info

    @staticmethod
    # Return the mask function of the provided mask pattern.
    def _define_type_of_masking(mask_id):
        # (i, j) refers to (row, col)
        # (i, j) = (0, 0) for the top left module in the symbol.
        #  Mask Pattern
        #    id   |   Reference |   # Condition
        #    0    |   000       |   # (i + j) mod 2 = 0
        #    1    |   001       |   # i mod 2 = 0
        #    2    |   010       |   # j mod 3 = 0
        #    3    |   011       |   # (i + j) mod 3 = 0
        #    4    |   100       |   # ((i div 2) + (j div 3)) mod 2 = 0
        #    5    |   101       |   # (i j) mod 2 + (i j) mod 3 = 0
        #    6    |   110       |   # ((i j) mod 2 + (i j) mod 3) mod 2 = 0
        #    7    |   111       |   # ((i j) mod 3 + (i+j) mod 2) mod 2 = 0

        mask_funcs = {
            0: lambda i, j: (i + j) % 2 == 0,
            1: lambda i, j: i % 2 == 0,
            2: lambda i, j: j % 3 == 0,
            3: lambda i, j: (i + j) % 3 == 0,
            4: lambda i, j: (i // 2 + j // 3) % 2 == 0,
            5: lambda i, j: (i * j) % 2 + (i * j) % 3 == 0,
            6: lambda i, j: ((i * j) % 2 + (i * j) % 3) % 2 == 0,
            7: lambda i, j: ((i * j) % 3 + (i + j) % 2) % 2 == 0,
        }
        return mask_funcs[mask_id]

    # Get mask matrix
    def _get_mask_matrix(self):

        # Make sure all information of the function patterns of QR code
        # was updated
        self._update_qr_code_info()

        # Init an mask array
        mask_matrix = np.zeros(
            (self.info.qr_width, self.info.qr_width), dtype=np.int)

        # Define type of mask of the QR code
        mask_func = self._define_type_of_masking(self.info.mask_id)

        # Modify elements based of type of masking
        for i in range(self.info.qr_width):
            for j in range(self.info.qr_width):
                if mask_func(j, i):
                    mask_matrix[j, i] = 1

        return mask_matrix

    def get_data_matrix(self):
        """ Returns: (numpy array): an data array which is unmasked"""
        # Get mask matrix
        mask_matrix = self._get_mask_matrix()

        # Unmask the data matrix
        self.__all_data_matrix = self.__bit_matrix - mask_matrix
        self.__all_data_matrix[self.__all_data_matrix == -1] = 1

        return self.__all_data_matrix

    @staticmethod
    # Define areas which are useless to decode
    # Returns a list of coordinates of zone
    # Note: Function patterns:
        # * Position Detection Patterns
        # * Seperators for Position Detection Patterns
        # * Timming Patterns
        # * Alignment position
    def _define_function_patterns(version, qr_width):
        # Define zone (x1, y1, x2, y2) as a rectangle with topleft(x1, y1)
        # and bottom-right(x2, y2). All points in zone will be considered as
        # useless points to decode
        garbage_for_decode_zone = [
            # upper left position + Seperators + format info
            (0, 0, 8, 8),
            # upper right position + Seperators + format info
            (qr_width - 8, 0, qr_width - 1, 8),
            # lower left position + Seperators + format info
            (0, qr_width - 8, 8, qr_width - 1),
            # Timing Patterns
            (6, 9, 6, qr_width - 9),
            (9, 6, qr_width - 9, 6)
        ]
        # Get coordinates of alignment patterns
        alignments_zones = []
        center_alignment_pattern = list(
            itertools.permutations(ALIGNMENT_POSITIONS[version - 1], 2))
        center_alignment_pattern.extend(
            (x, x) for x in ALIGNMENT_POSITIONS[version - 1])

        # Defint alignment zone (top-left and bottom-right)
        for center_x, center_y in center_alignment_pattern:
            alignment_zone = (center_x - 2, center_y - 2, center_x + 2, center_y + 2)
        alignments_zones.append(alignment_zone)

        func_patterns_zone = garbage_for_decode_zone + alignments_zones
        # Get coordinates
        function_patterns_coordinates = [
            (x, y) for zone in func_patterns_zone
            for x in range(zone[0], zone[2] + 1)
            for y in range(zone[1], zone[3] + 1)
            ]

        return list(set(function_patterns_coordinates))


    def get_data_and_error_correction_area(self):
        """Get data and error correction areas which are excluded
            function_patterns_coordinates zone

        Returns: a list of bit represent data and error correction
        """
        # Get function patterns coordinates list
        function_patterns_coordinates = self._define_function_patterns(
            self.info.version, self.info.qr_width)

        # Get the first element to Iterate ZigZag
        start_point = ((self.info.qr_width - 1), (self.info.qr_width - 1))

        # Get array data and error correction coordinates, then map it
        # to get a bit array which is excluded the useless zone
        data_coordinates = _get_data_and_error_correction_area_coordinaters(
            start_point, self.info.qr_width)
        coordinates = np.array(
            [tup for tup in data_coordinates \
                if tup not in function_patterns_coordinates])
        all_data = self.__all_data_matrix[tuple(coordinates.T)]

        return all_data
