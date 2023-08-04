# FisheyeCubemap

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Alt text](https://img.shields.io/pypi/pyversions/python-binance.svg)

Python notebooks and scripts to generate fisheye camera images from cubemap renders, using numpy and OpenCV.

---

## Description

Here is a brief description of the different scripts included:

- `FisheyeCubemap.ipynb`: given a field of view `fov` and folder `image_path` of rendered faces of the cube, maps the cubemap to a sphere and generates a fisheye image. It also undistorts the generated fisheye image to get the correspondent perspective version if the FoV is lower than 180º.

- `Cube2Sphere.ipynb`: compare different cube-sphere mappings.

- `Projections.ipynb`: includes plots for some quantities for the classical fisheye projections.

- `Polynomial.ipynb`: compare different root-finding polynomial algorithms for obtaining the angle.

- `undistort.py`: use OpenCV to undistort a fisheye image, indicating the camera parameters.

- `blending.py`: overlap and blend two images for comparison.

In the folder `Source` there are other functions defined related to geometric transformations in `geometry.py` and camera theory in `camera.py`.

## Requisites

To run the above scripts, the following python packages are required:

- `numpy`

- `matplotlib`

- `opencv`
