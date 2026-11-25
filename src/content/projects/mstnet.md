---
title: MSTNet — Label-Efficient Maritime 3D Detection
summary: Self-supervised pretraining on unlabeled LiDAR data so that maritime 3D object detectors need far fewer labels.
year: 2026
status: active
featured: true
tags: [3D object detection, self-supervised learning, LiDAR, PyTorch]
image: /images/publications/mstnet.svg
links:
  code: https://github.com/rwth-irt/mstnet
  data: https://doi.org/10.5281/zenodo.22825184
---

Labeled 3D LiDAR data of vessels is scarce — unlabeled data is not. **MSTNet** pretrains a sparse-transformer encoder on
unlabeled maritime and driving point clouds with masked geometric reconstruction targets (centroid, normal, occupancy),
then fine-tunes it on labeled maritime datasets.

The goal: reach the same detection accuracy with far fewer labels than training from scratch. The approach is evaluated across label budgets from 5 to 100 %
and is benchmarked against 11 established 3D detectors.

The manuscript is in internal review. [Code, configurations and results](https://github.com/rwth-irt/mstnet) and the [data](https://doi.org/10.5281/zenodo.22825184) are already public.
