---
title: LiDAR Object Detection in Adverse Weather
summary: Master's thesis on using temporal point-cloud sequences to make LiDAR 3D detection robust to rain, snow and fog.
year: 2023
status: completed
featured: false
tags: [3D object detection, automated driving, deep learning]
links:
  paper: https://doi.org/10.1109/ICECET58911.2023.10389489
  arxiv: https://arxiv.org/abs/2401.09049
---

Rain, snow and fog corrupt LiDAR point clouds and degrade object detection. In my Master's thesis at the
Institute for Automotive Engineering (ika) and the Chair for Computer Vision at RWTH Aachen, I compared ways to exploit
**temporal information** instead of filtering single frames:

- early and late sequence fusion
- convolutional LSTMs
- attention-based fusion
- grid-map-based fusion

evaluated on nuScenes, DENSE and the Canadian Adverse Driving Conditions dataset. A key finding — a temporal-offset augmentation
that randomly skips frames during training — is published at [IEEE ICECET 2023](https://doi.org/10.1109/ICECET58911.2023.10389489) ([arXiv](https://arxiv.org/abs/2401.09049)).
