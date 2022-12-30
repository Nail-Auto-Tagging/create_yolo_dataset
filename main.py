import cv2
from tools.utils import url_to_image, crop_nail_id
from tools.db import (
    get_nail_image_from_naily,
    get_yolo_tagged_data_from_nailedit,
)


if __name__ == "__main__":
    # 1. nailedit DB에서 태깅완료된 데이터들 조회
    cropped_nails = get_yolo_tagged_data_from_nailedit()

    # 2. nail_id 기준으로 bounding_box들과 colors 정보 저장
    nail_dict = {}
    for cropped_nail in cropped_nails:
        try:
            nail_id = crop_nail_id(cropped_nail["cropped_id"])
            bounding_box = cropped_nail["bounding_box"]
            classes = cropped_nail["categories"]

            if nail_id not in nail_dict:
                nail_dict[nail_id] = []

            nail_dict[nail_id].append({"bounding_box": bounding_box, "classes": classes})
        except Exception as e:
            print(e.__str__())
            continue

    for nail_id, values in nail_dict.items():
        try:
            # 3. naily DB에서 nail_id에 해당하는 images 다운로드
            nail = get_nail_image_from_naily(nail_id)
            image_uri = nail["thumb_image"]
            image = url_to_image(image_uri)
            (H, W) = image.shape[:2]
            cv2.imwrite(f"yolo/images/{nail_id}.jpg", image)

            # 4. 손 이미지와 라벨링 텍스트 파일을 각각 저장
            f = open(f"yolo/labels/{nail_id}.txt", mode="w")
            for value in values:
                classes = value["classes"]
                width = value["bounding_box"]["width"]
                height = value["bounding_box"]["height"]
                mid_x = value["bounding_box"]["mid_x"]
                mid_y = value["bounding_box"]["mid_y"]
                for c in classes:
                    f.write(f"{c} {mid_x/W} {mid_y/H} {width/W} {height/H}\n")
            f.close()
        except Exception as e:
            print(e.__str__())
            continue
