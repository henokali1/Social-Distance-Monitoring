import jetson.inference
import jetson.utils
import cv2


class mnSSD():
    def __init__(self, path, threshold):
        self.path = path
        self.threshold = threshold
        self.net = jetson.inference.detectNet(self.path, self.threshold)
    
    def detect(self, img, fps=False):
        imgCuda = jetson.utils.cudaFromNumpy(img)
        detections = self.net.Detect(imgCuda, overlay = "OVERLAY_NONE")
        objects = []
        filtered = {}
        for idx,d in enumerate(detections):
            className = self.net.GetClassDesc(d.ClassID)
            if className == 'person':
                objects.append([className, d])
                # print(d)
                x1,y1,x2,y2,c = int(d.Left),int(d.Top),int(d.Right),int(d.Bottom),(int(d.Center[0]), int(d.Center[1]))
                filtered[idx] = {'x1': x1,'y1': y1,'x2':x2,'y2':y2,'c':c}
                className = self.net.GetClassDesc(d.ClassID)
                # cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),2)
                # cv2.putText(img, className, (x1+5,y1+15),cv2.FONT_HERSHEY_DUPLEX, 0.75, (255,0,255),1)
                # cv2.putText(img, '.', (int(c[0]), int(c[1])),cv2.FONT_HERSHEY_DUPLEX, 0.75, (255,0,255),4)
                # print((int(c[0]), int(c[1])))
                if fps:
                    try:
                        cv2.putText(img, f'FPS: {int(self.net.GetNetworkFPS())}', (30,30),cv2.FONT_HERSHEY_DUPLEX, 0.75, (255,0,0),1)
                    except:
                        cv2.putText(img, f'FPS: -', (30,30),cv2.FONT_HERSHEY_DUPLEX, 0.75, (255,0,0),2)
        return filtered



def main():
    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    myModel = mnSSD("SSD-Mobilenet-v2", 0.5)
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

if __name__ == "__main__":
    main()
