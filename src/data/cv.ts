// CV data — rendered on /cv/ and (interests) on the home page.

export interface CvEntry {
  title: string;
  org: string;
  orgUrl?: string;
  location?: string;
  start: string; // free text, e.g. "2023" or "Oct 2023"
  end?: string; // omit for "present"
  details?: string[];
}

const IRT = 'https://www.irt.rwth-aachen.de';

export const experience: CvEntry[] = [
  {
    title: 'Research Associate & PhD Candidate — Navigation Group',
    org: 'Institute of Automatic Control (IRT), RWTH Aachen University',
    orgUrl: IRT,
    location: 'Aachen',
    start: 'Oct 2023',
    details: [
      'Calibration, navigation, detection and tracking for maritime autonomous systems; supervised by Prof. Dr.-Ing. Heike Vallery.',
      'Implemented, deployed and field-tested a navigation (ES-EKF, GNSS/IMU), LiDAR detection, tracking (JPDA) and grid-mapping pipeline for a real multi-vessel scenario (GALILEOnautic 2+).',
      'Developed SIMPLE-C, a target-based multi-LiDAR extrinsic calibration tool for feature-sparse maritime settings, deployed on real vessels.',
      'Developed MSTNet, a self-supervised pretraining pipeline for label-efficient maritime 3D LiDAR object detection.',
      'Working on factor-graph-based navigation fusing LiDAR, radar and IMU for GNSS-denied operation, multi-target tracking with a trajectory PMBM filter, and grey-box vessel trajectory prediction from AIS data.',
      'Industry-related projects: GALILEOnautic 2+, KORIS (medical robotics), innocam.NRW.',
    ],
  },
  {
    title: 'Intern — Automated Driving / Parking',
    org: 'Robert Bosch GmbH, Cross-Domain Computing Solutions',
    location: 'Stuttgart region',
    start: 'Apr 2023',
    end: 'Aug 2023',
    details: [
      'Function development and KPI analysis (Python) for the Moving Off Information System and Automated Emergency Brake, including in-vehicle testing.',
    ],
  },
  {
    title: 'Student Research Assistant — Vehicle Intelligence & Automated Driving',
    org: 'Institute for Automotive Engineering (ika), RWTH Aachen University',
    location: 'Aachen',
    start: 'Apr 2022',
    end: 'Mar 2023',
    details: [
      'Integrated adverse-weather datasets (DENSE, Canadian Adverse Driving Conditions) and Waymo into the institute’s ML framework; implemented the monocular 3D detector SMOKE in PyTorch.',
    ],
  },
  {
    title: 'Student Research Assistant — Neural Networks in Video Coding',
    org: 'Institute for Communications Engineering (IENT), RWTH Aachen University',
    location: 'Aachen',
    start: 'Oct 2019',
    end: 'Mar 2022',
    details: [
      'Developed features in a TensorFlow framework for intra prediction with (convolutional) neural networks.',
      'Built an image processing and computer vision lab for students (Python/C, Jupyter).',
    ],
  },
  {
    title: 'Head of Electrical Powertrain',
    org: 'Ecurie Aix — Formula Student Team RWTH Aachen e.V.',
    location: 'Aachen',
    start: 'Jan 2020',
    end: 'Jun 2021',
    details: [
      'Led a team of seven students (Oct 2020 – Jun 2021); responsible for the electrical system of two self-developed electric race cars.',
    ],
  },
];

export const education: CvEntry[] = [
  {
    title: 'Dr.-Ing. (PhD candidate), Electrical Engineering',
    org: 'RWTH Aachen University',
    location: 'Aachen',
    start: '2023',
    end: '2027 (expected)',
    details: ['Dissertation submission planned for Q1 2027.'],
  },
  {
    title: 'M.Sc. Electrical Engineering, Information Technology and Computer Engineering',
    org: 'RWTH Aachen University',
    location: 'Aachen',
    start: '2020',
    end: '2023',
    details: [
      'Major: Systems and Automation. Graduated with distinction (Dean’s List), overall grade 1.4 (top 5%).',
      'Thesis: “Current Approaches to Robust Lidar Object Detection under Adverse Weather Conditions” (grade 1.0), Institute for Automotive Engineering & Chair for Computer Vision.',
    ],
  },
  {
    title: 'B.Sc. Electrical Engineering, Information Technology and Computer Engineering',
    org: 'RWTH Aachen University',
    location: 'Aachen',
    start: '2016',
    end: '2020',
    details: ['Major: Communications Engineering and Information Technology.'],
  },
];

export const service: CvEntry[] = [
  {
    title: 'Lead, Expert Group “Water”',
    org: 'innocam.NRW competence center',
    start: '2023',
    details: ['Organizing and moderating workshops on inland-vessel topics; publishing market reports and advisory papers.'],
  },
  {
    title: 'Teaching & Supervision',
    org: 'Institute of Automatic Control (IRT), RWTH Aachen University',
    orgUrl: IRT,
    start: '2023',
    details: [
      'Supervised 10 interdisciplinary Bachelor’s and Master’s theses.',
      'Teaching support for Control Engineering.',
    ],
  },
];

export const awards: { year: string; title: string; detail?: string; url?: string }[] = [
  { year: '2023', title: 'Dean’s List, RWTH Aachen University', detail: 'M.Sc. graduated with distinction' },
];

export const schools: { year: string; title: string; detail?: string; url?: string }[] = [
  {
    year: 'Jul 2025',
    title: 'Graduate School NAVIGATE 2025',
    detail: 'Connected Autonomous Vehicles & Intelligent Transportation Systems — TU Delft, supported by the IEEE ITS Society Benelux Chapter',
    url: 'https://www.tudelft.nl/en/me/research/transport-mobility/graduate-school-navigate-2025',
  },
  {
    year: '2023–',
    title: 'Leadership & management trainings',
    detail:
      'The Engineer as a Manager · Leading Interdisciplinary Teams · Project Management I & II · Self-Organization and Time Management · Supervising Theses and Dissertations',
  },
];

export const skills: { group: string; items: string[] }[] = [
  { group: 'Methods', items: ['State estimation (ES-EKF, FGO)', 'Sensor fusion', 'Multi-object tracking (JPDA, PMBM)', '3D object detection', 'Extrinsic calibration'] },
  { group: 'Software', items: ['Python', 'PyTorch', 'C++', 'ROS 2', 'Gazebo', 'Docker', 'CI/CD', 'Git', 'Linux'] },
  { group: 'Hardware', items: ['GNSS', 'IMU', 'LiDAR', 'Radar', 'AIS', 'NVIDIA Jetson Orin'] },
  { group: 'Languages', items: ['German (native)', 'English (full professional)', 'Spanish & Latin (elementary)'] },
];

// Research interests — shown on the home page.
export const interests: { title: string; text: string }[] = [
  {
    title: 'State estimation & sensor fusion',
    text: 'GNSS/IMU navigation with error-state Kalman filters and factor graph optimization — and robust navigation when GNSS is unavailable, fusing LiDAR, radar and IMU.',
  },
  {
    title: '3D perception',
    text: 'LiDAR 3D object detection in maritime and adverse-weather conditions, self-supervised pretraining for label efficiency, and calibrated uncertainties for downstream tracking.',
  },
  {
    title: 'Tracking & prediction',
    text: 'Multi-object tracking across radar, LiDAR, AIS and camera with JPDA, FGO- and PMBM-based filters; vessel trajectory prediction with physics-informed learned models.',
  },
  {
    title: 'Field robotics',
    text: 'Calibration, time synchronization and deployment of complete pipelines on real vessels — validated in the field, not only in simulation.',
  },
];
