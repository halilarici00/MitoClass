import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import json
from PIL import Image, ImageDraw


# Load the image
image_path = "030.tiff"
image = Image.open(image_path)
print(image.size)
# Load the detection results from the JSON file
json_file = "mitotic-figures.json"
with open(json_file, "r") as f:
    detection_results = json.load(f)

# Get the detection results for the image
detections = detection_results.get(image_path, {}).get("points", [])

# Define the size of the region in millimeters
region_size_mm = 2

# Image resolution
image_resolution = (7215, 5412)  # Image resolution in pixels

# Convert region size from millimeters to pixels
region_size_px = (int(region_size_mm * (image_resolution[0] / image.width)),
                  int(region_size_mm * (image_resolution[1] / image.height)))
print(region_size_px)
# Define the size of the cropped region in pixels
cropped_size_px = (50, 50)

# Create a directory to save the cropped images
output_dir = "cropped_images"
os.makedirs(output_dir, exist_ok=True)

# Plot the image with bounding boxes
#plt.figure(figsize=(image_resolution[0] / 100, image_resolution[1] / 100))
#print("Figure size:", plt.gcf().get_size_inches())
#plt.imshow(image, extent=[0, image_resolution[0], 0, image_resolution[1]])
image_with_boxes=image.copy()
draw = ImageDraw.Draw(image_with_boxes)
# Add rectangles around the detected mitotic figures and save cropped images
for i, detection in enumerate(detections):
    x, y, _ = detection["point"]
    prob = detection["probability"]

    # Scale the coordinates
    x *= image_resolution[0]/2
    y *= image_resolution[1]/2
    #x=int(x)
    #y=int(y)
    print(x,y)
    # Define the bounding box for cropping
    x1 = max(0, int(x - cropped_size_px[0] / 2))
    y1 = max(0, int(y - cropped_size_px[1] / 2))
    x2 = min(image_resolution[0], int(x + cropped_size_px[0] / 2))
    y2 = min(image_resolution[1], int(y + cropped_size_px[1] / 2))

    # Add the rectangle patch
    draw.rectangle([(x1, y1), (x2, y2)],outline="red", width=4)
    #rect = patches.Rectangle((x1, y1), x2 - x1, y2 - y1,
    #                         linewidth=2, edgecolor="r", facecolor="none")
    #plt.gca().add_patch(rect)

    # Save the cropped image
    if x2 > x1 and y2 > y1:  # Ensure valid dimensions for cropping
        print(x1,y1,x2,y2)
        cropped_image = image_with_boxes.crop((x1, y1, x2, y2))
        cropped_image_path = os.path.join(output_dir, f"cropped_image_{i}.tiff")
        cropped_image.save(cropped_image_path, format="TIFF")

        # Add probability text
        draw.text((x2, y1), f"Prob: {prob:.2f}", fill="red")
        #plt.text(x2, y1, f"Prob: {prob:.2f}", fontsize=16, color="r")




#plt.title("Detected Mitotic Figures")
#plt.axis("off")
# Save the image with bounding boxes as TIFF
#output_image_path = "output_image_with_boxes.tiff"
output_image_path2 = "output_image_with_boxes2.tiff"
#plt.savefig(output_image_path, format="TIFF", bbox_inches='tight', pad_inches=0)
image_with_boxes.save(output_image_path2, format="TIFF")

#plt.show()
#print("Plot dimensions:", plt.gcf().get_size_inches() * plt.gcf().dpi)
print("Image dimensions:", image_with_boxes.size)
