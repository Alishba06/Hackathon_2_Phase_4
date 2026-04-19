---
name: frontend-ui
description: Build responsive pages, components, layouts, and styling for modern web apps. Use for frontend development tasks.
---

# Frontend Skill – Pages, Components, Layout & Styling

## Instructions

1. **Pages**
   - Use framework conventions (e.g. Next.js App Router `page.tsx`)
   - Keep pages clean and focused on composition
   - Separate UI from business logic

2. **Components**
   - Build reusable and modular components
   - Follow single-responsibility principle
   - Use props effectively and type them properly
   - Prefer server components when possible

3. **Layout**
   - Use layout files (`layout.tsx`) for shared UI
   - Implement responsive grids and flexbox
   - Maintain consistent spacing and alignment
   - Follow mobile-first design

4. **Styling**
   - Use Tailwind CSS / CSS Modules / scoped styles
   - Apply responsive utilities (`sm`, `md`, `lg`)
   - Maintain design consistency (colors, typography)
   - Avoid inline styles unless necessary

## Best Practices
- Mobile-first and responsive by default
- Keep components small and composable
- Avoid unnecessary client-side rendering
- Ensure accessibility (semantic HTML, aria labels)
- Maintain clean folder and file structure
- Reuse layout and UI patterns

## Example Structure
```tsx
// app/layout.tsx
export default function RootLayout({ children }) {
  return (
    <html>
      <body className="min-h-screen flex flex-col">
        {children}
      </body>
    </html>
  )
}
