---
title: Vessel Trajectory Prediction in Confined Waters
summary: A regime-switching grey-box model that predicts the next 10 minutes of vessel motion from AIS data in ports, rivers, canals and lock approaches.
year: 2026
status: active
image: /images/projects/inland-trajectory-prediction.svg
featured: false
tags: [trajectory prediction, AIS, grey-box, IMM, uncertainty]
---

Joint work with Dustin Klein and Wadie Skaf. The paper is in preparation for 2027.

## Problem

In ports, rivers, canals and in front of locks, vessels rarely go straight. They turn, stop, berth and give way to
mixed traffic. This is where good motion prediction matters most, for vessel traffic services, collision avoidance
and autonomous ships, and it is also where simple models such as constant velocity fail most often.

Learned predictors (e.g. TrAISformer or diffusion models) are mostly evaluated on open sea and contain no ship
physics. Physical models are interpretable but do not know how vessels actually maneuver.

## Approach

The model predicts the motion of other vessels from AIS data for a 10-minute horizon:

- **Maneuver regimes without labels.** The model learns a small number of recurring regimes (for example transit,
  turning, berthing, waiting) directly from the data.
- **Physics per regime.** For each regime, a network outputs control inputs (longitudinal acceleration, turn rate).
  A ship kinematics model with drift angle and yaw inertia (Nomoto-type) turns them into motion. The learned
  correction to a physical baseline is kept minimal, so the physics is not trained away.
- **Regime switches within the horizon.** A learned, state-dependent interacting multiple model (IMM) handles
  transitions, e.g. from transit into a turn.
- **Uncertainty.** Mean and covariance are propagated through the kinematics, as in the prediction step of an EKF.
  The output is a Gaussian mixture for every time step.
- **Map context.** 16 course-relative ray distances to the edge of the navigable water (from OpenStreetMap) describe
  the surroundings without using absolute position, so the model can transfer to new waterways.

## Data

AIS data from the German Federal Maritime and Hydrographic Agency (BSH), 2021 to 2026, from three stations with
confined waters: Kiel (Kiel Fjord, Kiel Canal entrance, Holtenau locks), Bremerhaven (port and Weser) and
Wedel (Lower Elbe). We rebuilt and audited the preprocessing pipeline, including reconstruction of receiver clock
offsets of up to ±29 s. The dataset covers about 29,000 vessels and more than 150 million training windows on a 10 s grid.

## Evaluation

The evaluation protocol is fixed before the test set is opened:

- vessel-disjoint splits, plus a temporal hold-out (2026) and a station hold-out,
- energy score over the full predictive distribution and ADE at 10 minutes, balanced per vessel and stratified by
  maneuver type (straight, turning, turn starting within the horizon, stationary),
- multiple seeds, bootstrap confidence intervals and correction for multiple comparisons,
- baselines run from their original code with the same tuning budget: TrAISformer, Trajectron++, PINN-VTP, Chronos-2,
  an LSTM with map input, and classical constant-velocity, CTRV and IMM Kalman filters,
- an ablation from pure learning over simple kinematics to the full model with regimes and regime switching.

## Status

Data pipeline, model, evaluation and all baseline integrations are implemented. Hyperparameter optimization,
ablations and the final test evaluation are next. Code, results and the paper will follow.
