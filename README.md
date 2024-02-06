# **Automatic Pixel Art Shader**

This is a program that automatically shades and highlights pixel art as shown in the image below. The unshaded illustrations are the inputs, and the shaded and highlighted ones are the outputs!
![program results](https://github.com/MariamFahmy/pixel-art-shader/blob/main/program_results.png "program results")

The program finds a shading distribution depending on the position of the light source. This part of the algorithm is taken from the paper  "Automatic Sprite Shading" at https://www.sbgames.org/papers/sbgames09/computing/full/cp10_09.pdf, and its implementation is my own.

Then, using this shading distribution, I devised and implemented a simple way to map the shading distribution value of the pixel to an actual shade or highlight using the Hue, Saturation, Intensity color model and then pixelated the sprite to give it a pixel-art appearance.

Written in Python using numpy and opencv-python.

To test it, the images provided in the repo can be used, or you can use your own illustrations!


