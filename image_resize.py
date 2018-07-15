from PIL import Image
import argparse
from argparse import ArgumentTypeError
from os.path import join, basename, splitext, dirname
from validate import (check_image_file_exists, check_sizes_args,
                      check_scale_arg, validate_optional_args,
                      check_output_path, check_sizes_ratio)


def get_args():
    parser = argparse.ArgumentParser(
        description="How to run image_resize.py:"
    )
    parser.add_argument(
        "path_to_source_image",
        type=check_image_file_exists
    )
    parser.add_argument(
        "-width",
        type=check_sizes_args,
        metavar="must be positive int"
    )
    parser.add_argument(
        "-height",
        type=check_sizes_args,
        metavar="must be positive int"
    )
    parser.add_argument(
        "-scale",
        type=check_scale_arg,
        metavar="must be a positive float"
    )
    parser.add_argument(
        "-output",
        type=check_output_path,
        metavar="specify the path where to save resized image"
    )

    args = parser.parse_args()
    return args


def open_image(path_to_source_image):
    image = Image.open(path_to_source_image)
    return image


def close_image(image):
    image.close()


def get_output_file_path(path_to_source_image, size, output=None):
    width, height = size
    source_file_name = basename(path_to_source_image)
    file_name, file_extension = splitext(source_file_name)
    output_file_name = "{}__{}x{}{}".format(
        file_name,
        width,
        height,
        file_extension
    )
    if output:
        return join(output, output_file_name)
    return join(dirname(path_to_source_image), output_file_name)


def calculate_sides_size(
    original_sides_size,
    width=None,
    height=None,
    scale=None
):
    original_width, original_height = original_sides_size
    if width and height:
        sides_size = (width, height)
    elif width:
        height = int(original_height / (original_width / width))
        sides_size = (width, height)
    elif height:
        width = int(original_width / (original_height / height))
        sides_size = (width, height)
    elif scale:
        sides_size = tuple([int(scale * size) for size in
                            (original_width, original_height)])
    else:
        return False
    return sides_size


def resize_image(image, sides_size):
    resized_image = image.resize(sides_size)
    return resized_image


def save_resized_image(image, output):
    image.save(output)
    return output


if __name__ == "__main__":
    args = get_args()
    path_to_source_image = args.path_to_source_image
    width = args.width
    height = args.height
    scale = args.scale
    output = args.output
    try:
        validate_args = validate_optional_args(width, height, scale)
        original_image = open_image(path_to_source_image)
        original_sides_size = original_image.size
        new_sides_size = calculate_sides_size(
            original_sides_size,
            width,
            height,
            scale
        )
        if not check_sizes_ratio(original_sides_size, new_sides_size):
            print("The aspect ratio will be changed!")
        path_to_resize = get_output_file_path(
            path_to_source_image,
            new_sides_size,
            output
        )
        new_image = resize_image(original_image, new_sides_size)
        save_resized_image(new_image, path_to_resize)
        close_image(original_image)
        print("Ok! The new file - '{}'".format(path_to_resize))
    except PermissionError:
        exit("You don't have permission to save into the"
             " '{}' directory".format(output))
    except IOError:
        exit("The source image file {} "
             "is invalid image file!".format(path_to_source_image))
    except ArgumentTypeError as error:
        ext_msg = error.args[0]
        exit(ext_msg)
