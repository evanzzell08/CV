import json
import os

with open('person_keypoints_default.json') as f:
    data = json.load(f)

output_dir = 'yolo_annotations'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

category_map = {
    3: 0  # skeleton category
}

for image in data['images']:
    image_id = image['id']
    width = image['width']
    height = image['height']
    filename = image['file_name']

    annotations = [anno for anno in data['annotations'] if anno['image_id'] == image_id]

    txt_file = os.path.join(output_dir, f"{filename[:-4]}.txt")
    with open(txt_file, 'w') as f:
        for annotation in annotations:
            category_id = annotation['category_id']
            if category_id not in category_map:
                continue

            bbox = annotation['bbox']
            x_center = (bbox[0] + bbox[2]) / 2 / width
            y_center = (bbox[1] + bbox[3]) / 2 / height
            box_width = bbox[2] / width
            box_height = bbox[3] / height

            f.write(f"{category_map[category_id]} {x_center} {y_center} {box_width} {box_height}")

            keypoints = annotation['keypoints']
            num_keypoints = annotation['num_keypoints']
            keypoint_str = ''

            for i in range(0, len(keypoints), 3):
                x = keypoints[i] / width
                y = keypoints[i + 1] / height
                visibility = keypoints[i + 2]

                keypoint_str += f" {x} {y} {visibility}"

            if keypoint_str:
                f.write(f"{keypoint_str}")
            f.write('\n')

print("Convertion complete!")
