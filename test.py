from matplotlib import pyplot as plt
from ultralytics import YOLO
import cv2

model_path = "C:/Users\Lenovo/runs\pose/train4\weights\last.pt"

image_path = 'data/images/test/Image_1.jpg'
img = cv2.imread(image_path)
h, w, _ = img.shape

model = YOLO(model_path)

results = model(image_path, conf=0.5, iou=0.4)[0]
print(results.keypoints)
print('____________________________________________')



for result in results:
    for bbox in result.boxes:
        # normalizing the coordinates (x_center, y_center, width, height)
        x_center, y_center, width, height = bbox.xywh[0].tolist()

        # converting to real pixel coordinates
        x1 = int((x_center - width / 2) * w)
        y1 = int((y_center - height / 2) * h)
        x2 = int((x_center + width / 2) * w)
        y2 = int((y_center + height / 2) * h)

        # drawing the bbox
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

    for keypoint_indx, keypoint in enumerate(result.keypoints.xy[0]):  # Используем индекс [0] для получения всех точек
        x, y = keypoint[0].item(), keypoint[1].item()  # Преобразуем координаты в числа
        print(keypoint_indx, x, y)

        # showing the keypoint indexes
        cv2.putText(img, str(keypoint_indx), (int(x), int(y)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# displaying the result
plt.imshow(image_rgb)
plt.axis('off')
plt.show()