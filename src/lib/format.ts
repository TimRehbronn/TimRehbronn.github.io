// Display labels for link keys used in publications and projects (keeps spelling consistent).
export const LINK_LABELS: Record<string, string> = {
  ieee: 'IEEE',
  pdf: 'PDF',
  arxiv: 'arXiv',
  doi: 'DOI',
  paper: 'Paper',
  code: 'Code',
  data: 'Data',
  project: 'Project page',
  demo: 'Demo',
  video: 'Video',
  slides: 'Slides',
  poster: 'Poster',
  press: 'Press',
  website: 'Website',
};

// Display labels for project status.
export const STATUS_LABELS: Record<string, string> = {
  active: 'What I’m currently on',
  completed: 'Completed',
  archived: 'Archived',
};

export const linkEntries = (links: Record<string, string | undefined>) =>
  Object.entries(links)
    .filter((e): e is [string, string] => Boolean(e[1]))
    .map(([key, href]) => ({ key, href, label: LINK_LABELS[key] ?? key }));

/** Minimal inline markup for data strings: escapes HTML and turns **text** into <strong>text</strong>. */
export const emph = (text: string) =>
  text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
