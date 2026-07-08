/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#f0f5ff",
          100: "#dbe6ff",
          500: "#3b5bfd",
          600: "#2f47d1",
          700: "#2536a3",
        },
      },
    },
  },
  plugins: [],
}
