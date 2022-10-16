import cv2
import MobileNetSSDModule as mnssdm

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
myModel = mnssdm.mnSSD("SSD-Mobilenet-v2", 0.5)

while True:
    success, img = cap.read()
    objects = myModel.detect(img, True)
    

    
    
    # img = jetson.utils.cudaToNumpy(imgCuda)

    cv2.imshow("Image", img)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
cap.release()
# Destroy all the windows
cv2.destroyAllWindows()
