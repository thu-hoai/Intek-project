#!/usr/bin/env python3
"""Testing for QR CODE DETECTOR project"""
from PIL import ImageDraw, Image
import time
import random
import pprint
from qrdecoder.qr_finder import *
from qrdecoder.qr_finder import (_calculate_min_surface, _get_sprites_object,
    _update_new_outer_patterns, _convert_to_monochrome_image)
from qrdecoder.constant import SIMILAR_SIZE_THRESHOLD


def test_create_bounding_box(image, sprites, background_color=(255, 255, 255)):
    """For check bounding box"""
    width = image.width
    height = image.height
    # Create a image to draw all sprite sheets
    new_sprite_sheet = Image.new(
        "RGB", (width, height), background_color)
    draw = ImageDraw.Draw(new_sprite_sheet)
    sprite_color = tuple([random.randint(0, 100) for _ in range(0, 3)])
    for sprite in sprites:
        top_left_coordinate = sprite.top_left
        bottom_right_coordinate = sprite.bottom_right
        draw.rectangle([top_left_coordinate,
                        bottom_right_coordinate],
                        outline=sprite_color)
    return new_sprite_sheet

def draw_line_3_points(im, a, b, c):
    """
    im
    a, b, c: 3 tuple"""
    line_color = tuple([random.randint(0, 255) for _ in range(0, 3)])
    line1 = ImageDraw.Draw(im)
    line1.line([a, b], fill=line_color)

    line2 = ImageDraw.Draw(im)
    line2.line([c, b], fill=line_color)

    return im

def test(file_path_name):
    #----------- test for wp01-7--------------
    image = _convert_to_monochrome_image(file_path_name)
    logging.info("Size of the image %s", image.size)

    sprites = _get_sprites_object(image)
    min_surface = _calculate_min_surface(image)


    #-------- Test for wp04 -----------------------
    visible_sprites = filter_visible_sprites(sprites,
        min_surface_area=min_surface)
    logging.info("The number of visible sprites %s, min_surface %s",
        len(visible_sprites), min_surface)
    # im = test_create_bounding_box(image, visible_sprites)
    # im.show()

    # --------Test for wp05--------------------------
    square_sprites = filter_square_sprites(visible_sprites)
    logging.info(" The number of square sprites: %s",
        len(square_sprites))
    # im = test_create_bounding_box(image, square_sprites)
    # im.show()

    #---------Test for wp06-----------------------------
    dense_sprites = filter_dense_sprites(square_sprites)
    logging.info("The number of dense sprites: %s",
        len(dense_sprites))
    # im = test_create_bounding_box(image, dense_sprites)
    # im.show()

    # --------Test for wp07-----------------------------
    # # Test similar size
    similar_size_groups = group_sprites_by_similar_size(dense_sprites, SIMILAR_SIZE_THRESHOLD)
    for group in similar_size_groups.values():
        print(len(group))
        im = test_create_bounding_box(image, group)
        im.show()

    # Test similar distance
    similar_groups = group_sprites_by_similar_size_and_distance(dense_sprites)
    # for similar_group in similar_groups:
    #     for pair in similar_group:
    #         position_pattern = list(set(pair[0]) | set(pair[1]))
    #         im = test_create_bounding_box(image, position_pattern)
    #         # Define upper_left_sprite by union two set of pairs
    #         upper_left_sprite = list(set(pair[0]) & set(pair[1]))[0]
    #         # upper_right_sprite, lower_left_sprite arbitrarily chosen
    #         upper_right_sprite = list(set(pair[0]) - set(pair[1]))[0]
    #         lower_left_sprite = list(set(pair[1]) - set(pair[0]))[0]

    #         im = draw_line_3_points(im,
    #         upper_right_sprite.centroid,
    #         upper_left_sprite.centroid,
    #         lower_left_sprite.centroid)
    #         im.show()
    #         print("the number of pairs", len(similar_group))
    # for similar_group in similar_groups:
    #     for i in similar_group:
    #         x = list(set(i[0]) | set(i[1]))
    #         # print(x)
    #         im = test_create_bounding_box(image, x)
    #         im.show()
    #     print("the number of pairs", len(similar_group))


    # # ------------Test for wp08------------------------------------------
    count = 0
    pattens_list = []
    draft = []
    for similar_group in similar_groups:
        position_patterns = search_position_detection_patterns(similar_group)
        for position_pattern in position_patterns:
            count += 1
            pattens_list.append(position_pattern)
            # im = test_create_bounding_box(image, [position_pattern[2]])
            # im.show()
            # im = test_create_bounding_box(image, list(position_pattern))
            # logging.info("""upper_left_sprite: %s,
            #     upper_right_sprite %s, lower_left_sprite %s""",
            #         position_pattern[0].centroid,
            #         position_pattern[1].centroid,
            #         position_pattern[2].centroid)
            # im = draw_line_3_points(im,
            #     position_pattern[2].centroid,
            #     position_pattern[0].centroid,
            #     position_pattern[1].centroid)
            # im.show()

            # Test for cases co qua nhieu pair found
            for i in position_pattern:
                draft.append(i)
    logging.info("Found %s pairs sprites", count)
    im = test_create_bounding_box(image, list(draft))
    im.show()

    # #-------------test for wp09------------------------
    outer_pattern = filter_matching_inner_outer_finder_patterns(pattens_list)
    logging.info("Found %s pattern", outer_pattern)
    im = test_create_bounding_box(image, list(outer_pattern))
    im.show()
    pattern_tuple = _update_new_outer_patterns(
        image, outer_pattern)
    # image.show()

    # # --------------test for wp10 ------------------------
    im = crop_qr_code_image(image, pattern_tuple)
    im.show()

    return im



def main():
    """Demonstrate and run test cases"""
    # Other tests
    image_list = [
    'qr_code_intek_edu_vn_fancy.png', #0
    '20190910_162611.jpg', #1
    './samples/20190820_114211.jpg', #2
    './samples/20190820_114223.jpg', #3
    './samples/20190820_114251.jpg', #4
    './samples/20190820_114302.jpg', #5
    './samples/20190820_114158.jpg', #6
    './samples/20190820_114118.jpg', #7
    './samples/20190820_114057.jpg', #8
    'test8.png', #9
    'test9.png', #10
    './samples/20190820_114029.jpg', #11
    './samples/20190820_114009.jpg', #12
    "qr_code.jpg", #13
    "thumbnail.jpg" #14
    ]
    file_path_name = image_list[5]
    start = time.time()
    test(file_path_name)
    stop = time.time()
    logging.info(stop-start)

    # for file_path_name in image_list:
    #     start = time.time()
    #     test(file_path_name)
    #     stop = time.time()
    #     logging.info(stop-start)

if __name__ == "__main__":
    main()

