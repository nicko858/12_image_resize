# Image Resizer

The program is represented by the modules ```image_resize.py, validate.py```.
Module ```image_resize.py``` contains the following functions:

- ```close_image()```
- ```get_args()```
- ```get_output_file_path()```
- ```get_sides_size()```
- ```open_image()```
- ```resize_image()```
- ```save_resize_image()```

Module ```validate.py``` contains the following:

- ```check_image_file_exists()```
- ```check_output_path()```
- ```check_sizes_args()```
- ```check_scale_arg()```
- ```validate_optional_args()```

**The program uses these standart and third-party libraries:**

```python
PIL
argparse
os
```
**How in works:**<br/>
The program accepts an image and puts it with a new size to a specified directory.If user doesn't specify output directory, the program puts new image to same as source image directory.<br/><br/>
If only the width is specified, the height is considered to preserve the aspect ratio of the image. And vice versa. - If both width and height are specified - create this image. Display a warning in the console if the proportions do not match the original image.<br/><br/>
    If the scale is specified, the width and height can not be specified. Otherwise, no resize occurs and the script breaks with an understandable error.
    If no path is specified before the final file, the result is placed to same as source image directory. If the source file is called pic.jpg (100x200), then after the call to python image_resize.py -scale 2 pic.jpg the file pic__200x400.jpg should appear.<br/><br/>
**It has a mandatory argument:**<br/>
```source_image ```- the path to the original picture. <br/><br/>
**And a few optional:** 
- ```width ```- width of the resulting image 
- ```height ```- its height
- ```scale``` - how many times to increase the image (maybe less than 1) 
- ```output``` - where to put the resulting file. 


# How to Install

Python 3 should be already installed. Then use pip (or pip3 if there is a conflict with old Python 2 setup) to install dependencies:

```bash
pip install -r requirements.txt # alternatively try pip3
```

Remember, it is recommended to use [virtualenv/venv](https://devman.org/encyclopedia/pip/pip_virtualenv/) for better isolation.

# How to run
- Activate virtualenv
``` bash
source <path_to_virtualenv>/bin/activate
```
- Run script with virtualenv-interpreter
```bash
<path_to_virtualenv>/bin/python3.5 image_resize.py <path_to_image> -height 170 
```
If everything is fine, you'll see such output:<br/><br/>
```Ok! The new file - '/home/nicko/devman//profit__170x170.png'!```

**The script will not run in the cases below:**

- In case of wrong directory or invalid image file, you'll see error messages:
```You don't have permission to save into the '/' directory```
  or 
```The source image file /home/nicko/devman/12_image_resize/batman.txt is invalid image file!```
- In case of bad scale value you'll see this error message:
``` image_resize.py: error: argument -scale: argument must be a positive!```
- In case of bad width or height value you'll see this error message:
``` image_resize.py: error: argument -height: argument must be a positive!```
- If you didn't specify any optional argumets, you'll see error-message:
```You didn't specify any optional parameter!```
```Run image_resize.py -h to read script usage.```
- The script doesn't allow to specify scale with height or width:
```You can not specify scale with height or width the same time! ```
# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
