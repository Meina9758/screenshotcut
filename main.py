import os
import cv2

def process_images_in_folder(input_folder, output_folder, cropped_folder):
    # Create the output and cropped folders if they don't exist
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(cropped_folder, exist_ok=True)

    # Iterate over the files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.png') or filename.endswith('.jpg')or filename.endswith('.JPG')or filename.endswith('.PNG'):
            # Construct the full input file path
            input_file_path = os.path.join(input_folder, filename)

            # Process the image using the cut() function
            output_image, cropped_image = cut(input_file_path)

            # Construct the full output file paths
            output_file_path = os.path.join(output_folder, filename)
            cropped_file_path = os.path.join(cropped_folder, filename)

            # Save the output image
            cv2.imwrite(output_file_path, output_image)

            # Save the cropped image
            cv2.imwrite(cropped_file_path, cropped_image)

def cut(image_path):
    # Read the image
    image = cv2.imread(image_path)

    # Convert the image to RGB color space
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Define the threshold color
    threshold_color = (234, 234, 234)

    # Create the threshold mask
    threshold_mask = cv2.inRange(image_rgb, threshold_color, (255, 255, 255))

    # Find contours
    contours, _ = cv2.findContours(threshold_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour
    max_contour = max(contours, key=cv2.contourArea)

    # Calculate the bounding box of the largest contour
    x, y, w, h = cv2.boundingRect(max_contour)

    # Draw the largest rectangle on the image
    output_image = cv2.rectangle(image.copy(), (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Crop the image based on the bounding rectangle
    cropped_image = image[y:y+h, x:x+w]

    return output_image, cropped_image

# Specify the input folder path containing the images
input_folder = 'images'

# Specify the output folder path to save the result images
output_folder = 'output'

# Specify the cropped folder path to save the cropped images
cropped_folder = 'cropped'

# Process the images in the input folder and save the results
process_images_in_folder(input_folder, output_folder, cropped_folder)
