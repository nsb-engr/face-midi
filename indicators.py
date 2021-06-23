import cv2
import numpy as np

def draw_meter(image: np.ndarray, value: int):
    offset = 5
    pt1 = (50,50)
    pt2 = (100,300)
    meter_val = int( value / 127.0 * (pt2[1]-pt1[1]))

    pt_meter = (50, 300 - meter_val)
    # print(pt_meter)
    cv2.rectangle(image, pt_meter, pt2,
                color=(0,255,0),thickness=-1,
                lineType=cv2.LINE_4)

    cv2.rectangle(image, pt1, pt2,
                color=(0,255,0),thickness=1,
                lineType=cv2.LINE_4)
    
    text = str(value)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, text, (50,45), font, 1,
                 (0,255,0), 2, cv2.LINE_AA)

if __name__ == "__main__":
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    i = 0
    while (cap.isOpened()):
        i %= 128
        value = (i + 1)
        ret, image = cap.read()
        draw_meter(image,value)
        cv2.imshow("test",image)
        key = cv2.waitKey(1)
        i += 1
        if key == 27: #esc key
            break

    cap.release()
    cv2.destroyAllWindows()