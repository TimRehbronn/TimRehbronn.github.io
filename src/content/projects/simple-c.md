---
title: SIMPLE-C — Multi-LiDAR Calibration on the Water
summary: Online extrinsic calibration of multiple LiDARs using nothing but a moving reflective target — built for feature-sparse harbors where the vessel and the water keep moving.
year: 2026
status: completed
featured: true
tags: [calibration, LiDAR, ROS 2, open source]
image: /images/publications/simple-c.svg
links:
  code: https://github.com/rwth-irt/SIMPLE-C
  paper: https://doi.org/10.1007/s10846-026-02486-7
  data: https://doi.org/10.5281/zenodo.13968727
  video: /videos/#simple-c-explainer
---

Calibrating several LiDARs on a docked ship is surprisingly hard: the platform moves, the water surface returns
unreliable points, and there are hardly any features to register against. Moving a large vessel just for calibration
is expensive.

**SIMPLE-C** solves this with a pragmatic idea: move a highly reflective object — a plastic lid with reflective tape or even
a warning vest — through the overlapping field of view and track it in every sensor. The target is detected via intensity
thresholding and spatial clustering with backtracking and filtering; a weighted Kabsch/SVD step then solves the extrinsics
in closed form. Adaptive outlier rejection and calibration weights make it robust, and it runs online, so you get live
feedback while calibrating.

- 5 cm / 0.3° RMSE on sparse water scenarios, 3 cm on land
- up to 47 % lower translational error than ICP variants, GMMCalib, CROON and Fast Global Registration on the water side
- no platform motion, extra sensors or special target geometry required

## Explainer video

<video controls playsinline preload="none" poster="/videos/simple-c-explainer.jpg" style="aspect-ratio: 4 / 5; width: 100%; max-width: 24rem; border-radius: 2px; border: 1px solid var(--border-strong); background: #000">
  <source src="/videos/simple-c-explainer.mp4" type="video/mp4" />
</video>

Published in the [Journal of Intelligent & Robotic Systems](https://doi.org/10.1007/s10846-026-02486-7). Code and dataset are
[open source](https://github.com/rwth-irt/SIMPLE-C), with a [Docker setup](https://github.com/rwth-irt/SIMPLE-C-docker).
