from typing import Dict
from tqdm import tqdm

import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
import math

from utils import save_df_to_file, save_current_plot_to_file

IMG_DIR = "img"
CSV_DIR = "csv"


def transform_and_save(
    transformation,
    original_shape: gpd.GeoSeries,
    transformation_params: Dict,
    output_dir: str,
    index: int,
) -> None:
    transformed_shape = transformation
    transformation_name = "centroid"
    if callable(transformation):
        transformed_shape = transformation(**transformation_params)
        transformation_name = transformation.__name__

    # Create initial plot/figure
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    # Plot the original shape
    original_shape.plot(ax=axes[0], edgecolor="black")
    axes[0].set_title("Original")

    # Plot the transformed shape
    transformed_shape.plot(ax=axes[1], edgecolor="black")
    axes[1].set_title("Transformed")

    # Add a title to the entire figure
    fig.suptitle(f"{transformation_name}: {transformation_params}")

    # Save and close
    save_current_plot_to_file(
        f"{output_dir}/{IMG_DIR}/{transformation_name}", str(index)
    )
    plt.close(fig)


def run(args) -> None:
    main_file: str = args.main_input
    secondary_file: str = args.secondary_input

    # Read the spatial data into a GeoDataFrame
    main_gdf: gpd.GeoDataFrame = gpd.read_file(main_file)
    secondary_gdf: gpd.GeoDataFrame = gpd.read_file(secondary_file)

    # Run dataframe type conversions
    save_df_to_file(main_gdf, f"{args.output_dir}/{CSV_DIR}", "original")
    save_df_to_file(
        main_gdf.overlay(right=secondary_gdf, how="union", keep_geom_type=False),
        f"{args.output_dir}/{CSV_DIR}",
        "union_overlay",
    )
    save_df_to_file(
        main_gdf.to_crs(epsg=3857), f"{args.output_dir}/{CSV_DIR}", "crs_3857"
    )
    save_df_to_file(
        main_gdf.to_wkb(hex=True), f"{args.output_dir}/{CSV_DIR}", "wkb_hex"
    )
    save_df_to_file(main_gdf.to_wkt(), f"{args.output_dir}/{CSV_DIR}", "wkt")

    main_gdf = main_gdf.to_crs(epsg=3857)
    secondary_gdf = secondary_gdf.to_crs(epsg=3857)

    modifier: float = math.sqrt(main_gdf.area.iloc[0])

    # Create sets of input parameters for data transformation
    parameters = [
        # simplification
        (
            main_gdf.simplify,
            main_gdf,
            {"tolerance": modifier * 2e-2, "preserve_topology": True},
        ),
        (
            main_gdf.simplify,
            main_gdf,
            {"tolerance": modifier * 3e-2, "preserve_topology": True},
        ),
        (
            main_gdf.simplify,
            main_gdf,
            {"tolerance": modifier * 5e-2, "preserve_topology": True},
        ),
        # centroid
        (main_gdf.centroid, main_gdf, {}),
        # buffer
        (main_gdf.buffer, main_gdf, {"distance": modifier * 1e-1, "resolution": 16}),
        (
            main_gdf.buffer,
            main_gdf,
            {"distance": modifier * 5e-2, "resolution": 16, "cap_style": 3},
        ),
        (
            main_gdf.buffer,
            main_gdf,
            {"distance": modifier * 2e-2, "resolution": 16, "join_style": 2},
        ),
        # affine transform
        (main_gdf.affine_transform, main_gdf, {"matrix": [1, 2, 1, 3, 4, 1]}),
        (main_gdf.affine_transform, main_gdf, {"matrix": [2, 1, 1, 1, 1, 1]}),
        (main_gdf.affine_transform, main_gdf, {"matrix": [3, 5, 1, 3, 3, 1]}),
        # rotate
        (main_gdf.rotate, main_gdf, {"angle": 10, "origin": "center"}),
        (main_gdf.rotate, main_gdf, {"angle": 90, "origin": (0, 0)}),
        (main_gdf.rotate, main_gdf, {"angle": 180, "origin": Point(0, 0)}),
        # scale
        (main_gdf.scale, main_gdf, {"xfact": 2, "yfact": 2, "origin": "center"}),
        (main_gdf.scale, main_gdf, {"xfact": 2, "yfact": 1, "origin": "center"}),
        (main_gdf.scale, main_gdf, {"xfact": 1, "yfact": 2, "origin": "center"}),
        # skew
        (main_gdf.skew, main_gdf, {"xs": 15, "ys": 15, "origin": "center"}),
        (main_gdf.skew, main_gdf, {"xs": 15, "ys": 30, "origin": "center"}),
        (main_gdf.skew, main_gdf, {"xs": 30, "ys": 30, "origin": "center"}),
        # translate
        (main_gdf.translate, main_gdf, {"xoff": modifier, "yoff": modifier}),
        (main_gdf.translate, main_gdf, {"xoff": modifier, "yoff": modifier}),
        (
            main_gdf.translate,
            main_gdf,
            {
                "xoff": -main_gdf.centroid.x.iloc[0],
                "yoff": -main_gdf.centroid.y.iloc[0],
            },
        ),
        # clip
        (
            main_gdf.clip,
            main_gdf,
            {"mask": main_gdf.centroid.buffer(modifier / math.sqrt(math.pi))},
        ),
        # clip by rect
        (
            main_gdf.clip_by_rect,
            main_gdf,
            {
                "xmin": float("-inf"),
                "xmax": float("inf"),
                "ymin": float("-inf"),
                "ymax": main_gdf.centroid.y.iloc[0],
            },
        ),
        (
            main_gdf.clip_by_rect,
            main_gdf,
            {
                "xmin": float("-inf"),
                "xmax": main_gdf.centroid.x.iloc[0],
                "ymin": float("-inf"),
                "ymax": main_gdf.centroid.y.iloc[0],
            },
        ),
        (
            main_gdf.clip_by_rect,
            main_gdf,
            {
                "xmin": float("-inf"),
                "xmax": main_gdf.centroid.x.iloc[0],
                "ymin": float("-inf"),
                "ymax": float("inf"),
            },
        ),
        # union
        (main_gdf.union, main_gdf, {"other": secondary_gdf, "align": True}),
    ]

    # Run data transformations
    for idx, params in enumerate(tqdm(parameters)):
        transform_and_save(
            transformation=params[0],
            original_shape=params[1],
            transformation_params=params[2],
            output_dir=args.output_dir,
            index=idx,
        )
