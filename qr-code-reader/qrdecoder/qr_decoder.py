#!/usr/bin/env python3
"""QR Code Decoder In Pure Python"""
from qrdecoder.constant import ENCODING_LEN
from qrdecoder.utils import _convert_binary_to_character

class QRCodeDecoder:
    """Class QRCodeDecoder represent real data of a QR Code Image """
    def __init__(self, encoding_region):
        """The constructor of QRCodeDecoder

        Parameters:
            encoding_region (numpy.array): represent a bit array which
                contains data and error correction
        """
        encoding_mode = None
        data_and_error_area = None
        data_len = None

        # Get encoding mode as binary 4 bit
        encoding_mode = ''.join(str(char) for char in \
            encoding_region[:ENCODING_LEN])
        self.__encoding_mode = encoding_mode

        # Get data and error correction area
        data_and_error_area = encoding_region[(ENCODING_LEN + 8):]
        self.__data_and_error_area = data_and_error_area

        # Len of the provided data
        data_len = int(''.join(str(char) for char in \
            encoding_region[ENCODING_LEN:ENCODING_LEN + 8]), 2)
        self.__data_len = data_len


    @property
    def encoding_mode(self):
        """str: 4 bit Represent encoding mode of provided QR"""
        return self.__encoding_mode

    @property
    def data_and_error_area(self):
        """(np.array): represent a bit array which contains data
            and error correction """
        return self.__data_and_error_area

    @property
    def data_len(self):
        """(int): represent len of provided data"""
        return self.__data_len


    def decode_qr_code_from_array(self):
        """Decode QR Code """
        string_data = ''
        string_error = ''
        # # Get encoding mode as binary 4 bit
        bit_length = self.data_len * 8
        data_area = self.__data_and_error_area[0:bit_length]
        error_area = self.__data_and_error_area[(bit_length+4):]

        for i in range(0, len(data_area), 8):
            binary_list = self.__data_and_error_area[i:i+8]
            char = _convert_binary_to_character(binary_list)
            string_data += char

        for i in range(0, len(error_area), 8):
            binary_list = error_area[i:i+8]
            char = _convert_binary_to_character(binary_list)
            string_error += char

        return string_data
