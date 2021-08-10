import os
import cv2

def compression (image_name):
    file_name, fileExtension = os.path.splitext(image_name) #확장자 분리

    toJpg = image_name.replace(fileExtension, '.jpg') #확장자를 jpg로 변경
    toPng = image_name.replace(fileExtension, '.png') #확장자를 Png로 변경

    image = cv2.imread(image_name)
    if fileExtension == '.jpg':  #이미지 확장자별 분류 : jpg
        cv2.imwrite(toJpg, image, [cv2.IMWRITE_JPEG_QUALITY, 35])  # 0~100 품질 jpg -> jpg
    elif fileExtension == '.png': #이미지 확장자별 분류 : png
        cv2.imwrite(toPng, image, [cv2.IMWRITE_PNG_COMPRESSION, 9])  # 0 ~9, 압축율 png -> png
        cv2.imwrite(toJpg, image, [cv2.IMWRITE_JPEG_QUALITY, 35])  # 0~100 품질 png -> jpg
    else : #이미지 확장자별 분류 : 기타 확장자는 jpg로 변경
        cv2.imwrite(toJpg, image, [cv2.IMWRITE_JPEG_QUALITY, 35])  # 0~100 품질 else -> jpg
