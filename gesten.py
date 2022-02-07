from charset_normalizer import detect
import cv2
from cvzone.HandTrackingModule import HandDetector
import keyboard
 
cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=2)
lp = False #Variable für Laserpointer toggel
ready = False #Linke/1. Hand zurückgesetzt
ready2 = False #Rechte/2. Hand zurückgesetzt
mode = "key" #Aktiver Modus (Tastatur, Scrollen, Zoomen)
 
while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)  # With Draw
    print(mode)
 
    if hands:
        # Erkennung Hand 1
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # List of 21 Landmarks points
        bbox1 = hand1["bbox"]  # Bounding Box info x,y,w,h
        centerPoint1 = hand1["center"]  # center of the hand cx,cy
        handType1 = hand1["type"]  # Hand Type Left or Right

        #Erste Hand muss die Linke hand sein, Abfrage da MediaPipe gelegentlich die Hand tauscht (Hand1 Hand2)
        if hand1["type"] == "Left":
            fingers = detector.fingersUp(hand1)
        else:
            if len(hands) == 2:
                fingers = detector.fingersUp(hands[1])
            else:
                fingers = 0
        
        if fingers != 0:

            #Vor jeder Neuen Geste muss mit einer Faust erst zurückgesetzt werden
            if fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                ready = True
                #print("ready")
            
            ###
            #Gestenerkennung für KeyModus
            ###
            if mode == "key":
                #Tastendruck "Rechts" Geste: Pommesgabel
                if ready == True and fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
                    ready = False
                    print("rechts")
                    keyboard.send("right")
                
                #Tastendruck "Links" Geste: Peace
                if ready == True and fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
                    ready = False
                    print("links")
                    keyboard.send("left")

                #Laserpointer ein/aus toogeln: Daumen Zeigefinger ausgestreckt (L)
                if ready == True and fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                    ready = False
                    if lp == False:
                        keyboard.send("cmd+L")
                        lp == True
                    else:
                        keyboard.send("cmd+U")

                #Präsentation ausblenden/einblenden: Geste Telefonhörer
                if ready == True and fingers[0] == 1 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
                    ready = False
                    keyboard.send("shift+B")
            
            ###
            #Gestenerkennung für ScrollModus
            ###
            if mode == "scroll":

                #Geste für nach unten Scrollen: Peace
                if ready == True and fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
                    ready = False
                    keyboard.send("pagedown")

                #Geste für nach oben Scrollen: Pommesgabel
                if ready == True and fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
                    ready = False
                    keyboard.send("pageup")

            ###
            #Gestenerkennung für ZoomModus
            ###
            if mode == "zoom":
                
                #nach unten scrollen: Daumen + Zeigefinger ausgestreckt
                if ready == True and fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
                    ready = False
                    keyboard.send("cmd+plus")

                #nach oben scrollen: Pommesgabel
                if ready == True and fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
                    ready = False
                    keyboard.send("cmd+-") 

        #Erkennung Hand 2 um Modus zu wechseln
        if len(hands) == 2:
            hand2 = hands[1]
            lmList2 = hand2["lmList"]  # List of 21 Landmarks points
            bbox2 = hand2["bbox"]  # Bounding Box info x,y,w,h
            centerPoint2 = hand2["center"]  # center of the hand cx,cy
            handType2 = hand2["type"]  # Hand Type Left or Right

            print("Zweite Hand erkannt")
            
            #Code stellt sicher das die Zweite Hand die Rechte hand ist, um Verwechslungen zu vermeiden
            if hand2["type"] == "Right":
                fingers2 = detector.fingersUp(hand2)
            else:
                fingers2 = detector.fingersUp(hand1)
            
            #Vor jeder Neuen Geste muss mit einer Faust erst zurückgesetzt werden
            if fingers2[0] == 0 and fingers2[1] == 0 and fingers2[2] == 0 and fingers2[3] == 0 and fingers2[4] == 0:
                ready2 = True
                print("ready2")

            #KeyModus mit Geste: Pommesgabel
            if ready2 == True and fingers2[0] == 0 and fingers2[1] == 1 and fingers2[2] == 0 and fingers2[3] == 0 and fingers2[4] == 1:
                ready2 = False
                mode = "key"

            #MausModus mit Geste: Telefon
            if ready2 == True and fingers2[0] == 1 and fingers2[1] == 0 and fingers2[2] == 0 and fingers2[3] == 0 and fingers2[4] == 1:
                ready2 = False
                mode = "zoom"

            #ScrollModus mit Geste: Peace
            if ready2 == True and fingers2[0] == 0 and fingers2[1] == 1 and fingers2[2] == 1 and fingers2[3] == 0 and fingers2[4] == 0:
                ready2 = False
                mode = "scroll"

 
    cv2.imshow("Image", img)
    cv2.waitKey(1)