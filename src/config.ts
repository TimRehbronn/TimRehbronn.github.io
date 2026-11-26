// Central site configuration — edit this file first.

export const SITE = {
  name: 'Tim Rehbronn',
  role: 'PhD Candidate',
  affiliation: 'Institute of Automatic Control (IRT), RWTH Aachen University',
  affiliationShort: 'IRT, RWTH Aachen',
  affiliationUrl: 'https://www.irt.rwth-aachen.de',
  location: 'Aachen, Germany',
  description:
    'Tim Rehbronn — researcher and PhD candidate at RWTH Aachen University working on state estimation and sensor fusion for autonomous systems.',
  email: 'tim@rehbronn.de',
  avatar: '/images/portrait-2026.jpg', // new file name = no stale browser cache
  ogImage: '/images/og.png', // social preview image (1200×630)
  cvPdf: '', // optional: put a public CV into public/cv.pdf and set '/cv.pdf'
  // Variants of your name that get highlighted in author lists.
  authorNames: ['Tim Rehbronn', 'T. Rehbronn'],
};

// Icons available in src/components/Icon.astro
export type IconName = 'email' | 'cv' | 'github' | 'linkedin' | 'researchgate' | 'orcid' | 'rss' | 'youtube' | 'link';

// Leave a URL empty ('') to hide the link.
type Social = { label: string; href: string; icon: IconName };

const ALL_SOCIALS: Social[] = [
  { label: 'Email', href: `mailto:${SITE.email}`, icon: 'email' },
  { label: 'CV', href: SITE.cvPdf ? SITE.cvPdf : '/cv/', icon: 'cv' },
  { label: 'GitHub', href: 'https://github.com/TimRehbronn', icon: 'github' },
  { label: 'LinkedIn', href: 'https://www.linkedin.com/in/tim-rehbronn-959598205', icon: 'linkedin' },
  { label: 'ORCID', href: 'https://orcid.org/0009-0009-5241-2588', icon: 'orcid' },
  { label: 'ResearchGate', href: 'https://www.researchgate.net/profile/Tim-Rehbronn-2', icon: 'researchgate' },
  { label: 'YouTube', href: '', icon: 'youtube' }, // TODO
];

export const SOCIALS = ALL_SOCIALS.filter((s) => s.href);

export const NAV = [
  { label: 'About', href: '/' },
  { label: 'Publications', href: '/publications/' },
  { label: 'Projects', href: '/projects/' },
  { label: 'CV', href: '/cv/' },
  { label: 'Blog', href: '/blog/' },
  { label: 'Videos', href: '/videos/' },
];
