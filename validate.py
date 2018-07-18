from argparse import ArgumentTypeError
from os.path import exists, isfile, isdir, splitext
from PIL import Image


def check_image_file(path_to_source_file):
    if not exists(path_to_source_file):
        msg_exist = ("No such file or directory"
                     " - '{}' !".format(path_to_source_file))
        raise ArgumentTypeError(msg_exist)
    elif not isfile(path_to_source_file):
        msg_isdir = "'{}' is not a file".format(path_to_source_file)
        raise ArgumentTypeError(msg_isdir)
    elif not check_file_extension((".jpg", ".png"), path_to_source_file):
        raise ArgumentTypeError("The source image file {} is invalid!\n"
                                "The valid file extensions are {}".format(
                                 path_to_source_file,
                                 (".jpg", ".png")))
    elif not check_file_consistent(path_to_source_file):
        raise ArgumentTypeError("The source image file {} "
                                "is invalid".format(path_to_source_file))
    return path_to_source_file


def check_file_extension(extensions, path_to_source_file):
    file_name, file_extension = splitext(path_to_source_file)
    return file_extension in extensions


def check_file_consistent(path_to_source_file):
    try:
        with Image.open(path_to_source_file):
            return True
    except OSError:
        return False


def check_sizes_args(arg):
    if int(arg) <= 0:
        raise ArgumentTypeError("argument must be a positive!")
    return int(arg)


def check_scale_arg(arg):
    if float(arg) <= 0:
        raise ArgumentTypeError("argument must be a positive!")
    return float(arg)


def is_check_sizes_ratio_change(original_size, new_size):
    original_width, original_height = original_size
    new_width, new_height = new_size
    return original_width/original_height != new_width/new_height


def validate_optional_args(args):
    if args.scale is not None:
        if args.width or args.height:
            return("You can not specify scale with "
                   "height or width the same time! ")
    if not args.width and not args.height and not args.scale:
        return("You didn't specify "
               "any optional parameter!\n"
               "Run image_resize.py -h to read script usage."
               )
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
    return output


if __name__ == "__main__":
    pass
