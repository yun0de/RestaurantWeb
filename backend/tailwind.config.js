// tailwind.config.js
module.exports = {
  content: [
    './api/templates/**/*.html',
    './api/**/*.py',
  ],
  theme: {
    extend: {
      colors: {
        'asian-red': '#b30000',   // traditional chinese red-ish
        'page-beige': '#f5eadf',
        'hero-black': '#0b0b0b'
      },
      fontFamily: {
        'serif-display': ['Georgia', 'serif'],
        'body': ['Inter', 'system-ui', 'sans-serif']
      }
    },
  },
  plugins: [],
}
