from PIL import Image
import argparse
from os.path import join, basename, splitext, dirname
from validate import (check_image_file_exists, check_sizes_args,
                      validate_optional_args, check_output_path,
                      MIN_SIZE_VALUE, MAX_SIZE_VALUE)


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
        metavar="must be int between {} and {}".format(
            MIN_SIZE_VALUE,
            MAX_SIZE_VALUE
        )
    )
    parser.add_argument(
        "-height",
        type=check_sizes_args,
        metavar="must be int between {} and {}".format(
            MIN_SIZE_VALUE,
            MAX_SIZE_VALUE
        )
    )
    parser.add_argument(
        "-scale",
        type=float,
        metavar="must be a float value"
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


def get_sides_size(
        image,
        width=None,
        height=None,
        scale=None
):
    original_width, original_height = image.size
    if width and height:
        sides_size = (width, height)
    elif width:
        height = int(round(original_height / (original_width / width)))
        sides_size = (width, height)
    elif height:
        width = int(round(original_width / (original_height / height)))
        sides_size = (width, height)
    elif scale:
        sides_size = tuple([int(round(scale * size)) for size in
                            (original_width, original_height)])
        if any(size not in range(MIN_SIZE_VALUE, MAX_SIZE_VALUE)
               for size in sides_size):
            raise ValueError("The scale value {} is invalid!\n"
                             "The height or width, couldn't be less"
                             " {} and larger then {}!".format(
                                scale,
                                MIN_SIZE_VALUE,
                                MAX_SIZE_VALUE
                             ))
    else:
        return False
    return sides_size


def make_args_for_resize(
        path_to_source_image,
        output_image_path=None,
        width=None,
        height=None,
        scale=None
):
    original_image = open_image(path_to_source_image)
    sides_size = get_sides_size(original_image, width, height, scale)
    output = get_output_file_path(
        path_to_source_image,
        sides_size,
        output_image_path
    )
    return original_image, sides_size, output


def resize_image(image, sides_size):
    resized_image = image.resize(sides_size)
    close_image(image)
    return resized_image


def save_resize_image(image, output):
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
        original_image, sides_size, path_to_resize = make_args_for_resize(
            path_to_source_image,
            output,
            width,
            height,
            scale
        )
        new_image = resize_image(original_image, sides_size)
        save_resize_image(new_image, path_to_resize)
        print("Ok! The new file - '{}'".format(path_to_resize))
    except PermissionError:
        exit("You don't have permission to save into the"
             " '{}' directory".format(output))
    except IOError:
        exit("The source image file {} "
             "is invalid image file!".format(path_to_source_image))
    except ValueError as error:
        ext_msg = error.args[0]
        exit(ext_msg)
