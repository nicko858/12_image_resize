# Image Resizer

The program is represented by the module ```image_resize.py```.
Module ```image_resize.py``` contains the following functions:

- ```check_image()```
- ```check_optional_args()```
- ```check_output_path()```
- ```check_positive()```
- ```get_args()```
- ```get_img_file_size()```
- ```get_max_size()```
- ```get_output_file_path()```
- ```resize_image()```

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

In case of wrong directory or invalid image file, you'll see error messages:<br/>

```You don't have permission to save into the '/' directory```<br/>
or <br/>
```The source image file is invalid!```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
