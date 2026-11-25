// Blog series. A part links to its post once a post with that slug is published; until then it is shown as "Coming soon…".
export type SeriesPart = { title: string; summary: string; slug?: string };

export const SERIES = {
  title: 'Localization and sensor fusion',
  parts: [
    { title: 'Strapdown inertial navigation', slug: 'strapdown-inertial-navigation', summary: 'From gyroscope and accelerometer readings to attitude, velocity and position.' },
    { title: 'GNSS', summary: 'Satellites, signals, pseudoranges and positioning, and where the errors come from.' },
    { title: 'State estimation', summary: 'Bayes filter, Kalman filter, EKF, UKF and particle filter, and how uncertainty is represented and propagated.' },
    { title: 'Sensor fusion 1: GNSS/INS', summary: 'Loosely and tightly coupled GNSS/INS with an error-state Kalman filter, and how to test whether its uncertainty is consistent.' },
    { title: 'LiDAR odometry', summary: 'Motion from point clouds: scan matching and LiDAR-inertial odometry.' },
    { title: 'Radar odometry', summary: 'Ego-motion from Doppler and radar scans, and what makes radar different.' },
    { title: 'Rotations and poses on manifolds', summary: 'Lie groups SO(3) and SE(3), IMU preintegration, calibration and observability.' },
    { title: 'Sensor fusion 2: multi-sensor localization', summary: 'GNSS, IMU, LiDAR and radar with ES-EKF, IEKF, invariant EKF, particle filter and factor graphs, with a focus on uncertainty and consistency.' },
  ] satisfies SeriesPart[],
};

/** Further topics after the series. */
export const LATER = ['Multi-object detection', 'Multi-object tracking', 'SLAM'];
