// @ts-check
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import { unified } from '@astrojs/markdown-remark';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

// Code highlighting in the site's colours: black background, greys, one orange accent.
const ORANGE = '#fd7422';
const siteTheme = {
  name: 'site-orange',
  type: /** @type {'dark'} */ ('dark'),
  colors: { 'editor.background': '#000000', 'editor.foreground': '#d0d0d0' },
  tokenColors: [
    { settings: { foreground: '#d0d0d0' } },
    { scope: ['comment', 'punctuation.definition.comment', 'string.quoted.docstring', 'string.quoted.docstring.multi.python'], settings: { foreground: '#6b6b6b', fontStyle: 'italic' } },
    { scope: ['keyword', 'storage', 'storage.type', 'storage.modifier', 'keyword.control', 'keyword.operator.logical', 'keyword.operator.new', 'support.type.python'], settings: { foreground: ORANGE } },
    { scope: ['entity.name.function', 'support.function', 'meta.function-call.generic', 'entity.name.class', 'entity.name.type'], settings: { foreground: '#ffffff' } },
    { scope: ['string', 'string.quoted', 'punctuation.definition.string'], settings: { foreground: '#a3a3a3' } },
    { scope: ['constant.numeric', 'constant.language', 'constant.other', 'variable.other.constant'], settings: { foreground: ORANGE } },
    { scope: ['keyword.operator', 'punctuation'], settings: { foreground: '#8a8a8a' } },
  ],
};

export default defineConfig({
  site: 'https://timrehbronn.github.io',
  integrations: [mdx(), sitemap()],
  markdown: {
    // unified (remark/rehype) pipeline so we can render LaTeX math with KaTeX.
    processor: unified({
      remarkPlugins: [remarkMath],
      rehypePlugins: [rehypeKatex],
    }),
    shikiConfig: {
      theme: siteTheme,
    },
  },
});
