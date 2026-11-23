// Central site configuration — edit this file first.
// Everything marked TODO is a placeholder.

export const SITE = {
  name: 'Tim Rehbronn',
  // Shown under your name on the home page and in the <title>.
  role: 'Researcher & Engineer', // TODO
  affiliation: 'Your Institution', // TODO, e.g. "PhD student @ TU Munich"
  affiliationUrl: '', // TODO
  location: 'Germany', // TODO
  description:
    'Personal website of Tim Rehbronn — research, projects, publications, videos and explanatory articles.', // TODO
  email: 'you@example.com', // TODO (shown obfuscated-ish as plain mailto)
  avatar: '/images/avatar.svg', // TODO: replace with /images/avatar.jpg
  ogImage: '/images/og.png', // optional social preview image (1200×630)
  cvPdf: '/cv.pdf', // TODO: put your CV PDF into public/cv.pdf
  // Variants of your name that get highlighted in author lists.
  authorNames: ['Tim Rehbronn', 'T. Rehbronn'],
};

// Leave a URL empty ('') to hide the link.
export const SOCIALS: { label: string; href: string }[] = [
  { label: 'Email', href: `mailto:${SITE.email}` },
  { label: 'CV', href: SITE.cvPdf },
  { label: 'GitHub', href: 'https://github.com/TimRehbronn' },
  { label: 'Google Scholar', href: '' }, // TODO
  { label: 'ORCID', href: '' }, // TODO
  { label: 'LinkedIn', href: '' }, // TODO
  { label: 'YouTube', href: '' }, // TODO
].filter((s) => s.href);

export const NAV = [
  { label: 'About', href: '/' },
  { label: 'Publications', href: '/publications/' },
  { label: 'Projects', href: '/projects/' },
  { label: 'Videos', href: '/videos/' },
  { label: 'Blog', href: '/blog/' },
  { label: 'CV', href: '/cv/' },
];
