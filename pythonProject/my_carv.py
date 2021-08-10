import cv2
import numpy as np

from seam_carving import SeamCarver
from Sketcher import Sketcher

def resize(img_name):
    print(img_name)

    MODE = 'remove'  # 'remove', 'protect' default = remove
    img_path = img_name  # sys.argv[1]


    def nothing(x):
        pass


    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    img_masked = img.copy()
    mask = np.zeros(img.shape[:2], np.uint8)
    # notice = 'Change Image! //m : remove mode/p : protect mode'
    sketcher = Sketcher('image', [img_masked, mask], lambda: ((255, 255, 255), 255))
    cv2.createTrackbar('width', 'image', img.shape[1], img.shape[1] * 2, nothing)
    cv2.createTrackbar('height', 'image', img.shape[0], img.shape[0] * 2, nothing)

    while True:


        key = cv2.waitKey()

        if key == ord('m'): #MODE를 remove로 변경
            print('Remove Mode Started')
            MODE = 'remove'
        if key == ord('p') : # MODE를 Protect로 변경
            print('Protect Mode started')
            MODE = 'protect'
        if key == ord('q'):  # quit
            break
        if key == ord('r'):  # masking reset.
            print('reset')
            img_masked[:] = img
            mask[:] = 0
            sketcher.show()
        if key == 32:  # hit spacebar
            new_width = int(cv2.getTrackbarPos(trackbarname='width', winname='image'))
            new_height = int(cv2.getTrackbarPos(trackbarname='height', winname='image'))

            if np.sum(mask) > 0:  # object removal : masking 있을 시 반영 or protect mask : masking이 있어도 사진 보호
                if MODE == 'remove': # 'm'을 누르면 Remove mode로 마우스를 이용해 mask
                    carver = SeamCarver(img, 0, 0, object_mask=mask)
                    cv2.imshow('output', carver.out_image.astype(np.uint8)) #즉시 확인 용도 imshow
                    res = carver.out_image.astype(np.uint8)
                    cv2.imwrite("./output_carv.jpg", res)
                elif MODE == 'protect': # 'p'를 누르면 마우스로 mask를 해도 반영되지 않고, resize의 결과만 반영
                    carver = SeamCarver(img, new_height, new_width, protect_mask=mask)
                    cv2.imshow('resize', cv2.resize(img, dsize=(new_width, new_height)))
                    res = cv2.resize(img, dsize=(new_width, new_height))
                    cv2.imwrite("./output_carv.jpg", res)
                else:
                    carver = SeamCarver(img, new_height, new_width)
                    cv2.imshow('resize', cv2.resize(img, dsize=(new_width, new_height)))
                    res = cv2.resize(img, dsize=(new_width, new_height))
                    cv2.imwrite("./output_carv.jpg", res)
            else:
                carver = SeamCarver(img, new_height, new_width)
                cv2.imshow('resize', cv2.resize(img, dsize=(new_width, new_height)))
                res = cv2.resize(img, dsize=(new_width, new_height))
                cv2.imwrite("./output_carv.jpg", res)
