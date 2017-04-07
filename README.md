#Jigsaw Puzzle Building Robot With CNC Approach

###Prerequisites

* [Python 2.7.X](https://www.python.org/ftp/python/2.7.13/python-2.7.13.msi)
* [Numpy 1.7.X](http://sourceforge.net/projects/numpy/files/NumPy/1.7.1/numpy-1.7.1-win32-superpack-python2.7.exe/download)
* [OpenCV-Python 2.X](https://sourceforge.net/projects/opencvlibrary/files/opencv-win/2.4.13/opencv-2.4.13.exe/download)

A useful introduction to the project's underlying libraries can be found [here](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_setup/py_table_of_contents_setup/py_table_of_contents_setup.html#py-table-of-content-setup).


###INTRODUCTION

This readme serves as a brief guide to the operation of the CNC Jigsaw Puzzle Building Robot at the University of Pretoria. This robot, along with all its hardware, software, and firmware components, was designed, developed, and built from first principals, by J.P. Strydom for his final year project. This project, along with its supporting documentation, served as the final deliverable to obtain a Bachelors in Computer Engineering. 

The project's YouTube video playlist is available [here](https://www.youtube.com/playlist?list=PL-dF5vEAX-wXbiRrD7gLAtIBlyCBS7HLN).


###BRIEF SOFTWARE DESCRIPTION

A link to the software folder can be found [here](code/software/).

* _**`Folders`**_ - All folders and sub-folders in the *`code/software/`* directory should be present at execution time, else execution will be unsuccessful.
* **`Classes.py`** - This file contains the definition and implementation of the `Puzzle` and `Puzzle_Piece` classes.
* **`Functions_1.py`** - This file contains the piece detection and piece classification code.
* **`Functions_2.py`** - This file contains the puzzle solving code.
* **`Functions_3.py`** - This file contains the construction command generation code.
* **`Puzzle_Solver_UI.py`** - This file contains the system controller and GUI code. Executing this file will run the entire system.
* **`Simulation_Platform.py`** - This file contains the simulation platform code. Executing this file allows users to test the functionality of the entire software system, including the digital camera, independently.
* **`Simulation_Platform_[Image].py`** - This file contains the code for the image simulation platform. This file functions identically to the `Simulation_Platform.py` file, except that it uses an image other than the digital camera input. This image should be labelled `original.png` and should be located in the *`code/software/images/`* directory. Eight example images have been provided in the aforementioned folder. (***Note**: This file is particularly useful if users are only interested in the image processing and puzzle-solving aspect of the project*).
* **`software-simulation-platform-controls.pdf`** -  This file shows the commands for controlling the simulation platform files.


###SETUP

The digital camera should have at least a 720p resolution (1280 by 720). The camera interface index can be configured on *lines 15* and *18* in the `Puzzle_Solver_UI.py` file, and on *line 14* in the `Simulation_Platform.py` file. When running the `Simulation_Platform.py` file, the unaltered camera output should look as similar as possible to the example images provided in the [*`code/software/images/`*](code/software/images) directory (`original.png` to `original-7.png`). Example camera setup photos can be found in the [*`images/photos/`*](images/photos) directory (`layout-1.jpg` and `layout-2.jpg`).

In order to interface with the hardware unit, it has to be linked with a computer housing the software unit, via a serial-to-USB cable. The COM port number can be configured on *lines 24* and *27* in the `Puzzle_Solver_UI.py` file.


###DEBUGGING

The `Classes.py`, `Functions_1.py`, `Functions_2.py`, and `Functions_3.py` files each have debugging boolean variables labelled `DEBUG_xxxxxx`, where `xxxxxx` represents the specific debugging feature. These variables are all found near the top of their respective files and their functionality is described in code. Setting these variables to true will enable their corresponding debugging features, and vice versa.


###CALIBRATION
  
Throughout the code, there are calibration dependant variables. These variables are preceded by a comment line which starts with multiple `#` characters (which makes them easy to locate), and these lines each end with a `[Calibration Values]` tag. Two examples of such calibration variable sets are shown below.

```python
##### Upper and lower HSV colour boundaries for corner markers [Calibration Values]
    corner_lower_PT = np.array([100, 0, 155], dtype = "uint8")
    corner_upper_PT = np.array([170, 100, 255], dtype = "uint8") 
```

```python
##### Min and Max piece parameters [Calibration Values]
    piece_min_area = 15000 
    piece_max_area = 22000 
    overlap_max_area = 3*piece_max_area
    min_wh_ratio = 0.575
    max_wh_ratio = 1.75
    min_wh_ratio_overlap = 0.2
    max_wh_ratio_overlap = 3.6
```

These variables pertain to aspects such as puzzle parameters and gantry specifications, and many of them can be found by utilising the debug tools, as described above, along with the software simulation platform.

As it stands, all the system`s calibration values have been configured for the current gantry setup and the puzzles accompanying this digital documentation package.
# Jigsaw-Puzzle-Building-Robot
