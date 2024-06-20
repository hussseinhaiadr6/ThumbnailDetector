from ultralytics import YOLO

def inference(source_file):
  model = YOLO("./weights/best.pt")  # load a custom model
  results = model.predict(source_file, iou=0.5, conf=0.01)
  return results


