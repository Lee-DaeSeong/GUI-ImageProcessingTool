import cv2

def nothing(x):
    pass

capture = cv2.VideoCapture(0)		# 동영상 파일 개방
if not capture.isOpened(): raise Exception("동영상 파일 개방 안됨")		# 예외 처리
cv2.namedWindow('color')
frame_rate = capture.get(cv2.CAP_PROP_FPS)           		# 초당 프레임 수
delay = int(1000 / frame_rate)                         		# 지연 시간
frame_cnt = 0                                       		# 현재 프레임 번호
cv2.createTrackbar('R','color',0,255,nothing)
cv2.createTrackbar('G','color',0,255,nothing)
cv2.createTrackbar('B','color',0,255,nothing)

while True:
    ret, frame = capture.read()
    if not ret or cv2.waitKey(delay) >= 0: break    				# 프레임 간 지연 시간 지정
    blue, green, red = cv2.split(frame)             				# 컬러 영상 채널 분리
    frame_cnt += 1

    r = cv2.getTrackbarPos('R', 'color')
    g = cv2.getTrackbarPos('G', 'color')
    b = cv2.getTrackbarPos('B', 'color')
    cv2.add(blue, b, blue)  		# blue 채널 밝기 증가
    cv2.add(green, g, green) 	# green 채널 밝기 증가
    cv2.add(red, r, red)   	# red 채널 밝기 증가

    frame = cv2.merge( [blue, green, red] )
    cv2.imshow("color", frame)
capture.release()