import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';
import { glob, file } from 'astro/loaders';

const links = z
  .object({
    ieee: z.string().optional(),
    pdf: z.string().optional(),
    arxiv: z.string().optional(),
    doi: z.string().optional(),
    code: z.string().optional(),
    project: z.string().optional(),
    demo: z.string().optional(),
    video: z.string().optional(),
    slides: z.string().optional(),
    poster: z.string().optional(),
    data: z.string().optional(),
    press: z.string().optional(),
    paper: z.string().optional(),
    website: z.string().optional(),
  })
  .default({});

const blog = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.coerce.date(),
    updated: z.coerce.date().optional(),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
  }),
});

const projects = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/projects' }),
  schema: z.object({
    title: z.string(),
    summary: z.string(),
    year: z.number(),
    status: z.enum(['active', 'completed', 'archived']).default('active'),
    tags: z.array(z.string()).default([]),
    image: z.string().optional(), // path under public/, e.g. /images/projects/foo.png
    featured: z.boolean().default(false),
    links,
  }),
});

const publications = defineCollection({
  loader: file('src/data/publications.yaml'),
  schema: z.object({
    title: z.string(),
    authors: z.array(z.string()),
    venue: z.string(),
    venueShort: z.string().optional(),
    year: z.number(),
    type: z.enum(['journal', 'conference', 'workshop', 'preprint', 'manuscript', 'thesis', 'other']),
    selected: z.boolean().default(false),
    thumbnail: z.string().optional(),
    abstract: z.string().optional(),
    note: z.string().optional(), // e.g. "Oral", "Best Paper Award"
    links,
    bibtex: z.string().optional(),
  }),
});

const videos = defineCollection({
  loader: file('src/data/videos.yaml'),
  schema: z.object({
    title: z.string(),
    youtubeId: z.string().optional(), // either a YouTube video …
    src: z.string().optional(), // … or a self-hosted file under public/, e.g. /videos/foo.mp4
    poster: z.string().optional(),
    aspect: z.string().default('16 / 9'), // CSS aspect-ratio, e.g. '4 / 5' for portrait
    date: z.coerce.date(),
    description: z.string().optional(),
    thumbnail: z.string().optional(), // local thumbnail avoids a request to YouTube before consent
    tags: z.array(z.string()).default([]),
  }),
});

const news = defineCollection({
  loader: file('src/data/news.yaml'),
  schema: z.object({
    date: z.coerce.date(),
    text: z.string(),
    link: z.string().optional(),
  }),
});

export const collections = { blog, projects, publications, videos, news };
