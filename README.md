# **Automatic Pixel Art Shader**

This is a program that automatically shades and highlights pixel art as shown below.

The program finds a shading distribution depending on the position of the light source. This shading distribution will be used to assign the appropriate shades or highlights to the pixels. This part of the algorithm is taken from the paper  "Automatic Sprite Shading" at https://www.sbgames.org/papers/sbgames09/computing/full/cp10_09.pdf.

Then, using this shading distribution I devised a simple way using the Hue, Saturation, Intensity color model to map the shading distribution value of the pixel to an actual shade or highlight and then pixelated the sprite to give it a pixel-art appearance.

Written in Python using numpy and cv2.

To run the code, you need numpy and cv2. 

To test it, the images provided in the repo can be used. 

![program results](https://github.com/MariamFahmy/pixel-art-shader/blob/main/program_results.png "program results")
