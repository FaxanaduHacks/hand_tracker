import cv2
import mediapipe as mp

def count_fingers(lm_list):
    # Finger landmark indices
    thumb_tip = lm_list[4]
    index_tip = lm_list[8]
    middle_tip = lm_list[12]
    ring_tip = lm_list[16]
    little_tip = lm_list[20]

    # Calculate the distance between thumb tip and index finger tip
    thumb_index_dist = abs(thumb_tip['y'] - index_tip['y'])

    # Calculate the distance between index finger tip and middle finger tip
    index_middle_dist = abs(index_tip['y'] - middle_tip['y'])

    # Check for closed fist gesture
    if thumb_index_dist < 0.1 and index_middle_dist < 0.1:  # Adjust the thresholds as needed
        return 0

    # Count fingers held up
    finger_count = 0

    # Thumb
    if thumb_tip['y'] < index_tip['y']:
        finger_count += 1

    # Index finger
    if index_tip['y'] < middle_tip['y']:
        finger_count += 1

    # Middle finger
    if middle_tip['y'] < ring_tip['y']:
        finger_count += 1

    # Ring finger
    if ring_tip['y'] < little_tip['y']:
        finger_count += 1

    # Little finger
    finger_count += 1

    return finger_count

def main():
    # Initialize VideoCapture object to read from the webcam
    cap = cv2.VideoCapture(0)

    # Initialize mediapipe hands module
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()

    # Initialize mediapipe drawing module
    mp_drawing = mp.solutions.drawing_utils

    while True:
        # Read frame from the webcam
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame horizontally
        frame = cv2.flip(frame, 1)

        # Convert the image to RGB for mediapipe
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the image with mediapipe hands
        results = hands.process(image)

        # Initialize positions for hand readings
        text_position_left = (10, 30)
        text_position_right = (10, 60)

        # Draw hand landmarks and count fingers for each hand
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw landmarks
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Get landmark coordinates
                lm_list = []
                for lm in hand_landmarks.landmark:
                    lm_list.append({
                        'x': int(lm.x * frame.shape[1]),
                        'y': int(lm.y * frame.shape[0])
                    })

                # Count fingers
                finger_count = count_fingers(lm_list)

                # Determine left or right hand based on x-coordinate of wrist landmark
                hand_side = "Left" if lm_list[0]['x'] < frame.shape[1] // 2 else "Right"

                # Display finger count for each hand
                if hand_side == "Left":
                    cv2.putText(frame, f"{hand_side} Hand Fingers: {finger_count}", text_position_left,
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                    text_position_left = (text_position_left[0], text_position_left[1] + 30)
                else:
                    cv2.putText(frame, f"{hand_side} Hand Fingers: {finger_count}", text_position_right,
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                    text_position_right = (text_position_right[0], text_position_right[1] + 30)

        # Display the frame
        cv2.imshow('Hand Tracking', frame)

        # Exit the loop if the window is closed
        if cv2.waitKey(1) == ord('q'):
            break

    # Release the VideoCapture and destroy the OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

