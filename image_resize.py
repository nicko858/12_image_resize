from PIL import Image
import argparse
from argparse import ArgumentTypeError
from os.path import (exists, isfile,
                     basename, splitext, dirname, isdir)


def check_image(source_file):
    if not exists(source_file):
        msg_exist = ("No such file or directory"
                     " - '{}' !".format(source_file))
        raise ArgumentTypeError(msg_exist)
    elif not isfile(source_file):
        msg_isdir = "'{}' is not a file".format(source_file)
        raise ArgumentTypeError(msg_isdir)
    else:
        return source_file


def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise ArgumentTypeError("{} is an invalid value! "
                                "It must be positive!".format(value))
    return ivalue


def check_optional_args(width=None, height=None, scale=None):
    msg_error = ("You can not specify scale with height or width "
                 "the same time! ")
    if scale:
        if width or height:
            return msg_error
    return "Ok"


def check_output_path(output):
    output_dir = dirname(output)
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
    script_usage = """python image_resize.py 
                       Mandatory parameter:
                       -source_image <path to source image>
    
                       Optional parameters:
                       -width <value>
                       -height <value>
                       -scale <value>
                       -output <path to resize file>"""
    parser = argparse.ArgumentParser(
        description="How to run image_resize.py:",
        usage=script_usage
    )
    parser.add_argument(
        "source_image",
        type=check_image
    )

    parser.add_argument(
        "-width",
        type=check_positive
    )
    parser.add_argument(
        "-height",
        type=check_positive
    )
    parser.add_argument(
        "-scale",
        type=check_positive
    )
    parser.add_argument(
        "-output",
        type=check_output_path
    )

    args = parser.parse_args()
    return args


def get_img_file_size(source_image):
    with Image.open(source_image) as im:
        width, height = im.size
    return width, height


def get_output_file_path(source_image, size, output=None):
    width, height = size
    source_file_name = basename(source_image)
    file_name, file_extension = splitext(source_file_name)
    output_file_name = "{}__{}x{}{}".format(file_name,
                                            width,
                                            height,
                                            file_extension)
    if output:
        return "{}/{}".format(output, output_file_name)
    return "{}/{}".format(dirname(source_image), output_file_name)


def get_max_size(path_to_original,
                 width=None,
                 height=None):
    original_width, original_height = get_img_file_size(path_to_original)
    max_size = ()
    if width and height:
        max_size = (width, height)
    elif width:
        max_size = (width, original_height)
    elif height:
        max_size = (original_width, height)
    elif scale:
        max_size = tuple([scale * i for i in
                          (original_width, original_height)])
    return max_size


def resize_image(path_to_original,
                 output_image_path=None,
                 width=None,
                 height=None,
                 scale=None):
    max_size = get_max_size(path_to_original, width, height)
    with Image.open(path_to_original) as original_image:
        if scale or (width and height):
            resized_image = original_image.resize(max_size)
            image = resized_image
        else:
            original_image.thumbnail(max_size, Image.ANTIALIAS)
            image = original_image
        output = get_output_file_path(path_to_original,
                                      image.size,
                                      output_image_path)
        image.save(output)
    return output


if __name__ == "__main__":
    args = get_args()
    source_image = args.source_image
    width = args.width
    height = args.height
    scale = args.scale
    output = args.output
    validate_args = check_optional_args(width, height, scale)
    if validate_args is not "Ok":
        exit(validate_args)
    try:
        result_image = resize_image(source_image,
                                    output,
                                    width,
                                    height,
                                    scale)
        print("Ok! The new file - '{}'!".format(result_image))
    except PermissionError:
        exit("You don't have permission to save into the"
             " '{}' directory".format(output))
    except IOError:
        exit("The source image file is invalid!")