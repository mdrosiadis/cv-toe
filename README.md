# CV Toe
### An augmented reality tic tac toe game, co-developed with two of my students

## The Motive
One of the major set-backs of learning to code in a young age is the lack of visual feedback from your programs. Students often get dissapointed during their early steps in coding, as text based programs are not that exiting. Our goal was to fix that, by providing new ways to interact with projects that would otherwise seem like a coding-101 assingment.

## The Idea
It's no secret that computer vision is one of the decade's hot topics, with augmented reality getting in our everyday lives with every day passing. After implementing a tic-tac-toe game as a hands-on project on Python programming, we thought: how about making the computer understand the symbols drawn on our whiteboard? That was the begining of CV-Toe.

## Making a GUI
The first thing we needed was a nice User Interface to display on our whiteboard. It had to be simple enough for our students to understand, yet convinient and visually appealing. We used tkinter, a Python library for GUIs, to render the the grid and symbols, using a canvas and basic math, to scale to arbitary resolutions.

## The computer vision
Alegendly. the most exciting part of the project was making the computer understand the video singal from the webcam observing the whiteboard. We used OpenCV, an open-source library for computer vision tasks. After some experimentation, we conclueded on these recognition steps:

  1. Focus the webcam on the videowall, and drop brightness enough.
  2. Detect the 4 circles using HoughTransform, one for each corner of the videowall. These are used to crop the video signal to only analyse the region of interset
  3. Transform the region of interest on an alligned 2D plane. Doing so, the recognition is flawless even if the camera points at an angle.
  4. Crop each on of the 9 boxes. For each one of those, detect if it containts a symbol or not, using circle and line detection, using Hough transforms and Canny edge detection.

## Binding the components
Our last step was to bind the components developed (tic-tac-toe logic, GUI and camera detector) together. We abstracted the game logic into a class, to better integrate with the GUI program. Then, we've spawned a websockets server, to listen for changes in the detected state. The camera recognition script sends the new state to the server whenever a change is detected. We detect movement using a basic, per-frame diffrence-based algorithm.

## Set Up Instructions
After setting up your projector or video wall, run the graphics module:

```sh
python graphics.py
```

Set up your camera settings to make the wall clearly visible and not over-saturated.
Now run the final_camera module.

```sh
python final_camera.py
```

You might need to change the camera device ID. You should get feedback on the detection soon after.
That's it! The video wall and detection are conected. You can draw on the whiteboard, and the AI system should play back. Player staring is X, so you're playing X. Press ENTER to clear the board.

## Notes

Code is far from perfect. This is a demonstration of what is possible with the tools available and the classes level of knowledge, guided by me.

## Contributing

Feel free to suggest changes or make pull requests.
