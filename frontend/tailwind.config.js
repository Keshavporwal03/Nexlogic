/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        charcoal: '#1F1F1F',
        sandstone: '#E6DED3',
        taupe: '#D2C8BB',
        sage: '#A8B5A2',
        'brown-grey': '#6F6A63',
        'sandstone-light': '#F5F1ED',
        cream: '#F9F6F2',
        white: '#FFFFFF',
        'dark-olive': '#384F3E',
        // Semantic mappings
        primary: '#384F3E',
        secondary: '#A8B5A2',
        background: '#F9F6F2', // Using cream as default background
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'], // Professional font mapping
        heading: ['Montserrat', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
