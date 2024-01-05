import geopandas as gpd
from shapely.geometry import Polygon
import matplotlib.pyplot as plt


def plotter() -> None:
    # Create a square
    square = gpd.GeoDataFrame(geometry=[Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])])

    # Plot the original and rotated squares in one figure
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    # Plot the original square
    square.plot(ax=axes[0], edgecolor='black')
    axes[0].set_title('Original Square')

    # Rotate the square by 45 degrees
    square_rotated = square.rotate(angle=45, origin='center')

    # Plot the rotated square
    square_rotated.plot(ax=axes[1], edgecolor='black')
    axes[1].set_title('Rotated Square (45 degrees)')

    # Add a title to the entire figure
    fig.suptitle('Transformation: Original to Rotated (45 degrees)')

    # Save the combined plot as an image file
    plt.savefig('combined_transformation.png')
    plt.show()
