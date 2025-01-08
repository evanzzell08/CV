import os
from xml.dom import minidom

# Define the output directory
out_dir = 'cvat_annotations'
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

# Parse the XML file
file = minidom.parse('annotations.xml')

# Get all image elements
images = file.getElementsByTagName('image')

# Loop through each image
for image in images:
    width = int(image.getAttribute('width'))
    height = int(image.getAttribute('height'))
    name = image.getAttribute('name')

    # Get the points and box elements
    elem = image.getElementsByTagName('points')
    bbox = image.getElementsByTagName('box')[0]

    # Extract the bounding box coordinates
    xtl = int(float(bbox.getAttribute('xtl')))
    ytl = int(float(bbox.getAttribute('ytl')))
    xbr = int(float(bbox.getAttribute('xbr')))
    ybr = int(float(bbox.getAttribute('ybr')))
    w = xbr - xtl
    h = ybr - ytl

    # Open the output label file for writing
    label_file = open(os.path.join(out_dir, name[:-4] + '.txt'), 'w')

    # Process each points element
    for e in elem:
        # Get the 'occluded' attribute
        # occluded = e.getAttribute('occluded')
        occluded = 2

        # Write the label and normalized bounding box coordinates
        label_file.write('0 {} {} {} {} '.format(
            str((xtl + (w / 2)) / width),
            str((ytl + (h / 2)) / height),
            str(w / width),
            str(h / height)))

        # Process the points
        points = e.attributes['points']
        points = points.value.split(';')
        points_ = []
        for p in points:
            p = p.split(',')
            p1, p2 = p
            points_.append([int(float(p1)), int(float(p2))])

        # Write the normalized points with the 'occluded' value
        for p_, p in enumerate(points_):
            label_file.write('{} {} {}'.format(p[0] / width, p[1] / height, occluded))  # Add occluded after each point
            if p_ < len(points_) - 1:
                label_file.write(' ')
            else:
                label_file.write('\n')
