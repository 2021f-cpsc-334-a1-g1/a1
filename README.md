# Assignment 1: Leeds Studio Projector Configuration System

## Overview

For this assignment, we were tasked with creating a program that would create a pixel configuration for the projector set up in Leeds Studio. This involved creating a mapping of the 6 projector screens pixel values to the physical space.

We chose to use Processing to develop the UI and store the pixel values in a JSON file upon completion of the user's mapping. Python was then used with various libraries (TODO: specify Python libraries). Below are further details about the UI, an explanation of the mapping of pixels to physical space, and a use case for these values in the form of a video processing module.

## Semi-Automatic Program: User Interface

In an attempt to align with the task's permission that the program could be semi-automatic, meaning requiring human input, we designed a User Interface in order to obtain the pixel to physical space mapping.

Through console prompts in the original Processing Sketch window, the user is instructed to click each of the available screens' top left and bottom right corner. These data points provide valuable information as they can be manipulated with each other to obtain each screen's height, width, and position.

The console also instructs the user to address the screens in order of left to right. In order to provide some clarity on this point, the number of the corresponding screen is displayed. For example, the far left screen will display 0, and the rightmost (in Leeds) will display 5.

After completing a screen by drawing its rectangle, the user must either press [y] to continue to the next rectangle or [n] to redraw the current rectangle in case of a mistake. The console reminds the user of these hotkeys throughout the workflow.

Finally, the user can press [s] to save the top left and bottom right corner pixel values to a JSON file when they finish mapping each screen and the screens display their corresponding numbers in ascending order from left to right.

### UI Demo in Leeds:
https://user-images.githubusercontent.com/57645852/133021774-980c5b18-9f20-4ac3-9738-62a9d3f2c837.mp4


## File Output: Pixels to Physical Space Mapping

In order to describe the pixel space to physical screen mapping, we labeled each physical screen with the pixel coordinates of its top left and bottom right corners. From these two points, it's possible to calculate the size and rotation of each screen. Since the user inputs these coordinates for each screen starting from left to right, the output file preserves this ordering of the screens.

These pixel coordinate values are stored in a JSON file (screen_coords.json) containing an array of objects, one for each screen. The order of screens in the array goes from left to right in physical space. Each screen object in the array contains the x and y pixel coordinates for the physical screen's top left and bottom right corners. So, for example, if a user wanted to display something on the leftmost screen, they would display content between the pixel coordinates stored at index 0 in the array. A sample trial on the Leeds room projectors led to the following results across the 6 screens, in JSON format:

[

  {
    "bottom_right_x": 9182,
    "bottom_right_y": 10,
    "top_left_y": 761,
    "top_left_x": 7831
  },
  
  {
    "bottom_right_x": 7814,
    "bottom_right_y": 8,
    "top_left_y": 760,
    "top_left_x": 6473
  },
  
  {
    "bottom_right_x": 6456,
    "bottom_right_y": 9,
    "top_left_y": 723,
    "top_left_x": 5111
  },
  
  {
    "bottom_right_x": 5101,
    "bottom_right_y": 5,
    "top_left_y": 721,
    "top_left_x": 3740
  },
  
  {
    "bottom_right_x": 2364,
    "bottom_right_y": 11,
    "top_left_y": 737,
    "top_left_x": 1031
  },
  
  {
    "bottom_right_x": 3739,
    "bottom_right_y": 0,
    "top_left_y": 741,
    "top_left_x": 2388
  }
  
]

The above numbers are taken directly from user input (mouse clicking) so are slightly different from the exact mapping. They represent the following physical mapping of pixels to screens (pixel values are shown in red as x,y pairs):

<img width="732" alt="Screen Shot 2021-09-13 at 12 36 19 AM" src="https://user-images.githubusercontent.com/16601007/133024689-a3c693fb-061c-4813-b77c-5a4ba1cbe1ef.png">


## Use Case: Video Processing Module

TODO: @Cody include in description

- Explanation of how the Processing script output can be used to translate videos to be properly displayed across the projectors
- Identify various libraries used
- Talk about program being dynamic and not only specific to this projector set up
