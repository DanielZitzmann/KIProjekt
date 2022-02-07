import os
import sys

import cv2
import mediapipe as mp
#import win32api, win32con
from pynput.mouse import Button, Controller

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
mouseCounter = 1
courserLastPostX = 0
courserLastPostY = 0
thumbLastPosX = 0
thumbLastPosY = 0
scale = 0.5 # Stelle Mausempfindlichkeit ein
useStickmode = 0 # Benutze Gleit Modus
mouse = Controller()

# For webcam input:
cap = cv2.VideoCapture(0)  # Kamera ID
with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        height, width, channels = image.shape
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_no, hand_landmarks in enumerate(results.multi_hand_landmarks):

                print(f'HAND NUMBER: {hand_no + 1}')
                print('-----------------------')
                if (hand_no == 0):
                    # Hole Zeigefingerkuppe Koordinaten und rechne diese in Pixel  um
                    indextipX = (width * hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x)
                    indextipY = height - (height * hand_landmarks.landmark[
                        mp_hands.HandLandmark.INDEX_FINGER_TIP].y)  # Spiegle Y von oben zu unten auf unten nach oben

                    # Hole Mittelfingerkuppe Koordinaten und rechne diese in Pixel um
                    mftipX = (width * hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x)
                    mftipY = height - (height * hand_landmarks.landmark[
                        mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y)  # Spiegle Y von oben zu unten auf unten nach oben

                    # Hole Ringfingerkuppe Koordinaten und rechne diese in Pixel um
                    rftipX = (width * hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x)
                    rftipY = height - (height * hand_landmarks.landmark[
                        mp_hands.HandLandmark.RING_FINGER_TIP].y)  # Spiegle Y von oben zu unten auf unten nach oben

                    # Hole Daumenkuppe Koordinaten und rechne diese in Pixel um
                    thumbtipX = (width * hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x)
                    thumbtipY = height - (height * hand_landmarks.landmark[
                        mp_hands.HandLandmark.THUMB_TIP].y)  # Spiegle Y von oben zu unten auf unten nach oben

                    # Berechne Abstände
                    # Abstand Mittelfinger Daumen
                    distanceThumbMiddleX = abs(mftipX - thumbtipX)
                    distanceThumbMiddleY = abs(mftipY - thumbtipY)
                    # Abstand Zeigefinger Daumen
                    distanceThumbIndexX = abs(indextipX - thumbtipX)
                    distanceThumbIndexY = abs(indextipY - thumbtipY)
                    # Abstand Ringfinger Daumen
                    distanceThumbRingX = abs(rftipX - thumbtipX)
                    distanceThumbRingY = abs(rftipY - thumbtipY)


                    thumbstring = 'Thumb: ' + str(thumbtipX)[:3] + " : " + str(thumbtipY)[:4]  # Setze DevAusgabe zusammen
                    indexstring = 'index: ' + str(indextipX)[:3] + " : " + str(indextipY)[:4]  # Setze DevAusgabe zusammen
                    distancestring = 'Distance: ' + str(distanceThumbMiddleX)[:3] + " : " + str(distanceThumbMiddleY)[:4] + " MC: " + str(
                        mouseCounter)

                    cv2.flip(image, 1) # Entspiegel Bild

                    if distanceThumbMiddleX <= 20 and distanceThumbMiddleY <= 20: # Erkenne Ob Daumen und MF berühren
                        distanceColor = (0, 0, 255)
                        # print('mc: ' + str(mouseCounter))
                        if mouseCounter < 15:  # Warte Mit Mausbewegung auf mouseCounter um ungewollte Bewegung zu verhindern
                            mouseCounter += 1
                            thumbLastPosX, thumbLastPosY = thumbtipX, thumbtipY # Speicher Letzte Pos des Daumen
                        else:
                            if distanceThumbIndexX <= 20 and distanceThumbIndexY <= 20: # Erkenne Ob Daumen und ZF berühren
                                mouse.press(Button.left)
                                mouse.release(Button.left)

                            if distanceThumbRingX <= 20 and distanceThumbRingY <= 20: # Erkenne Ob Daumen und RF berühren
                                mouse.press(Button.right)
                                mouse.release(Button.right)


                            nx, ny = mouse.position #Speichere Letzte Maus Pos
                            #Setze Neue absolute Maus Pos abhängig von Daumenbewegung und letzter Maus Pos
                            mouse.position =(
                                ((nx - (int((thumbtipX - thumbLastPosX)/scale)) ), (ny - ((int((thumbtipY - thumbLastPosY)/scale))))))
                            courserLastPostX, courserLastPostY = nx, ny
                            if useStickmode==0:
                              thumbLastPosX, thumbLastPosY = thumbtipX, thumbtipY
                            print('last Coords : ' + str(courserLastPostX) + ' ' + str(courserLastPostY))
                            print('New Coords : ' + str(nx) + ' ' + str(ny))
                            # win32api.SetCursorPos((int(thumbtipX), int(thumbtipY)))
                    else:
                        distanceColor = (255, 255, 255)
                        # print('mc: ' + str(mouseCounter))
                        if mouseCounter > 0:
                            mouseCounter -= 1
                            # print('mc: ' + str(mouseCounter))

                    # Füge Kamera Dev Ausgaben hinzu
                    image = cv2.putText(image, indexstring[:], (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2,
                                        cv2.LINE_AA)
                    image = cv2.putText(image, thumbstring[:], (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2,
                                        cv2.LINE_AA)
                    image = cv2.putText(image, distancestring[:], (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, distanceColor, 2,
                                        cv2.LINE_AA)
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
        # Flip the image horizontally for a selfie-view display.

        cv2.imshow('Anwendung für freihändige Eingabe', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
