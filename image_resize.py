from PIL import Image
import argparse
from argparse import ArgumentTypeError
from os.path import (exists, isfile, join,
                     basename, splitext, dirname, isdir)

MIN_SIZE_VALUE = 1
MAX_SIZE_VALUE = 16383


def check_image_file_exists(path_to_source_file):
    if not exists(path_to_source_file):
        msg_exist = ("No such file or directory"
                     " - '{}' !".format(path_to_source_file))
        raise ArgumentTypeError(msg_exist)
    elif not isfile(path_to_source_file):
        msg_isdir = "'{}' is not a file".format(path_to_source_file)
        raise ArgumentTypeError(msg_isdir)
    else:
        return path_to_source_file


def check_sizes_args(arg):
    if int(arg) not in range(MIN_SIZE_VALUE, MAX_SIZE_VALUE):
        raise ArgumentTypeError("argument must be in range({}, {})".format(
            MIN_SIZE_VALUE,
            MAX_SIZE_VALUE
        ))
    return int(arg)


def validate_optional_args(width=None, height=None, scale=None):
    if scale is not None:
        if width or height:
            raise SyntaxError("You can not specify scale with "
                              "height or width the same time! ")
    elif width and height:
        print("You have specified width and height."
              "The aspect ratio will be changed!")
    if not width and not height and not scale:
        raise SyntaxError("You didn't specify "
                          "any optional parameter!\nRun {} -h "
                          "to read script usage.".format(__file__))
    return True


def check_output_path(output):
    output_dir = output
    if not exists(output_dir):
        msg_exist = ("No such file or directory - "
                     "'{}' !".format(output_dir))
        raise ArgumentTypeError(msg_exist)
    elif not isdir(output_dir):
        msg_isdir = "'{}' is not a directory".format(output_dir)
        raise ArgumentTypeError(msg_isdir)
    else:
        return output


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
            raise ValueError
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
    except ValueError:
        exit("The scale value {} is invalid!\nThe height or width,"
             " couldn't be less {} and larger then {}!".format(
              scale,
              MIN_SIZE_VALUE,
              MAX_SIZE_VALUE
              ))
    except SyntaxError as error:
        ext_msg = error.args[0]
        exit(ext_msg)
