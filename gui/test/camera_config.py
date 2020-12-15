import cv2

cap = cv2.VideoCapture(0)

print(cap.get(cv2.CAP_PROP_BUFFERSIZE))

for i in range(-4,50):
    try:
        a = cap.get(i)
        print("capture property ID: ",i, " Value: ",a)
    except:
        print("capture property ID: ",i, " NOT AVAIL")
