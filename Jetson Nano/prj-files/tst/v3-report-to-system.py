from glob import glob
from turtle import distance
import cv2
import MobileNetSSDModule as mnssdm
import itertools
from math import sqrt as sqrt
import time
import requests

myModel = mnssdm.mnSSD("SSD-Mobilenet-v2", 0.5)
distance_threshold = 350
cntr_start = 0
crnt_tm = 0
tm_df = 0
report_delay = 10
url = 'http://18.183.88.175:9991/'

location = 'HCT-Fuj'
gate = 'Gate 8A'
cam_id = 'FLR251'

def possible_combs(val):
    c = list(itertools.product(val, val))
    f=[]
    for i in c:
        f.append(i) if not any([i[0] == i[1], (i[1], i[0]) in f]) else 0
    return f


def calculate_dist(p1, p2):
    x1=p1[0]
    x2=p2[0]
    y1=p1[0]
    y2=p2[1]
    dst = sqrt((x2-x1)**2 + (y2-y1)**2)
    return int(dst)

def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=640,
    display_height=360,
    framerate=60,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


def show_camera():
    global cntr_start
    global crnt_tm
    global tm_df
    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    # print(gstreamer_pipeline(flip_method=0))
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    if cap.isOpened():
        window_handle = cv2.namedWindow("CSI Camera", cv2.WINDOW_AUTOSIZE)
        # Window
        while cv2.getWindowProperty("CSI Camera", 0) >= 0:
            _, img = cap.read()
            filtered = myModel.detect(img)
            tot = len(filtered)
            ctrs = []
            if tot <= 1:
                cntr_start = 0
                crnt_tm = 0
                tm_df = 0
                print(f'Cond-1\t tm_diff: {tm_df}\tdist: 0')

            if tot > 0:
                pc_idxs = [i for i in range(tot)]
                pos_combs = possible_combs(pc_idxs)
                for k in filtered.keys():
                    x1 = filtered[k]['x1']
                    y1 = filtered[k]['y1']
                    x2 = filtered[k]['x2']
                    y2 = filtered[k]['y2']
                    c = filtered[k]['c']
                    ctrs.append(c)
                    # cv2.putText(img, str(k), (x1+5,y1+15),cv2.FONT_HERSHEY_DUPLEX, 0.75, (255,0,255),1)
                    cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),2)
                    cv2.putText(img, '.', (int(c[0]), int(c[1])),cv2.FONT_HERSHEY_DUPLEX, 0.75, (255,0,255),4)
                for i in pos_combs:
                    crnt_tm = int(time.time())
                    dist = calculate_dist(ctrs[i[0]], ctrs[i[1]])
                    # print(f'dist: {dist}')
                    if dist <= distance_threshold:
                      if cntr_start == 0:
                        cntr_start = int(time.time())
                      else:
                        tm_df = crnt_tm - cntr_start
                        print(f'Cond-2\t tm_diff: {tm_df}\tdist: {dist}')
                        if tm_df > report_delay:
                            cv2.line(img, ctrs[i[0]], ctrs[i[1]], (0,0,255), 2)
                            fn=f'/home/nvidia/prj-files/report-imgs/{int(time.time())}---{location}---{gate}---{cam_id}---.jpg'
                            cv2.imwrite(fn, img)
                            files = {'image': open(fn, 'rb')}
                            r = requests.post(url, files=files)
                            print(r)
                            print('Send Report')
                            time.sleep(3)
                            cntr_start = int(time.time())
                      cv2.line(img, ctrs[i[0]], ctrs[i[1]], (0,0,255), 2) 
                    else:
                      cntr_start = int(time.time())
                      tm_df = crnt_tm - cntr_start
                      print(f'cond-3\t tm_diff: {tm_df}\tdist: {dist}')
                      # cv2.line(img, ctrs[i[0]], ctrs[i[1]], (0,255,0), 2) 






            cv2.imshow("CSI Camera", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
    else:
        print("Unable to open camera")


if __name__ == "__main__":
    show_camera()
