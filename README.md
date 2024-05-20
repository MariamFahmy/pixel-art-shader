# **Automatic Pixel Art Shader**

**Demo video:** https://www.youtube.com/watch?v=33y9JV2fO6A

This is a prototype program that automatically shades and highlights pixel art as shown in the image below. The unshaded illustrations are the inputs, and the shaded and highlighted ones are the outputs!
![program results](https://github.com/MariamFahmy/pixel-art-shader/blob/main/program_results.png "program results")
![image](https://github.com/MariamFahmy/pixel-art-shader/assets/51763380/91994ea7-90f6-4226-8a97-7459824ada02)


The program finds a shading distribution depending on the position of the light source. This part of the algorithm is taken from the paper  "Automatic Sprite Shading" at https://www.sbgames.org/papers/sbgames09/computing/full/cp10_09.pdf, and its implementation is my own.

Then, using this shading distribution, I devised and implemented a simple way to map the shading distribution value of the pixel to an actual shade or highlight using the Hue, Saturation, Intensity color model and then added code to pixelate the sprite to give it a pixel-art appearance.

Written in Python using numpy and cv2.

To test it, clone the repo in your Python IDE with numpy and opencv-python packages installed. The images provided in the repo can be used, or you can use your own illustrations! 

This is an open-source project. I encourage you to fork it and contribute. 


