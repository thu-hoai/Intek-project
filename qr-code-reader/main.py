import logging
import time
import pprint
from qrdecoder.qr_scanner import QRCodeImage
from qrdecoder.qr_decoder import QRCodeDecoder

def main():
    """Demonstrate and run test cases"""
    image_list = [
        # './samples/DSC07314.jpg',  # 0
        './samples/20190910_162611.jpg',  # 1
        './samples/20190820_114211.jpg',  # 2
        './samples/20190820_114223.jpg',  # 3
        './samples/20190820_114251.jpg',  # 4
        './samples/20190820_114302.jpg',  # 5
        './samples/20190820_114158.jpg',  # 6
        './samples/20190820_114118.jpg',  # 7
        './samples/20190820_114057.jpg',  # 8
        './samples/20190820_114029.jpg',  # 9
        './samples/20190820_114009.jpg',  # 10
        './samples/qr_code_intek_edu_vn_level_q.png',  # 11
        './samples/qr_code_intek_edu_vn_logo.png',  # 12
        './samples/qr_code_intek_edu_vn_level_m.png',  # 13
        './samples/test8.png',  # 14
        "./samples/testwp12.jpg" #15
    ]
    start = time.time()

    for i in range(len(image_list)):
        file_path_name = image_list[i]

        print(f"Processing {file_path_name}")
        qr_code = QRCodeImage(file_path_name)
        im = qr_code.find_qr_codes()
        im.show()

        qr_code3 = QRCodeImage(im)
        qr_code3.get_data_matrix()
        print(qr_code3.info)
        data = qr_code3.get_data_and_error_correction_area()
        decoder = QRCodeDecoder(data)
        print(decoder.decode_qr_code_from_array())

    stop = time.time()
    print(stop - start)
if __name__ == "__main__":
    main()


