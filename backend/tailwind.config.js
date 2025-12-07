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
        'asian-red': '##b22b23',
        'page-beige': '#f5eadf',
        'hero-black': '#0b0b0b'
      },
      fontFamily: {
        'display': ['Playfair Display','Georgia','serif'],
        'body': ['Source Sans 3','system-ui','sans-serif']
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
