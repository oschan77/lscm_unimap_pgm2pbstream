import cv2


def convert_to_black_and_white(input_filename, output_filename, threshold):
    # Read the grayscale image
    image = cv2.imread(input_filename, cv2.IMREAD_GRAYSCALE)

    if image is None:
        raise FileNotFoundError(f"File {input_filename} not found or not a valid image")

    # Apply the threshold to create a binary image
    _, bw_image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)

    # Save the output image
    cv2.imwrite(output_filename, bw_image)


if __name__ == "__main__":
    input_filename = "/home/ubuntu/Downloads/Ogm2Pgbm/workspace/lab2d_vectorized/lab2d_vectorized.pgm"
    output_filename = "/home/ubuntu/Downloads/Ogm2Pgbm/workspace/lab2d_vectorized/lab2d_vectorized_bw.pgm"
    threshold = 128  # You can adjust the threshold value (0-255)

    convert_to_black_and_white(input_filename, output_filename, threshold)
