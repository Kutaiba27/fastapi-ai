from typing import Annotated
import cv2
from fastapi import Depends
import pickle
from ..database.databaseConnition import get_db
from sqlalchemy.orm import Session
from ..database.models import Features

def keypoints_to_array(keypoints):
   keypoints_array = []
   for kp in keypoints:
      kp_as_list = (kp.pt, kp.size, kp.angle, kp.response, kp.octave, kp.class_id)
      keypoints_array.append(kp_as_list)
   return keypoints_array


def save_features_to_db(idProduct, keypoints, db: Session):
   keypoints_blob = pickle.dumps(keypoints)
   details = {'keypoints': keypoints_blob, 'id_image': idProduct}
   features = Features(**details)
   db.add(features)
   db.commit()
   db.refresh(features) 
   
def saveImage(image, id, db: Session):
   keypoints, descriptors = cv2.SIFT_create().detectAndCompute(image, None)
   save_features_to_db(id, descriptors, db)