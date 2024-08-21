import cairosvg
import cv2

# def png_to_pgm(input_png_path, output_pgm_path):
#     png = cv2.imread(input_png_path)
#     grayscale_png = cv2.cvtColor(png, cv2.COLOR_BGR2GRAY)
#     cv2.imwrite(output_pgm_path, grayscale_png)


def svg_to_png(svg_file_path, png_file_path, width, height):
    png_data = cairosvg.svg2png(
        url=svg_file_path, output_width=width, output_height=height
    )

    with open(png_file_path, "wb") as f:
        f.write(png_data)


if __name__ == "__main__":
    original_size = (1800, 1037)
    ratio = 0.5
    new_size = (int(original_size[0] * ratio), int(original_size[1] * ratio))
    svg_file_path = "/home/ubuntu/Downloads/slam_state_vc.svg"
    png_file_path = "/home/ubuntu/Downloads/slam_state_vc.png"
    # pgm_file_path = "/home/ubuntu/Downloads/slam_state_vb.pgm"

    svg_to_png(svg_file_path, png_file_path, new_size[0], new_size[1])
    # png_to_pgm(png_file_path, pgm_file_path)
