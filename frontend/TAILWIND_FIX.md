# Complete Tailwind CSS Configuration for Next.js

This document provides a complete, working solution for Tailwind CSS configuration in your Next.js project.

## Problem Summary
- Tailwind CSS not applying styles
- PostCSS error related to Tailwind plugin
- Tailwind classes not working anywhere in the UI

## Solution Overview
The issue was caused by:
1. Incorrect PostCSS plugin configuration
2. Improper Tailwind configuration mapping CSS variables to classes
3. Using `@apply` directives in CSS that reference classes not properly configured in Tailwind

## Step-by-Step Solution

### 1. PostCSS Configuration (`postcss.config.js`)
```javascript
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
```

### 2. Tailwind Configuration (`tailwind.config.js`)
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./ui/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: `var(--radius)`,
        md: `calc(var(--radius) - 2px)`,
        sm: "calc(var(--radius) - 4px)",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};
```

### 3. CSS Configuration (`src/app/globals.css`)
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 47.4% 11.2%;

    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;

    --popover: 0 0% 100%;
    --popover-foreground: 222.2 47.4% 11.2%;

    --card: 0 0% 100%;
    --card-foreground: 222.2 47.4% 11.2%;

    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;

    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;

    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;

    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;

    --destructive: 0 100% 50%;
    --destructive-foreground: 210 40% 98%;

    --ring: 215 20.2% 65.1%;

    --radius: 0.5rem;
  }

  .dark {
    --background: 224 71% 4%;
    --foreground: 213 31% 91%;

    --muted: 223 47% 11%;
    --muted-foreground: 215.4 16.3% 56.9%;

    --popover: 224 71% 4%;
    --popover-foreground: 215 20.2% 65.1%;

    --card: 224 71% 4%;
    --card-foreground: 213 31% 91%;

    --border: 216 34% 17%;
    --input: 216 34% 17%;

    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 1.2%;

    --secondary: 222.2 47.4% 11.2%;
    --secondary-foreground: 210 40% 98%;

    --accent: 216 34% 17%;
    --accent-foreground: 210 40% 98%;

    --destructive: 0 63% 31%;
    --destructive-foreground: 210 40% 98%;

    --ring: 216 34% 17%;

    --radius: 0.5rem;
  }
}

@layer base {
  * {
    border-color: hsl(var(--border));
  }

  body {
    background-color: hsl(var(--background));
    color: hsl(var(--foreground));
  }
}

@layer utilities {
  .text-balance {
    text-wrap: balance;
  }
}
```

### 4. Package Installation
Make sure you have the required packages installed:
```bash
npm install tailwindcss-animate
```

### 5. Clear Cache and Restart (Windows)
```bash
# Stop the development server (Ctrl+C)

# Clear Next.js cache
npx next clean

# Clear npm cache (optional)
npm cache clean --force

# Install dependencies
npm install

# Start the development server
npm run dev
```

## Verification Steps
1. After applying the configurations, restart your development server
2. Check that Tailwind classes are now working in your components
3. Verify that the UI is rendering with proper styles
4. Test that utility classes like `bg-red-500`, `text-blue-600`, etc. work correctly

## Troubleshooting
If you still experience issues:
1. Make sure all file paths in the `content` array of `tailwind.config.js` match your actual project structure
2. Verify that you're importing `globals.css` in your `layout.tsx` file
3. Check that your component files are using the correct file extensions (`.tsx` or `.jsx`)
4. Ensure that Tailwind classes are spelled correctly in your JSX

## Notes
- The `@apply` directives were removed from the CSS file to prevent conflicts during CSS processing
- CSS variables are now directly used in the CSS file instead of Tailwind classes
- The Tailwind configuration properly maps CSS variables to utility classes for use in JSX
- The `tailwindcss-animate` plugin adds support for animation utilities