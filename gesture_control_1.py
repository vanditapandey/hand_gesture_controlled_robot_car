import cv2
import mediapipe as mp
import math
import serial
import time

# Arduino/Bluetooth connection
arduino = serial.Serial("COM9",9600)
time.sleep(2)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

prev_command = ""   # prevent spamming


def send_command(command):
    global prev_command
    if command != prev_command:
        print("Sending:", command)
        arduino.write(command.encode())
        prev_command = command


with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7) as hands:

    while True:

        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame,1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        command = "S"   # Default = STOP

        # If a hand is detected
        if results.multi_hand_landmarks:

            for hand_landmarks in results.multi_hand_landmarks:

                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

                lm = hand_landmarks.landmark

                # Detect fingers
                index_open = lm[8].y < lm[6].y
                middle_open = lm[12].y < lm[10].y
                ring_open = lm[16].y < lm[14].y
                pinky_open = lm[20].y < lm[18].y

                gesture = "NONE"

                if not index_open and not middle_open and not ring_open and not pinky_open:
                    gesture = "FIST"

                elif index_open and middle_open and not ring_open and not pinky_open:
                    gesture = "REVERSE"

                elif index_open and middle_open and ring_open and pinky_open:
                    gesture = "OPEN"

                # Tilt detection
                x1, y1 = lm[5].x, lm[5].y
                x2, y2 = lm[17].x, lm[17].y

                angle = math.degrees(math.atan2(y2 - y1, x2 - x1))

                # Command mapping
                if gesture == "FIST":
                    command = "S"

                elif gesture == "REVERSE":
                    command = "B"

                elif gesture == "OPEN":

                    if angle > 30:
                        command = "L"

                    elif angle < -30:
                        command = "R"

                    else:
                        command = "F"

                # Send when hand detected
                send_command(command)

                # Display info
                cv2.putText(frame, f"Gesture: {gesture}", (20,40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

                cv2.putText(frame, f"Angle: {int(angle)}", (20,80),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

                cv2.putText(frame, f"Command: {command}", (20,120),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

        else:
            # 🔥 ONLY ADDITION (your requirement)
            send_command("S")   # No hand → STOP

            cv2.putText(frame, "NO HAND → STOP", (20,160),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)


        cv2.imshow("Gesture Robot Control", frame)

        key = cv2.waitKey(1)

        if key == 27:
            break

        if cv2.getWindowProperty("Gesture Robot Control", cv2.WND_PROP_VISIBLE) < 1:
            break


cap.release()
cv2.destroyAllWindows()
