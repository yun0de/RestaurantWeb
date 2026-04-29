/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './api/templates/**/*.html',
    './api/templates/*.html',
    './api/**/*.py'
  ],
  theme: {
    extend: {
      colors: {
        'asian-red': '#b22b23',
        'page-beige': '#f5eadf',
        'hero-black': '#0b0b0b',
        'boong-ivory': '#F5F3EC',
        'boong-ink': '#1A1817',
        'boong-crimson': '#8C2121',
        'boong-jade': '#4A6054',
        'boong-gold': '#C2A36B',
        'boong-stone': '#DCD6CB'
      },
      fontFamily: {
        'display': ['Playfair Display','Georgia','serif'],
        'body': ['Source Sans 3','system-ui','sans-serif'],
        'boong-serif': ['Cormorant Garamond','Georgia','serif'],
        'boong-sans': ['Outfit','system-ui','sans-serif']
      },
      boxShadow: {
        'hero-lg': '0 30px 60px rgba(0,0,0,0.45)',
      },
      borderColor: theme => ({
        ...theme('colors'),
        'panel-divider': '#e9dcd3',
      })
    },
  },
  plugins: [],
}
