# TimRehbronn.github.io

Personal website — CV, research, publications, projects, videos and an interactive explainer blog.
Built with [Astro](https://astro.build), deployed to GitHub Pages via GitHub Actions.

## Local development

```bash
npm install
npm run dev        # http://localhost:4321
npm run build      # type-check + static build into dist/
npm run preview    # serve the built site
```

## Where to edit what

| What                     | File                                                   |
| ------------------------ | ------------------------------------------------------ |
| Name, role, links        | `src/config.ts`                                        |
| Bio text                 | `src/pages/index.astro` (hero section)                 |
| Research interests, CV   | `src/data/cv.ts`                                       |
| Publications             | `src/data/publications.yaml`                           |
| News                     | `src/data/news.yaml`                                   |
| Videos (YouTube)         | `src/data/videos.yaml`                                 |
| Projects                 | `src/content/projects/*.md` (one file per project)     |
| Blog posts               | `src/content/blog/*.mdx` (one file per post)           |
| Interactive figures      | `src/components/explainers/*.astro`                    |
| Colors, fonts, spacing   | `src/styles/global.css` (CSS variables at the top)     |
| Photo, CV PDF, images    | `public/images/avatar.jpg`, `public/cv.pdf`, `public/images/…` |

All content is schema-checked (`src/content.config.ts`) — a typo in a YAML field fails the build
with a clear error instead of silently breaking the page.

### Blog posts with math and animations

Posts are MDX: Markdown + LaTeX math (`$…$`, `$$…$$`, rendered with KaTeX) + components.
See `src/content/blog/gradient-descent.mdx` for an example that embeds an interactive figure:

```mdx
import GradientDescent from '../../components/explainers/GradientDescent.astro';

<GradientDescent lr={0.05} start={2.2}>Caption</GradientDescent>
```

Set `draft: true` in the frontmatter to hide a post in production (it still shows in `npm run dev`).

## Deployment

Every push to `main` builds and deploys via `.github/workflows/deploy.yml`.
One-time setup: **Settings → Pages → Build and deployment → Source: GitHub Actions**.

## Privacy notes (DE)

- No external fonts, analytics or trackers are loaded.
- YouTube videos are loaded from `youtube-nocookie.com` only after a click. Add a local
  `thumbnail` in `videos.yaml` to avoid fetching the preview image from YouTube as well.
