/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        "primary": "#00180f",
        "primary-container": "#112d23",
        "on-primary": "#ffffff",
        "on-primary-container": "#789688",
        "secondary": "#2c694e",
        "secondary-container": "#aeeecb",
        "on-secondary-container": "#316e52",
        "secondary-fixed": "#b1f0ce",
        "on-secondary-fixed-variant": "#0e5138",
        "surface": "#f9f9ff",
        "surface-container-lowest": "#ffffff",
        "surface-container-low": "#f0f3ff",
        "surface-container": "#e7eeff",
        "surface-container-high": "#dee8ff",
        "on-surface": "#111c2d",
        "on-surface-variant": "#424845",
        "outline": "#727974",
        "outline-variant": "#c1c8c3",
        "error": "#ba1a1a",
        "error-container": "#ffdad6",
        "on-error-container": "#93000a",
      },
      fontFamily: {
        headline: ["Space Grotesk", "sans-serif"],
        body: ["Hanken Grotesk", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
    },
  },
  plugins: [],
}
