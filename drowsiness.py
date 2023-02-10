from imutils import face_utils
import dlib
import cv2
from pygame import mixer
import os
import time
import serial

'''
pip install -r requirements.txt로 필수 라이브러리 설치하시고
실행해서 눈 떴을때랑 감았을때 거리 출력되는거 보고 thres 변수 바꿔주시면 적절하게 바꿔서 실행하세요.
'''

path = os.path.abspath(os.path.dirname(__file__))
#ser = serial.Serial("/dev/cu.usbserial-120", baudrate=9600)

# calibrate this based on your camera setting
thres = 6

mixer.init()
sound = mixer.Sound(path + "/alarm.wav")
dlist = []


detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(path + "/shape_predictor_68_face_landmarks.dat")

#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('http://192.168.1.102:81/stream')
frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))


def dist(a,b):
    x1,y1 = a
    x2,y2 = b
    return ((x1-x2)**2 + (y1-y2)**2)**0.5
 
while True:
    # Getting out image by webcam 
    _, image = cap.read()
    # Converting the image to gray scale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
    # Get faces into webcam's image
    rects = detector(gray, 0)
    
    # For each detected face, find the landmark.
    for (i, rect) in enumerate(rects):
        # Make the prediction and transfom it to numpy array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
    
        # Draw on our image, all the finded cordinate points (x,y) 
        le = []
        re = []
        for (x, y) in shape:
            cv2.circle(image, (x, y), 2, (0, 255, 0), -1)
        
        le_38 = shape[37]
        le_39 = shape[38]
        le_41 = shape[40]
        le_42 = shape[41]

        re_44 = shape[43]
        re_45 = shape[44]
        re_47 = shape[46]
        re_48 = shape[47]
        

        print(dist(re_44, re_48))
        
        dlist.append((dist(le_38,le_42)+dist(le_39,le_41)+dist(re_44,re_48)+dist(re_45,re_47)) / 4<thres)
        if len(dlist)>10:dlist.pop(0)

        print(dlist)
        # Drowsiness detected
        if sum(dlist)>=4:
            try:
                end = time.time()
                result_time = end - begin
                result_time = round(result_time,0)
                print("YOU SLEEPIN in",result_time)
                if result_time >= 2:
                    sound.play()
                    #ser.write(2)
            except:
                pass
        else:
            try:
                sound.stop()
                begin = time.time()
                print("Eyes are open.")
                #ser.write(1)
            except:
                pass
        
        
    # Show the image
    cv2.imshow("Output", image)
    
    # q to quit
    if cv2.waitKey(5) & 0xFF == 113:
        break

cv2.destroyAllWindows()
cap.release()