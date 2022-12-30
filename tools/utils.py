import urllib.request
import numpy as np
import cv2


def url_to_image(url):
	resp = urllib.request.urlopen(url)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)
	return image

def crop_nail_id(cropped_id: str):
    return cropped_id.split("(")[0]