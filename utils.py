import os
import geopandas as gpd
from typing import List, Tuple, Dict, Callable
import numpy as np
import matplotlib.pyplot as plt
from shapely import Polygon
import random
import math


SCRIPT_DIR = os.path.dirname(__file__)


def create_random_polygon(num_vertices: int) -> gpd.GeoDataFrame:
    # Generate random x and y coordinates
    x_coords: List[float] = np.random.rand(num_vertices)
    y_coords: List[float] = np.random.rand(num_vertices)

    # Create a Polygon using the coordinates
    polygon = Polygon(zip(x_coords, y_coords))

    # Ensure polygon validity
    polygon = polygon.buffer(0)
    return polygon


def create_regular_polygon(
    num_vertices: int,
    center_limit: Tuple[float] = (-100, 100),
    radius_limit: Tuple[float] = (1, 1000),
) -> Polygon:
    # Generate random center coordinates within the specified range
    center: Tuple[float, float] = (
        random.uniform(center_limit[0], center_limit[1]),
        random.uniform(center_limit[0], center_limit[1]),
    )

    # Generate random radius within the specified range
    radius: float = random.uniform(radius_limit[0], radius_limit[1])

    # Calculate coordinates for a regular polygon with a dynamic center and size
    angle: float = 2 * math.pi / num_vertices
    coords: List[Tuple[float, float]] = [
        (
            center[0] + radius * math.cos(i * angle),
            center[1] + radius * math.sin(i * angle),
        )
        for i in range(num_vertices)
    ]

    # Create closed polygon
    coords.append(coords[0])
    polygon = Polygon(coords)
    return polygon


FUNCTION_MAPPING: Dict[str, Callable] = {
    "random": create_random_polygon,
    "regular": create_regular_polygon,
}


def n_log_n_function(x, a):
    return a * x * np.log(x)


def save_current_plot_to_file(output_directory: str, file_name: str) -> None:
    target_dir: str = os.path.join(SCRIPT_DIR, output_directory)

    # validate if directory exists
    if not os.path.isdir(target_dir):
        os.makedirs(target_dir)

    # Save the current plot as png
    plt.savefig(f"{target_dir}/{file_name}.png")


def save_df_to_file(
    gdf: gpd.GeoDataFrame, output_directory: str, file_name: str
) -> None:
    target_dir: str = os.path.join(SCRIPT_DIR, output_directory)

    # validate if directory exists
    if not os.path.isdir(target_dir):
        os.makedirs(target_dir)

    # Save the dataframe as csv
    gdf.to_csv(f"{target_dir}/{file_name}.csv", index=False)
