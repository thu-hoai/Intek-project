#!/usr/bin/env python3
"""Exception of QR Code"""

class QRSymbolInfoException(Exception):
    """An exception specific to QRSymbolInfo"""

class QRDecoderException(Exception):
    """An exception specific to QRDecoder"""


class NoMaskIdException(QRSymbolInfoException):
    """An exception specific to format infor"""


class NotCorrectVersionException(QRSymbolInfoException):
    """An exception specific to format infor"""


class NotCorrectEncodingModeException(QRDecoderException):
    """An exception specific to Encoding Mode"""
