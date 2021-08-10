import cv2

def nothing(x):
    pass


cv2.namedWindow('color')
cv2.createTrackbar('R','color',0,255,nothing)
cv2.createTrackbar('G','color',0,255,nothing)
cv2.createTrackbar('B','color',0,255,nothing)


img=cv2.imread('1.jpg')

while True:
    img = cv2.imread('1.jpg')
    blue, green, red = cv2.split(img)             				# 컬러 영상 채널 분리

    r = cv2.getTrackbarPos('R', 'color')
    g = cv2.getTrackbarPos('G', 'color')
    b = cv2.getTrackbarPos('B', 'color')
    cv2.add(blue, b, blue)  		# blue 채널 밝기 증가
    cv2.add(green, g, green) 	# green 채널 밝기 증가
    cv2.add(red, r, red)   	# red 채널 밝기 증가

    img = cv2.merge( [blue, green, red] )
    cv2.imshow("color", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyWindow('color')


