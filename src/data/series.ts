// Blog series. A part links to its post once a post with that slug is published; until then it is shown as "Coming soon…".
// Parts are numbered from 0 (the introduction).
export type SeriesPart = { title: string; summary: string; slug?: string };

export const SERIES = {
  title: 'Localization and sensor fusion',
  parts: [
    { title: 'What is state estimation, and why localization needs it', summary: 'The big picture: states, measurements and uncertainty, why no single sensor is enough, and a map of this series.' },
    { title: 'Strapdown inertial navigation', slug: 'strapdown-inertial-navigation', summary: 'From gyroscope and accelerometer readings to attitude, velocity and position.' },
    { title: 'GNSS', summary: 'Satellites, signals, pseudoranges and positioning, and where the errors come from.' },
    { title: 'Bayes filter and Kalman filter', summary: 'Recursive estimation, the Bayes filter and the Kalman filter, and how uncertainty is represented and propagated.' },
    { title: 'Nonlinear filters: EKF vs. UKF vs. particle filter', summary: 'Three approximations of the same Bayes filter: linearization, sigma points and particles, and when each one fails.' },
    { title: 'Sensor fusion 1: GNSS/INS', summary: 'The error-state Kalman filter for loosely and tightly coupled GNSS/INS, and how to test whether its uncertainty is consistent.' },
    { title: 'LiDAR odometry', summary: 'Motion from point clouds: scan matching and LiDAR-inertial odometry.' },
    { title: 'Radar odometry', summary: 'Ego-motion from Doppler and radar scans, and what makes radar different.' },
    { title: 'Filters on manifolds: ES-EKF vs. invariant EKF vs. manifold EKF', summary: 'Lie groups SO(3), SE(3) and SE₂(3), and three ways to define the error of a filter on them, with consequences for observability and consistency.' },
    { title: 'From EKF to factor graphs', summary: 'Recursive vs. batch, filter vs. smoother, fixed-lag and incremental; iterated EKF, factor graph optimization, IMU preintegration, sum-product vs. max-product.' },
    { title: 'Sensor fusion 2: multi-sensor localization', summary: 'GNSS, IMU, LiDAR and radar with the methods compared side by side, extrinsic and temporal calibration, and a focus on consistency.' },
    { title: 'Visual odometry', summary: 'Motion from a camera: camera models, features, epipolar geometry and visual-inertial odometry.' },
    { title: 'Sensor fusion 3: adding the camera', summary: 'Camera, IMU, GNSS, LiDAR and radar together: visual-inertial filters, sliding-window optimization and consistency.' },
    { title: 'SLAM', summary: 'Localizing while building a map: landmarks, loop closure, pose graphs and globally consistent maps.' },
    { title: 'Multi-target tracking', summary: 'Estimating many objects at once: data association, JPDA, MHT and random finite set filters such as PMBM.' },
  ] satisfies SeriesPart[],
};

/** Further topics after the series. */
export const LATER = ['Multi-object detection'];
