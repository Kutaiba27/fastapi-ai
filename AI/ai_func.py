
import cv2
import pickle
from sqlalchemy.orm import Session
from ..database.models import Features

def prdict(model, img_recized):
    # pretrained YOLOv8n model
    results = model.predict(
        source=img_recized,
        show=False,
        save=True,
        conf=0.8,
        verbose=False,
        imgsz=640,
        show_labels=False,
        show_conf=False,
    )

    return results


def extract_sift_features_from_image(image):
    query_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sift = cv2.SIFT_create()
    query_keypoints, query_descriptors = sift.detectAndCompute(query_img, None)
    return  query_descriptors


def match_sift_features(
    query_descriptors, sift_features_list, threshold=0.7
):
    bf = cv2.BFMatcher()
    best_match = None
    max_matches = 0
    for features in sift_features_list:
        stored_descriptors = features["keypoints"]
        matches = bf.knnMatch(query_descriptors, stored_descriptors, k=2)
        good_matches = []
        for m, n in matches:
            if m.distance < threshold * n.distance:
                good_matches.append(m)
        if len(good_matches) > max_matches:
            max_matches = len(good_matches)
            best_match = features

    return best_match


def drow_label(imge, results):
    text = "Medicine box"
    image = imge
    boxes = results[0].boxes.xyxy.tolist()
    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = box
        start_point = (int(x1), int(y2))
        start_point_text = (int(x1), int(y1))
        end_point = (int(x2), int(y1))
        new_end_point = (int(x2), int((y1 - 25)))
        color = (255, 0, 0)
        text_color = (255, 255, 1)
        thickness = 2
        fontFace = cv2.FONT_HERSHEY_DUPLEX
        fontScale = 1
        thickness1 = 1
        image = cv2.rectangle(image, start_point, end_point, color, thickness)
        image = cv2.rectangle(image, start_point_text, new_end_point, color, -1)
        image = cv2.putText(
            image,
            text,
            start_point_text,
            fontFace,
            fontScale,
            text_color,
            thickness1,
            lineType=cv2.LINE_AA,
        )
    return image


def crop_object(results, img):
    list_of_object = []
    boxes = results[0].boxes.xyxy.tolist()
    if len(boxes) == 0:
        list_of_object.append(img)
        return list_of_object
    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = box
        cropped_image = img[int(y1) : int(y2), int(x1) : int(x2)]
        gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        list_of_object.append(
            {
                "crops": cropped_image,
                "box": [int(x1), int(y1), int(x2), int(y2)],
                "class": 0,
            }
        )
    return list_of_object


def get_all_features_from_db(db: Session):
    
    c = db.query(Features).all()
    features = []
    for row in c:
        id_image = row.id_image
        keypoints = pickle.loads(row.keypoints)
        features.append({"id_image": id_image, "keypoints": keypoints})
    return features


def counting(list_of_object, database_features):
    sku_count = dict()
    for object in list_of_object:
        des = extract_sift_features_from_image(object["crops"])
        best_match = match_sift_features(des, database_features)
        if best_match is not None:
            sku  = best_match["id_image"]
            object["class"] = sku
            if best_match["id_image"] in sku_count:
                sku_count[sku] += 1
            else:
                sku_count[sku] = 1
    return sku_count
