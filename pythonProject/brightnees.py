import numpy as np, cv2

def bright(n):
    array = np.full(src.shape, (n, n, n), dtype=np.uint8)
    if cv2.getTrackbarPos(switch,'bright')==0:
        res = cv2.add(src, array)
        cv2.imshow("bright", res)
    else:
        res = cv2.subtract(src, array)
        cv2.imshow("bright", res)


def reverse(x):
    if cv2.getTrackbarPos(switch, 'bright') == 0:
        n=cv2.getTrackbarPos('brightly','bright')
        array = np.full(src.shape, (n, n, n), dtype=np.uint8)
        res = cv2.add(src, array)
        cv2.imshow("bright", res)
    else:
        n = cv2.getTrackbarPos('brightly', 'bright')
        array = np.full(src.shape, (n, n, n), dtype=np.uint8)
        res = cv2.subtract(src, array)
        cv2.imshow("bright", res)


cv2.namedWindow('bright')
src=cv2.imread('1.jpg')  # 영상 읽기
cv2.imshow('origin', src)
cv2.imshow("bright",src)
cv2.createTrackbar('brightly','bright',0,255,bright)
switch='0 : Brightnees \n 1 : Darknees'
cv2.createTrackbar(switch,'bright',0,1,reverse)
cv2.waitKey(0)
cv2.destroyAllWindows()
