// CV data — rendered on /cv/. All entries are PLACEHOLDERS.

export interface CvEntry {
  title: string;
  org: string;
  orgUrl?: string;
  location?: string;
  start: string; // free text, e.g. "2023" or "Oct 2023"
  end?: string; // omit for "present"
  details?: string[];
}

export const education: CvEntry[] = [
  {
    title: 'M.Sc. Your Field',
    org: 'Your University',
    location: 'City, Germany',
    start: '2022',
    end: '2025',
    details: ['Thesis: “Title of your master thesis”', 'Grade: 1.x'],
  },
  {
    title: 'B.Sc. Your Field',
    org: 'Your University',
    location: 'City, Germany',
    start: '2019',
    end: '2022',
  },
];

export const experience: CvEntry[] = [
  {
    title: 'Research Assistant',
    org: 'Some Lab',
    location: 'City',
    start: '2025',
    details: ['What you work on, in one line.', 'A concrete result or responsibility.'],
  },
  {
    title: 'Software Engineering Intern',
    org: 'Some Company',
    start: '2023',
    end: '2023',
    details: ['What you built and why it mattered.'],
  },
];

export const awards: { year: string; title: string; detail?: string }[] = [
  { year: '2024', title: 'Example Scholarship', detail: 'Short description' },
];

export const teaching: CvEntry[] = [
  { title: 'Teaching Assistant — Course Name', org: 'Your University', start: 'WS 2024/25' },
];

export const skills: { group: string; items: string[] }[] = [
  { group: 'Programming', items: ['Python', 'C++', 'TypeScript'] },
  { group: 'Tools', items: ['PyTorch', 'Git', 'Docker', 'LaTeX'] },
  { group: 'Languages', items: ['German (native)', 'English (fluent)'] },
];

// Research interests — shown on the home page.
export const interests: { title: string; text: string }[] = [
  { title: 'Research area one', text: 'One sentence on what fascinates you here and which questions you ask.' },
  { title: 'Research area two', text: 'One sentence on the methods or applications you care about.' },
  { title: 'Research area three', text: 'One sentence that connects your work to a bigger goal.' },
];
