---
title: GALILEOnautic 2+ — Cooperative Navigation & Perception for Vessels
summary: A navigation, detection, tracking and mapping pipeline for a real multi-vessel scenario — deployed on vessels in the port of Rostock.
year: 2025
status: active
featured: true
tags: [navigation, sensor fusion, tracking, field deployment]
image: /images/publications/icmass2025.svg
links:
  paper: https://doi.org/10.1088/1742-6596/3123/1/012020
---

Automated maneuvering in ports and confined waters requires every vessel to know precisely where it is and what is around it.
In the GALILEOnautic 2+ project, I implemented, deployed and tested the perception side of a cooperative multi-vessel system:

- **Navigation:** error-state EKF fusing GNSS and IMU for accurate self-localization.
- **Detection:** LiDAR-based object detection on board.
- **Tracking:** multi-object tracking (JPDA) fusing onboard detections with AIS data and observations from other vessels.
- **Mapping:** grid maps distinguishing static and dynamic obstacles, passed as convex polygons to a centralized collision-avoidance planner.

The system runs on NVIDIA Jetson hardware with synchronized sensor networks, Docker-based deployment and ROS 2,
and was validated in the port of Rostock with two real and one simulated vessel — among them the 52 m research vessel *Deneb*.
Results are published at [ICMASS 2025](https://doi.org/10.1088/1742-6596/3123/1/012020).
