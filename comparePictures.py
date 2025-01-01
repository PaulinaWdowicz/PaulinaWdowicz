#The script compares two images pixel by pixel and checks the percentage difference.

from PIL import Image, ImageChops

# Put the file`s path
file1_path = input("Put the first's image path: ")
file2_path = input("Put the second`s image path: ")

def compare_images(file1_path, file2_path, output_diff_path=None):
    """
    Argumetss:
        file1_path (str): The first image path.
        file2_path (str): The second image path.
        output_diff_path (str, optional): Path to save the difference image. If None, no image is saved.
    
    Returns:
        float: Percentage of different pixels.
    """

    # Open images
    image1 = Image.open(file1_path).convert('RGB')
    image2 = Image.open(file2_path).convert('RGB')

    # Check if both images have the same size
    if image1.size != image2.size:
        raise ValueError("Images have different sizes: {} vs {}".format(image1.size, image2.size))

    # Compare pixels in pictures
    imageWidth, imageHeight = image1.size
    different_pixels = 0

    # Create a difference image
    difference_image = ImageChops.difference(image1, image2)

    # Count differences of pixels
    for y in range(imageHeight):
        for x in range(imageWidth):
            pixel1 = image1.getpixel((x, y))
            pixel2 = image2.getpixel((x, y))
            if pixel1 != pixel2:
                different_pixels += 1

    # Percentage difference of pixels
    all_pixels = imageWidth * imageHeight
    difference_percentage = (different_pixels / all_pixels) * 100
    print("Difference percentage: {:.2f}%".format(difference_percentage))

    # Save the difference image if requested
    if output_diff_path:
        difference_image.save(output_diff_path)
    return difference_percentage

compare_images(file1_path, file2_path, output_diff_path=None)