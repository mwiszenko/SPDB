import time
from typing import List, Tuple, Callable

import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np
from scipy.optimize import curve_fit
import geopandas as gpd

from utils import FUNCTION_MAPPING, n_log_n_function, save_current_plot_to_file

ANALYSIS_DIR = "analysis"


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

        generation_args: List = []

        if args.generation_mode == "regular":
            generation_args = [num_vertices]
        elif args.generation_mode == "random":
            generation_args = [num_vertices]

        generation_method: Callable = FUNCTION_MAPPING[args.generation_mode]

        gdf = gpd.GeoDataFrame(
            geometry=[
                generation_method(*generation_args)
                for _ in tqdm(range(num_shapes), desc="Generating polygons")
            ]
        )

        # Measure average execution time
        single_execution_times: List[float] = []
        for i in range(args.aggregations):
            start_time: float = time.time()
            gdf.unary_union
            end_time: float = time.time()
            execution_time: float = end_time - start_time
            single_execution_times.append(execution_time)
        execution_times.append(sum(single_execution_times) / len(single_execution_times))

    # Plot the results
    total_vertices: List[int] = [t[0] * t[1] for t in input_params]
    plt.scatter(total_vertices, execution_times, marker="o")
    plt.xlabel("Total number of vertices")
    plt.ylabel("Execution time (seconds)")
    plt.title("Unary union (Time complexity)")

    # Fit the non-linear function to the data
    params, covariance = curve_fit(n_log_n_function, total_vertices, execution_times)
    # Extract the fitted parameters
    a_fit = params
    # Generate y values for the fitted curve
    y_fit = n_log_n_function(np.array(total_vertices), a_fit)
    plt.plot(total_vertices, y_fit, label="Best-fit curve", color="red")
    plt.legend()

    save_current_plot_to_file(
        f"{args.output_dir}/{ANALYSIS_DIR}", "unary_union-complexity"
    )
    plt.close()
