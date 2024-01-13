import time
import random
from typing import List, Tuple

import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from tqdm import tqdm
import os
import numpy as np
import geopandas as gpd
import math


SCRIPT_DIR = os.path.dirname(__file__)
ANALYSIS_DIR = os.path.join(SCRIPT_DIR, "analysis")


def save_current_plot_to_file(output_directory: str, file_name: str) -> None:
    target_dir: str = os.path.join(SCRIPT_DIR, output_directory)

    # validate if directory exists
    if not os.path.isdir(target_dir):
        os.makedirs(target_dir)

    # Save the current plot as png
    plt.savefig(f"{target_dir}/{file_name}.png")


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
    center_limit: Tuple[float] = (-10, 10),
    radius_limit: Tuple[float] = (1, 100),
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


def analyse(args) -> None:
    input_params: List[Tuple[int, int]] = []
    for i in range(args.iterations):
        input_params.append((args.shapes, args.vertices))

        # Update number of shapes and vertices for the next iteration
        args.shapes += args.shape_increment
        args.vertices += args.vertex_increment

    execution_times: List[float] = []

    for num_shapes, num_vertices in tqdm(input_params):
        # Generate n polygons with k vertices
        gdf = gpd.GeoDataFrame(
            geometry=[
                create_random_polygon(num_vertices)
                for _ in tqdm(range(num_shapes), desc="Generating polygons")
            ]
        )

        # Measure execution time
        start_time: float = time.time()
        gdf.unary_union
        end_time: float = time.time()
        execution_time: float = end_time - start_time
        execution_times.append(execution_time)

    # Plot the results
    total_vertices: List[int] = [t[0] * t[1] for t in input_params]
    plt.scatter(total_vertices, execution_times, marker="o")
    plt.xlabel("Total number of vertices")
    plt.ylabel("Execution time (seconds)")
    plt.title("Time Complexity Analysis")

    save_current_plot_to_file(f"{args.output_dir}/{ANALYSIS_DIR}", "test")
    plt.close()
