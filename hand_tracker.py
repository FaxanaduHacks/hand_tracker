import cv2
import mediapipe as mp

class HandGestureCounter:
    """
    This class performs hand gesture detection and finger counting using the
    MediaPipe library. It displays the hand landmarks and finger count on a
    live video feed, and allows adjusting the finger detection thresholds using
    slider bars.

    Note: This program accurately detects left and right hands; however, the
    `count_fingers()` method needs some work. I added a threshold slider to
    help troubleshoot for now. Also, don't forget about the sliders box to help
    adjust the threshold, it usually spawns behind the camera window.
    """

    def __init__(self):
        """
        Initialize the HandGestureCounter object.

        Attributes:
            cap (cv2.VideoCapture): Video capture object.

            mp_hands (mp.solutions.hands): MediaPipe Hands object for hand
            detection.

            hands (mp.solutions.hands.Hands): Hands object for hand detection.
            mp_drawing (mp.solutions.drawing_utils): MediaPipe drawing utility.

            text_position_left (tuple): Position of left-hand text display.

            text_position_right (tuple): Position of right-hand text display.

            thumb_index_threshold (float): Default threshold for thumb-index
            distance.

            index_middle_threshold (float): Default threshold for index-middle
            distance.
        """
        # Initialize VideoCapture for accessing the camera:
        self.cap = cv2.VideoCapture(0)
        # Initialize Mediapipe hands module:
        self.mp_hands = mp.solutions.hands
        # Create an instance of the hands detector:
        self.hands = self.mp_hands.Hands()
        # Initialize Mediapipe drawing utilities:
        self.mp_drawing = mp.solutions.drawing_utils
        # Initial position for left-hand text display:
        self.text_position_left = (10, 30)
        # Initial position for right-hand text display:
        self.text_position_right = (10, 60)

        # Initialize default threshold values:
        self.thumb_index_threshold = 0.1
        self.index_middle_threshold = 0.1

        # Create a separate window for sliders:
        cv2.namedWindow("Threshold Sliders")
        cv2.createTrackbar("Thumb-Index Threshold", "Threshold Sliders", int(self.thumb_index_threshold * 100), 100, self.on_thumb_index_threshold_change)
        cv2.createTrackbar("Index-Middle Threshold", "Threshold Sliders", int(self.index_middle_threshold * 100), 100, self.on_index_middle_threshold_change)

    def on_thumb_index_threshold_change(self, value):
        """
        Update the thumb-index threshold when the slider value changes.

        Args:
            value (int): New value of the slider.
        """
        self.thumb_index_threshold = value / 100.0

    def on_index_middle_threshold_change(self, value):
        """
        Update the index-middle threshold when the slider value changes.

        Args:
            value (int): New value of the slider.
        """
        self.index_middle_threshold = value / 100.0

    def count_fingers(self, lm_list):
        """
        Count the number of fingers held up based on landmark positions.

        Args:
            lm_list (list): List of hand landmark positions.

        Returns:
            int: Number of fingers held up.
        """
        # Get the thumb-index and index-middle thresholds:
        thumb_index_threshold = self.thumb_index_threshold
        index_middle_threshold = self.index_middle_threshold

        # Finger landmark indices:
        thumb_tip = lm_list[4]
        index_tip = lm_list[8]
        middle_tip = lm_list[12]
        ring_tip = lm_list[16]
        little_tip = lm_list[20]

        # Calculate the distance between thumb tip and index finger tip:
        thumb_index_dist = abs(thumb_tip['y'] - index_tip['y'])

        # Calculate the distance between index finger tip and middle finger
        # tip:
        index_middle_dist = abs(index_tip['y'] - middle_tip['y'])

        # Check for closed fist gesture:
        if thumb_index_dist < thumb_index_threshold and index_middle_dist < index_middle_threshold:
            return 0

        # Count fingers held up:
        finger_count = 0

        # Thumb:
        if thumb_tip['y'] < index_tip['y']:
            finger_count += 1

        # Index finger:
        if index_tip['y'] < middle_tip['y']:
            finger_count += 1

        # Middle finger:
        if middle_tip['y'] < ring_tip['y']:
            finger_count += 1

        # Ring finger:
        if ring_tip['y'] < little_tip['y']:
            finger_count += 1

        # Little finger:
        finger_count += 1

        return finger_count

    def run(self):
        """
        Run the hand gesture counter.

        This method captures video frames, detects hand landmarks, counts fingers,
        and displays the results on the video feed.
        """
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            # Flip the frame horizontally for a mirrored effect:
            frame = cv2.flip(frame, 1)

            # Convert the BGR color image to RGB format for processing by
            # MediaPipe:
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the image to detect hand landmarks using the MediaPipe
            # Hands model:
            results = self.hands.process(image)

            # Check if there are multiple hand landmarks detected in the frame:
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw hand landmarks and connections on the frame:
                    self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                    # Convert hand landmarks to a list of dictionary entries:
                    lm_list = []
                    for lm in hand_landmarks.landmark:
                        lm_list.append({
                            'x': int(lm.x * frame.shape[1]),
                            'y': int(lm.y * frame.shape[0])
                        })

                    # Count the number of fingers held up using landmarks:
                    finger_count = self.count_fingers(lm_list)

                    # Determine if the hand is on the left or right side of the
                    # frame:
                    hand_side = "Left" if lm_list[0]['x'] < frame.shape[1] // 2 else "Right"

                    # Display finger count text on the frame:
                    if hand_side == "Left":
                        cv2.putText(frame, f"{hand_side} Hand Fingers: {finger_count}", self.text_position_left,
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                    else:
                        cv2.putText(frame, f"{hand_side} Hand Fingers: {finger_count}", self.text_position_right,
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

                # Reset text positions for the next frame:
                self.text_position_left = (10, 30)
                self.text_position_right = (10, 60)

            cv2.imshow('Hand Tracking', frame)

            # Exit the loop if the window is closed:
            if cv2.waitKey(1) == ord('q'):
                break

        # Release the VideoCapture, destroy OpenCV windows, and cleanup the
        # slider window:
        self.cap.release()
        cv2.destroyAllWindows()
        cv2.destroyWindow("Threshold Sliders")

if __name__ == '__main__':
    hand_gesture_counter = HandGestureCounter()
    hand_gesture_counter.run()
