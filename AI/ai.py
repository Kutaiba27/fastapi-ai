
from ultralytics import YOLO

def load_model():
   return YOLO("/home/kutaiba/main/pyserver/AI/epoch20.pt")

model = load_model()
# orignal = cv2.imread("s2.jpg")
# result = prdict(model, orignal)
# ims = drow_label(orignal, result)
# cv2.imshow("Clustered Image", ims)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# list_of_object = crop_object(result, orignal)
# len(list_of_object)
# database_features = get_all_features_from_db("sift.db")
# count = counting(list_of_object, database_features)
