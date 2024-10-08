#Advance Image Manipulation and Enhancement Using Python

## Importing the necessary libraries
"""

import pandas as pd
import numpy as np
import cv2
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

"""## Loading the image"""

image_path = '/content/ZEBRA.jpg'
image = cv2.imread(image_path)

from google.colab.patches import cv2_imshow
cv2_imshow(image)

print(image.shape)

"""## 1. Image Transformation: Rotation, Cropping, and Resizing

###Rotate an image by 45°, 90°, and 180° using OpenCV.
"""

height, width = image.shape[:2]

def rotate_image(image, angle):
    # Calculate the center of the image
    center = (width/2, height/2)

    # Get the rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

    # Calculate the sine and cosine of the angle
    abs_cos = abs(rotation_matrix[0, 0])
    abs_sin = abs(rotation_matrix[0, 1])

    # Compute the new bounding dimensions of the image
    new_width = int(height * abs_sin + width * abs_cos)
    new_height = int(height * abs_cos + width * abs_sin)

    # Adjust the rotation matrix to account for the translation
    rotation_matrix[0, 2] += (new_width / 2) - center[0]
    rotation_matrix[1, 2] += (new_height / 2) - center[1]

    # Perform the rotation
    rotated_image = cv2.warpAffine(image, rotation_matrix, (new_width, new_height))
    return rotated_image

# Rotate by 45 degrees
rotated_image45 = rotate_image(image, 45)
cv2_imshow(rotated_image45)

# Rotate by 90 degrees
rotated_image90 = rotate_image(image, 90)
cv2_imshow(rotated_image90)

# Rotate by 180 degrees
rotated_image180 = rotate_image(image, 180)
cv2_imshow(rotated_image180)

"""**Observations**:

1.   When i was rotating the image without considering the bounding dimensions of the image, resultant image was getting cropped.
2.   Rotation in image processing is used for correcting the orientation of photos, aligning images for comparison, or creating artistic effects.

###Crop a specific region from an image.
"""

# Define the coordinates for cropping
start_row, start_col = int(height * 0.25), int(width * 0.25)
end_row, end_col = int(height * 0.75), int(width * 0.75)

# Crop the image
cropped_image = image[start_row:end_row, start_col:end_col]
cv2_imshow(cropped_image)

"""**Observation :** Cropping in image processing means cutting out the unwanted outer parts of an image. This helps to focus on the important parts, improve the composition, or change the size and shape of the image.

###Resize the image to dimensions of 256x256 pixels and 512x512 pixels.
"""

# Resize to 256x256
resized_image256 = cv2.resize(image, (256, 256))
cv2_imshow(resized_image256)

# Resize to 512x512
resized_image512 = cv2.resize(image, (512, 512))
cv2_imshow(resized_image512)

"""**Observations :**

1.   Resizing an image means changing its width and height to make it larger or smaller. This is useful for fitting images into specific spaces, reducing file sizes, or preparing them for different uses.

1.  Resizing has lead to significant reduction in image quality.

## 2. Color Space Conversion

### Convert an image from RGB to HSV, Grayscale, and back to RGB.
"""

# Convert to HSV
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
cv2_imshow(hsv_image)

# Convert to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2_imshow(gray_image)

# Convert grayscale back to RGB
rgb_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)
cv2_imshow(rgb_image)

"""*   **Note :**

1.   HSV (Hue, Saturation, Value): Hue represents the color type (e.g., red, green, blue), Saturation indicates the intensity or purity of the color, Value refers to the brightness of the color.
2.   HSV is useful for color-based image processing tasks because it separates color information (hue) from intensity (value).

1.   Grayscale represents the image in shades of gray, with values ranging from black (0) to white (255), it only contains intensity information, not color.
2.   Grayscale image are used for edge detection and thresholding.




*   **Observations :**

1.   In the HSV colour space, I can observe the hue, saturation and value which is giving us a brief idea about the image's colours.
2.   In the grayscale colour space the edges of the foreground are much more prominent.

1.   We can't convert a grayscale image to RGB because grayscale image lacks colour information, it just contains intensity information.

##  3. Histogram Analysis

###Generate and plot the histogram of the original image and the grayscale version.
"""

# Calculate histogram for each channel of the original image
hist_original_b = cv2.calcHist([image], [0], None, [256], [0, 256]).flatten()
hist_original_g = cv2.calcHist([image], [1], None, [256], [0, 256]).flatten()
hist_original_r = cv2.calcHist([image], [2], None, [256], [0, 256]).flatten()

# Calculate histogram for grayscale image
hist_gray = cv2.calcHist([gray_image], [0], None, [256], [0, 256]).flatten()

# Plot histogram for each channel of the original image
fig_original_b = px.line(x=np.arange(256), y=hist_original_b, title='Histogram of Original Image - Blue Channel', labels={'x':'Pixel Intensity', 'y':'Frequency'})
fig_original_g = px.line(x=np.arange(256), y=hist_original_g, title='Histogram of Original Image - Green Channel', labels={'x':'Pixel Intensity', 'y':'Frequency'})
fig_original_r = px.line(x=np.arange(256), y=hist_original_r, title='Histogram of Original Image - Red Channel', labels={'x':'Pixel Intensity', 'y':'Frequency'})

fig_original_b.show()
fig_original_g.show()
fig_original_r.show()

# Plot histogram for grayscale image
fig_gray = px.line(x=np.arange(256), y=hist_gray, title='Histogram of Grayscale Image', labels={'x':'Pixel Intensity', 'y':'Frequency'})
fig_gray.show()

"""**Observation :**

1.   The x-axis represents the pixel intensity values, ranging from 0 - 255.
2.   The y-axis shows the number of pixels for each intensity value.

1.   The smaller peaks and variations throughout the histogram indicate different shades of colours are present in the image.

1.   The spread of the histogram indicates the contrast of the image.
2.   Comparing the red, blue and green channels indicates that the original image is overall colour balanced.

1.   Grayscale image : A notable peak is between intensity values of 150 to 200, suggesting a significant portion of the image is relatively bright. The spread of the histogram suggests that the image has a wide range of brightness levels, from dark to bright areas.

###Perform histogram equalization on the grayscale image to enhance its contrast, and plot the histogram of the enhanced image.
"""

# Perform histogram equalization
equalized_image = cv2.equalizeHist(gray_image)
cv2_imshow(equalized_image)

# Calculate histogram for equalized image
hist_equalized = cv2.calcHist([equalized_image], [0], None, [256], [0, 256]).flatten()

# Plot histogram for equalized image
fig_equalized = px.line(x=np.arange(256), y=hist_equalized, title='Histogram of Equalized Image', labels={'x':'Pixel Intensity', 'y':'Frequency'})
fig_equalized.show()

"""*   **Note :**

1.   Equalization is a technique used to improve the contrast of an image.It aims to distribute the pixel intensity values more evenly across the entire range, enhancing the overall contrast of the image.


*   **Observations :**

1.   In the image dark areas become lighter, and light areas become darker, making details more visible.
2.   The image appears more balanced in terms of brightness and contrast.

## 4. Image Filtering

###Apply the following filters to the grayscale version of an image and observe the changes :

1.   Guassian Blur
2.   Median Filter

1.   Sharpening Filter
"""

# Gaussian Blur
blurred_image = cv2.GaussianBlur(gray_image, (11, 11), 0)
cv2_imshow(blurred_image)

# Median Filter
median_filtered_image = cv2.medianBlur(gray_image, 11)
cv2_imshow(median_filtered_image)

# Sharpening Filter
kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
sharpened_image = cv2.filter2D(gray_image, -1, kernel)
cv2_imshow(sharpened_image)

"""*   **Note :**

1.   Gaussian Filter smooths the image, Median Filter reduces noise while preserving edges, and Sharpening Filter enhances edges and details.


*   **Observations :**







1.   In the first image where Guassian filter was applied, we were able to blur the image and reduce some noise but as a consequence, we lost the edge details.
2.   In the second image, a Median filter was applied to effectively reduce noise while preserving and highlighting the edges. That's why it is better in comparison to Guassian filter.

1.   In the third image, sharpening filter was applied to enhance the edges and details in the image, making them more prominent.

## 5. Combining Techniques

### Apply a combination of the above techniques to an image:

1.   Convert the image to Grayscale.
2.   Resize it to 300x300 pixels.

1.   Apply histogram equalization.
2.   Use Gaussian blur to smoothen the image.
"""

# Convert to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Resize to 300x300
resized_image = cv2.resize(gray_image, (300, 300))

# Apply histogram equalization
equalized_image = cv2.equalizeHist(resized_image)

# Apply Gaussian blur
blurred_imagen = cv2.GaussianBlur(equalized_image, (3,3), 0)

cv2_imshow(image)
cv2_imshow(blurred_imagen)

"""## Visualization Methods

### 1. Use scatter plots to visualize the relationships between pixel intensities before and after transformation.
"""

# Flatten the grayscale and blurred images to 1D arrays
gray_pixels = resized_image.flatten()
blurred_pixels = blurred_imagen.flatten()

# Create a scatter plot using Plotly Express
fig = px.scatter(x=gray_pixels, y=blurred_pixels,
                 labels={'x':'Gray Image Pixel Intensity', 'y':'Blurred Image Pixel Intensity'},
                 title='Relationship between Pixel Intensities of Gray and Blurred Images')
fig.show()

"""**Observations :**

1.   The scatter plot shows a positive correlation between the pixel intensities of gray and blurred images.
2.   The dense clustering of points along the line indicates that most pixel intensities in the gray image have corresponding similar intensities in the blurred image, reinforcing the consistency of the blurring effect.

### 2. Generate a pair plot to observe relationships between different channels of an image (e.g., R, G, B).
"""

df = pd.DataFrame(image.reshape(-1, 3), columns=['Blue', 'Green', 'Red'])
sns.pairplot(df)

"""**Observations :**

1.   The scatter plots show a positive correlation between the RGB channels.
2.   The width of the histogram in the diagonal of the pairplot indicates good contrast.

1.   All the 3 channels have high dynamic range.

### 3. Create box plots to show the distribution of pixel values before and after applying histogram equalization.
"""

# Create a DataFrame for the box plot
df = pd.DataFrame({'Original': resized_image.flatten(), 'Equalized': equalized_image.flatten()})

# Create a box plot using Plotly Express
fig = px.box(df, title='Distribution of Pixel Values Before and After Histogram Equalization')
fig.show()

"""**Observations :**

1.   The median value in the ‘Equalized’ boxplot has shifted compared to the ‘Original’ boxplot, indicating a change in the central tendency of pixel intensities.
2.   The IQR is wider in the ‘Equalized’ boxplot, showing that histogram equalization increases the spread of the middle 50% of pixel values, enhancing contrast.

1.   Histogram equalization has made the distribution more symmetric.
2.   Equalization has even removed the outliers from the original image.

1.   Longer whiskers in the ‘Equalized’ boxplot indicate a broader range of pixel intensities, reflecting an increased dynamic range.

### 4. Display histograms for the original and transformed images, particularly after color space conversion and filtering.

#### Histogram for Color Space Conversion already included in section 3.

#### **Note :** Histogram for filtering transformation
"""

# Calculate histogram for gray_image
hist_gray = cv2.calcHist([gray_image], [0], None, [256], [0, 256]).flatten()

# Calculate histogram for blurred_image
hist_blurred = cv2.calcHist([blurred_image], [0], None, [256], [0, 256]).flatten()

# Plot histogram for gray_image
fig_gray = px.line(x=np.arange(256), y=hist_gray, title='Histogram of Gray Image', labels={'x':'Pixel Intensity', 'y':'Frequency'})
fig_gray.show()

# Plot histogram for blurred_image
fig_blurred = px.line(x=np.arange(256), y=hist_blurred, title='Histogram of Blurred Image', labels={'x':'Pixel Intensity', 'y':'Frequency'})
fig_blurred.show()

"""**Observations :**

1.   Fine details and sharp edges are smoothed out, causing a decrease in the frequency of certain pixel intensities that were originally part of those details.

### 5. Compare the original and filtered images side-by-side using subplots to illustrate the impact of each filter.
"""

# Create a figure and subplots
fig, axs = plt.subplots(2, 2, figsize=(12, 12))

# Display the original image
axs[0, 0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
axs[0, 0].set_title('Original Image')
axs[0, 0].axis('off')

# Display the blurred image
axs[0, 1].imshow(blurred_image, cmap='gray')
axs[0, 1].set_title('Gaussian Blur')
axs[0, 1].axis('off')

# Display the median filtered image
axs[1, 0].imshow(median_filtered_image, cmap='gray')
axs[1, 0].set_title('Median Filter')
axs[1, 0].axis('off')

# Display the sharpened image
axs[1, 1].imshow(sharpened_image, cmap='gray')
axs[1, 1].set_title('Sharpening Filter')
axs[1, 1].axis('off')

# Adjust spacing between subplots
plt.tight_layout()

# Show the plot
plt.show()

"""**Note :** I have mentioned the observations for each filtered image in section 4.


"""
