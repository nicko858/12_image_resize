from argparse import ArgumentTypeError
from os.path import exists, isfile, isdir


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
            raise ValueError("You can not specify scale with "
                             "height or width the same time! ")
    elif width and height:
        print("You have specified width and height."
              "The aspect ratio will be changed!")
    if not width and not height and not scale:
        raise ValueError("You didn't specify "
                         "any optional parameter!\n"
                         "Run image_resize.py -h to read script usage.")
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
