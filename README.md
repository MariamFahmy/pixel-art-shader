# **Automatic Pixel Art Shader**

This is a program that automatically shades and highlights pixel art as shown below.

The program finds a shading distribution depending on the position of the light source. This shading distribution will be used to assign the appropriate shades or highlights to the pixels. This part of the algorithm is taken from the paper  "Automatic Sprite Shading" at https://www.sbgames.org/papers/sbgames09/computing/full/cp10_09.pdf, and its implementation is my own.

Then, using this shading distribution I devised and implemented a simple way to map the shading distribution value of the pixel to an actual shade or highlight using the Hue, Saturation, Intensity color model  and then pixelated the sprite to give it a pixel-art appearance.

Written in Python using numpy and cv2.

Currently, there is no graphical user interface :(

The program can be run from a Python environment with numpy and cv2 installed. 

To test it, the images provided in the repo can be used. 

![program results](https://github.com/MariamFahmy/pixel-art-shader/blob/main/program_results.png "program results")
