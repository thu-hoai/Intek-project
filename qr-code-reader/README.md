# QR Code Reader

## Description
---

### What is a QR Code?

A [Quick Response (QR) code](https://en.wikipedia.org/wiki/QR_code) is two-dimensional [**barcode**](https://en.wikipedia.org/wiki/Barcode) first [designed in 1994](https://www.youtube.com/watch?v=LS1wrEv-fjk) for the automotive industry in Japan. A **barcode** is a machine-readable optical label that represents data.

A QR code consists of black squares arranged in a square grid on a white background, which can be read by any devices that have an embedded camera (QR code **scanner**), typically a smartphone. Data are then extracted from patterns that are present in both horizontal and vertical components of the image.


### Purposes the project
QR code finder and decoder in **pure Python**, without the help of any computer vision libraries. A **pure Python** library is a library that only contains Python code, and doesn't include, say, C extensions or code in other languages.

_Note: This **pure Python** implementation of a QR code finder and decoder is not intended to be used for real-time QR code decoding; it could take up to several seconds per image to detect and decode a QR code._

_Note:_ These functions support for:
- Photo Orientation and Brightness: consists in finding a form that looks like a QR code in an image, whatever its size, its orientation, or even its color.
- QR Code Detection. For example:
    ```python 3
    >>> from qrdecoder.qr_scanner import QRCodeImage
    >>> qr_code = QRCodeImage('./samples/20190820_114223.jpg')
    >>> im = qr_code.find_qr_codes()
    >>> im.show()
    ```
- QR Code Decoder
    Example for finding QR Code Symbol Information

    ```python 3
    >>> from qrdecoder.qr_decoder import QRCodeDecoder
    >>> from qrdecoder.qr_scanner import QRCodeImage
    >>> qr_code = QRCodeImage('./samples/20190820_114223.jpg')
    >>> im = qr_code.find_qr_codes()
    >>> qr_code3 = QRCodeImage(im)
    >>> qr_code3.get_data_matrix()
    >>> print(qr_code3.info)
    ```

## How to use
---
### Prerequisites
- Python3.6 + installation is required to get started (check by using `python3 --version`)
- Install python packages:
    - [spriteutils-pkg 2.0.1](https://pypi.org/project/spriteutils-pkg/)
    - Numpy
    - ExifRead 2.1.2
    - Pillow


### Usage
- Clone this repo to your local machine using `git@github.com:intek-training-jsc/qr-code-reader-hoaithu1.git`
- Run as below example

     ```python 3
    >>> from qrdecoder.qr_decoder import QRCodeDecoder
    >>> from qrdecoder.qr_scanner import QRCodeImage
    >>> qr_code = QRCodeImage('./samples/20190820_114223.jpg')
    >>> im = qr_code.find_qr_codes()
    >>> qr_code3 = QRCodeImage(im)
    >>> qr_code3.get_data_matrix()
    >>> data = qr_code3.get_data_and_error_correction_area()
    >>> decoder = QRCodeDecoder(data)
    >>> decoder.decode_qr_code_from_array()
    'https://intek.edu.vn'
     ```

## Support

Reach out to me (author)at the following place!

- Email at hoai.le@f4.intek.edu.vn
---

