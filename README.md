# hand_tracker

A Python script that utilizes OpenCV and the MediaPipe libraries to perform hand gesture detection and finger counting in real-time using your computer's camera feed. The script displays hand landmarks and the finger count on the video feed and allows you to adjust finger detection thresholds using slider bars.

Note: Finger counting is a little unstable at the moment, having a hard time calibrating to detect more than three fingers. I have added some trackbars to adjust the threshold values for calibration.

## Installation

Before running the `hand_tracker.py` script, make sure you have the necessary dependencies installed:

1. Install the required Python packages using the following command:

   ```bash
   pip install opencv-python mediapipe
   ```

2. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/your-username/hand-gesture-tracker.git
   cd hand_tracker
   ```

## Usage

1. Run the `hand_tracker.py` script:

   ```bash
   python hand_tracker.py
   ```

2. A window will open showing the live camera feed with hand landmarks and finger count displayed.

3. To exit the program, press the 'q' key.

## Features

- The `HandGestureCounter` class in the script performs hand gesture detection and finger counting using the MediaPipe library.
- It utilizes the `cv2.VideoCapture` to access the camera feed and the MediaPipe Hands module to detect hand landmarks.
- The script displays hand landmarks and connections on the video feed using MediaPipe drawing utilities.
- You can adjust finger detection thresholds using slider bars for thumb-index and index-middle distances. The sliders can be found in the separate window titled "Threshold Sliders".
- The script provides basic finger counting functionality based on the landmark positions. Note that the counting accuracy may vary.

## Notes

- The `count_fingers()` method provides a basic implementation for finger counting and might require further refinement for improved accuracy.
- The script is set to work with both left and right hands, but the finger counting logic may not be completely accurate.
- The "Threshold Sliders" window may sometimes appear behind the camera feed window. Make sure to locate and adjust the sliders as needed.

Feel free to experiment with and improve the script according to your requirements and contribute any enhancements to the original repository.
                                                                                
## Acknowlegdements                                                              
                                                                                
This program utilizes the OpenCV library for computer vision tasks. Credits to the OpenCV community for their contributions.

The development of this application benefited from the assistance of language models, including GPT-3.5 and GPT-4, provided by OpenAI. The author acknowledges the valuable contributions made by these language models in generating design ideas and providing insights during the development process.
