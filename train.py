from ultralytics import YOLO

# Loading a model
model = YOLO("yolo11n-pose.pt")

# Training the model
results = model.train(
    data="config.yaml",
    batch=8,
    epochs=1500,
    multi_scale=True,
    imgsz=224,
    plots=True,
    single_cls=True,
    degrees=30.0, # degree range to rotate the image randomly
    patience=300,  # number of epochs for early stopping
    bgr=0.2, # color channel flipping probability
    erasing=0.4, # random erasing probability
    flipud=0.3, # vertical flipping probability
    nbs=32,  # normalized batch size
    mosaic=0.5,  # combining multiple images into one probability
    pose=18.0,  # pose-specific augmentation index
    kobj=3.0,  # object-related augmentation index
    iou=0.4,  # iou threshold for training
    conf=0.5  # confidence threshold for training
)