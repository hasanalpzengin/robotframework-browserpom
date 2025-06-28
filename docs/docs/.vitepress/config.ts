import { defineConfig } from 'vitepress'

// https://vitepress.vuejs.org/config/app-configs
export default defineConfig({
  title: 'robotframework-browserpom',
  description: 'Page Object Model extension for Robot Framework Browser',
  base: '/robotframework-browserpom/',
  themeConfig: {
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Installation', link: '/installation' },
      { text: 'Usage', link: '/usage' },
      { text: 'Examples', link: '/examples' },
      { text: 'Contributing', link: '/contributing' },
      { text: 'License', link: '/license' },
    ],
    sidebar: [
      {
        text: 'Guide',
        items: [
          { text: 'Introduction', link: '/' },
          { text: 'Installation', link: '/installation' },
          { text: 'Usage', link: '/usage' },
          { text: 'Examples', link: '/examples' },
          { text: 'Tips & Best Practices', link: '/tips' },
        ]
      },
      {
        text: 'Project',
        items: [
          { text: 'Contributing', link: '/contributing' },
          { text: 'License', link: '/license' },
        ]
      }
    ]
  }
})
