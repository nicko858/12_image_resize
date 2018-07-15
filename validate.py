from argparse import ArgumentTypeError, ArgumentError
from os.path import exists, isfile, isdir


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
    if int(arg) <= 0:
        raise ArgumentTypeError("argument must be a positive!")
    return int(arg)


def check_scale_arg(arg):
    if float(arg) <= 0:
        raise ArgumentTypeError("argument must be a positive!")
    return float(arg)


def check_sizes_ratio(original_size, new_size):
    original_width, original_height = original_size
    new_width, new_height = new_size
    if original_width/original_height != new_width/new_height:
        return False
    return True


def validate_optional_args(width=None, height=None, scale=None):
    if scale is not None:
        if width or height:
            raise ArgumentTypeError("You can not specify scale with "
                                    "height or width the same time! ")
    if not width and not height and not scale:
        raise ArgumentTypeError(
            "You didn't specify "
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
    else:
        return output


if __name__ == "__main__":
    pass
