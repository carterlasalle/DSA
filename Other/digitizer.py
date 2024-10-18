import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button
from PIL import Image
import pandas as pd
from scipy.ndimage import median_filter

# Function to load the image (specify the path directly)
def load_image(image_path):
    return Image.open(image_path)

# Function to select regions and collect numerical inputs using matplotlib widgets
def select_points_and_values(image):
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.imshow(image)
    plt.axis('off')

    regions = {}
    axis_values = {}
    clicks = []
    prompts = [
        ('heatmap', 'Select top-left and bottom-right corners of the heatmap region'),
        ('colorbar', 'Select top and bottom points of the colorbar'),
        ('x_axis', 'Select two known points along the x-axis (e.g., tick marks)'),
        ('y_axis', 'Select two known points along the y-axis (e.g., tick marks)'),
    ]
    current_prompt = [0]  # Using list to make it mutable in nested function

    def onclick(event):
        if event.inaxes == ax:
            key, prompt = prompts[current_prompt[0]]
            clicks.append((event.xdata, event.ydata))
            ax.plot(event.xdata, event.ydata, 'ro', markersize=5)
            fig.canvas.draw()
            if len(clicks) == 2:
                regions[key] = clicks.copy()
                clicks.clear()
                current_prompt[0] += 1
                if current_prompt[0] < len(prompts):
                    key, prompt = prompts[current_prompt[0]]
                    ax.set_title(prompt)
                else:
                    fig.canvas.mpl_disconnect(cid)
                    plt.close(fig)

    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    key, prompt = prompts[current_prompt[0]]
    ax.set_title(prompt)
    plt.show()

    # Now collect numerical inputs using TextBox widgets
    values = {}
    num_inputs = [
        ('x_min', 'First x-axis value:'),
        ('x_max', 'Second x-axis value:'),
        ('y_min', 'First y-axis value:'),
        ('y_max', 'Second y-axis value:'),
        ('colorbar_min', 'Bottom colorbar value:'),
        ('colorbar_max', 'Top colorbar value:'),
    ]

    fig_inputs, ax_inputs = plt.subplots(figsize=(6, len(num_inputs)*1.5))
    plt.subplots_adjust(bottom=0.2, top=0.8)
    text_boxes = []

    for i, (key, label) in enumerate(num_inputs):
        ax_box = plt.axes([0.25, 0.8 - i*0.1, 0.5, 0.05])
        text_box = TextBox(ax_box, label)
        text_boxes.append((key, text_box))

    # Add a submit button
    submit_ax = plt.axes([0.4, 0.05, 0.2, 0.075])
    button = Button(submit_ax, 'Submit')

    def submit(event):
        for key, text_box in text_boxes:
            value_str = text_box.text
            try:
                values[key] = float(value_str)
            except ValueError:
                print(f"Invalid input for {key}. Please enter a numerical value.")
                return
        plt.close(fig_inputs)

    button.on_clicked(submit)
    plt.show()

    if len(values) != len(num_inputs):
        print("Failed to collect all inputs.")
        return None, None

    return regions, values

# The rest of the functions remain the same
def map_colors_to_values(colorbar_region, colorbar_min, colorbar_max):
    height, _, _ = colorbar_region.shape
    colorbar_pixels = colorbar_region[:, 0, :]  # Use the first column of pixels
    # Map color values from colorbar_max to colorbar_min to match image orientation
    color_values = np.linspace(colorbar_max, colorbar_min, height)
    return colorbar_pixels, color_values

def map_heatmap_to_values(heatmap_region, colorbar_pixels, color_values):
    # Apply median filter to reduce the impact of gridlines
    filtered_heatmap = median_filter(heatmap_region, size=3)

    # Reshape arrays for vectorized computation
    heatmap_pixels = filtered_heatmap.reshape(-1, 3)
    distances = np.linalg.norm(heatmap_pixels[:, None, :] - colorbar_pixels[None, :, :], axis=2)
    indices = np.argmin(distances, axis=1)
    heatmap_values = color_values[indices].reshape(filtered_heatmap.shape[:2])
    return heatmap_values

def digitize_heatmap():
    # Specify the image path directly
    image_path = 'path_to_your_image.png'  # Replace with your image path
    image = load_image(image_path)
    image_array = np.array(image)

    regions, values = select_points_and_values(image)
    if regions is None or values is None:
        print("Failed to collect all inputs.")
        return

    pts_heatmap = regions['heatmap']
    pts_colorbar = regions['colorbar']
    pts_x_axis = regions['x_axis']
    pts_y_axis = regions['y_axis']

    # Crop the regions
    x1, y1 = map(int, pts_heatmap[0])
    x2, y2 = map(int, pts_heatmap[1])
    heatmap_region = image_array[int(y1):int(y2), int(x1):int(x2), :3]

    cx1, cy1 = map(int, pts_colorbar[0])
    cx2, cy2 = map(int, pts_colorbar[1])
    colorbar_region = image_array[int(cy1):int(cy2), int(cx1):int(cx2), :3]

    # Get axis numerical values
    x_min = values['x_min']
    x_max = values['x_max']
    y_min = values['y_min']
    y_max = values['y_max']
    colorbar_min = values['colorbar_min']
    colorbar_max = values['colorbar_max']

    # Map colors to values
    colorbar_pixels, color_values = map_colors_to_values(colorbar_region, colorbar_min, colorbar_max)

    # Map heatmap to values
    heatmap_values = map_heatmap_to_values(heatmap_region, colorbar_pixels, color_values)

    # Calculate axis scales
    x_axis_pixel_values = [pts_x_axis[0][0], pts_x_axis[1][0]]  # x-coordinates
    y_axis_pixel_values = [pts_y_axis[0][1], pts_y_axis[1][1]]  # y-coordinates

    x_pixel_range = x_axis_pixel_values[1] - x_axis_pixel_values[0]
    y_pixel_range = y_axis_pixel_values[1] - y_axis_pixel_values[0]

    # Compute scaling factors
    x_scale = (x_max - x_min) / x_pixel_range
    y_scale = (y_max - y_min) / y_pixel_range

    # Map pixel positions to axis values
    height, width = heatmap_values.shape
    x_indices = np.arange(width)
    y_indices = np.arange(height)

    x_pixels = x1 + x_indices
    y_pixels = y1 + y_indices

    x_values = x_min + (x_pixels - x_axis_pixel_values[0]) * x_scale
    y_values = y_min + (y_pixels - y_axis_pixel_values[0]) * y_scale

    # Correct for image coordinate system (if necessary)
    if y_values[0] > y_values[-1]:
        y_values = y_values[::-1]
        heatmap_values = heatmap_values[::-1, :]

    # Show the resulting heatmap values
    df = pd.DataFrame(heatmap_values, index=y_values, columns=x_values)
    print("Heatmap Values (2D Array with axis values):")
    print(df)

    # Return 3D array
    X, Y = np.meshgrid(x_values, y_values)
    heatmap_3d = np.dstack((X, Y, heatmap_values))

    print("Heatmap as 3D Array:")
    print(heatmap_3d.shape)

    return heatmap_3d, (x_min, x_max), (y_min, y_max), x_values, y_values

if __name__ == "__main__":
    heatmap_3d, x_range, y_range, x_values, y_values = digitize_heatmap()
