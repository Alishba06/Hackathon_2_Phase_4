# Frontend Agent – Skills and Optimization Practices

## Core Skills

### 1. Frontend Skill (Primary)
- **Next.js App Router Mastery**: Deep understanding of App Router conventions, layouts, loading states, and error handling
- **React Component Development**: Expertise in creating reusable, well-structured React components
- **Responsive Design**: Proficiency in creating mobile-first, responsive UIs that work across devices
- **Modern CSS**: Advanced knowledge of Tailwind CSS, CSS Modules, and responsive utilities
- **Performance Optimization**: Understanding of rendering optimization, code splitting, and bundle size reduction
- **Accessibility (a11y)**: Knowledge of WCAG guidelines and accessible component development

### 2. Architecture Skills
- **Component Architecture**: Ability to design scalable component hierarchies
- **State Management**: Understanding of when to use server vs client components
- **Folder Structure**: Knowledge of organizing code according to App Router conventions
- **Design Systems**: Experience creating and maintaining consistent UI systems
- **Theming**: Ability to implement flexible theme systems
- **Internationalization**: Understanding of i18n considerations in UI design

### 3. Performance Skills
- **Bundle Optimization**: Knowledge of reducing bundle sizes and optimizing loading
- **Image Optimization**: Expertise in using `next/image` for optimal performance
- **Dynamic Imports**: Understanding of when and how to implement code splitting
- **Caching Strategies**: Knowledge of implementing effective caching patterns
- **Rendering Optimization**: Understanding of SSR, SSG, and client-side rendering trade-offs
- **Web Vitals**: Experience in optimizing Core Web Vitals metrics

### 4. Testing Skills
- **Component Testing**: Experience with testing React components
- **Visual Regression Testing**: Knowledge of tools for catching UI regressions
- **Accessibility Testing**: Understanding of automated and manual accessibility testing
- **Cross-Browser Testing**: Experience testing across different browsers and devices
- **Performance Testing**: Knowledge of measuring and optimizing performance metrics
- **Responsive Testing**: Experience testing across different screen sizes

## Optimization Practices

### 1. Component Optimization
- **Minimize Client Components**: Use server components by default, only use client when necessary
- **Component Composition**: Build complex UIs from simple, composable components
- **Conditional Rendering**: Implement efficient conditional rendering patterns
- **Memoization**: Use React.memo and useMemo appropriately
- **Event Handling**: Optimize event handling to prevent unnecessary re-renders
- **Props Optimization**: Pass only necessary props to components

### 2. Image Optimization
- **Use next/image**: Always use Next.js Image component for optimization
- **Optimal Dimensions**: Specify width and height to prevent layout shift
- **Format Selection**: Use modern formats (WebP, AVIF) when possible
- **Loading Strategy**: Implement lazy loading for off-screen images
- **Placeholder Strategy**: Use blur-up or color placeholders appropriately
- **Responsive Images**: Implement responsive images with srcSet

### 3. Code Splitting and Dynamic Imports
- **Route-Level Splitting**: Leverage Next.js automatic route splitting
- **Component-Level Splitting**: Use dynamic imports for heavy components
- **Library Splitting**: Split heavy libraries into separate bundles
- **Conditional Loading**: Load components only when needed
- **Prefetching**: Implement prefetching for critical navigation paths
- **Bundle Analysis**: Regularly analyze and optimize bundle sizes

### 4. Data Fetching Optimization
- **Server-Side Fetching**: Fetch data on the server when possible
- **Streaming**: Implement streaming for faster content delivery
- **Caching**: Use appropriate caching strategies (HTTP, CDN, client-side)
- **Request Deduplication**: Prevent duplicate requests
- **Progressive Loading**: Show content as it becomes available
- **Error Handling**: Implement proper error boundaries and fallbacks

### 5. CSS and Styling Optimization
- **Utility-First Approach**: Leverage Tailwind CSS for efficient styling
- **CSS Purging**: Ensure unused styles are removed in production
- **Critical CSS**: Inline critical CSS for faster rendering
- **Theme Isolation**: Separate theme definitions from component styles
- **Responsive Utilities**: Use responsive prefixes effectively
- **Animation Optimization**: Use hardware-accelerated animations

### 6. Accessibility Optimization
- **Semantic HTML**: Use proper HTML elements for their intended purpose
- **ARIA Labels**: Add appropriate ARIA attributes for accessibility
- **Keyboard Navigation**: Ensure all functionality is keyboard accessible
- **Focus Management**: Implement proper focus management
- **Color Contrast**: Maintain sufficient color contrast ratios
- **Screen Reader Support**: Ensure content is properly announced by screen readers

## Best Practices

### 1. App Router Structure
- **Layout Files**: Use layout.tsx files for shared UI and wrapper components
- **Page Files**: Use page.tsx files for route-specific content
- **Route Groups**: Organize routes using route groups for logical separation
- **Parallel Routes**: Implement parallel routes when appropriate
- **Loading UI**: Implement loading.tsx files for loading states
- **Error Handling**: Use error.tsx files for error boundaries

### 2. Performance Best Practices
- **Early Return Patterns**: Implement early returns to minimize computation
- **Debouncing/Throttling**: Apply to expensive operations like scrolling or resizing
- **Virtual Scrolling**: Implement for large lists of items
- **Intersection Observer**: Use for detecting element visibility
- **Resource Hints**: Implement prefetch and preload hints appropriately
- **Font Optimization**: Use Next.js font optimization features

### 3. Security Best Practices
- **Sanitization**: Sanitize user-generated content before rendering
- **CSP Headers**: Implement Content Security Policy headers
- **Input Validation**: Validate all user inputs on the client side
- **Secure Links**: Use rel="noopener noreferrer" for external links
- **Data Attributes**: Sanitize data attributes to prevent XSS
- **Third-Party Scripts**: Carefully vet and isolate third-party scripts

### 4. Development Best Practices
- **Type Safety**: Use TypeScript for all components and props
- **Consistent Naming**: Follow consistent naming conventions
- **Documentation**: Document components with JSDoc/TSDoc
- **Code Organization**: Group related functionality logically
- **Reusable Utilities**: Create utility functions for common operations
- **Version Control**: Follow proper Git practices for frontend code

## Quality Standards

### 1. Performance Standards
- **Core Web Vitals**: Meet Google's Core Web Vitals thresholds
- **Bundle Size**: Maintain reasonable bundle sizes (under 250KB for main bundle)
- **Loading Speed**: Achieve fast initial loading times
- **Render Performance**: Minimize render blocking resources
- **Resource Optimization**: Optimize all assets (images, fonts, etc.)
- **Memory Usage**: Minimize memory consumption

### 2. Accessibility Standards
- **WCAG Compliance**: Meet WCAG 2.1 AA standards
- **Keyboard Navigation**: Ensure full keyboard operability
- **Screen Reader Support**: Ensure compatibility with assistive technologies
- **Focus Indicators**: Provide visible focus indicators
- **Alternative Text**: Provide appropriate alt text for images
- **Form Labels**: Associate form controls with proper labels

### 3. Compatibility Standards
- **Browser Support**: Support modern browsers (last 2 versions)
- **Device Responsiveness**: Work well on all screen sizes
- **Touch Targets**: Ensure adequate touch target sizes
- **Cross-Platform Consistency**: Maintain consistent experience across platforms
- **Legacy Browser Fallbacks**: Provide graceful degradation when needed
- **Performance Across Devices**: Optimize for various device capabilities

## Operational Guidelines

### 1. Change Management
- **Incremental Changes**: Implement changes in small, testable units
- **Performance Monitoring**: Monitor performance after each change
- **Accessibility Testing**: Test accessibility after each change
- **Responsive Testing**: Verify responsiveness across devices after changes
- **Regression Testing**: Ensure existing functionality remains intact

### 2. Review Process
- **Code Reviews**: Subject all changes to peer review
- **Performance Reviews**: Evaluate performance impact of changes
- **Accessibility Reviews**: Verify accessibility compliance
- **Design Reviews**: Ensure consistency with design system
- **Cross-Browser Reviews**: Test across different browsers
- **Mobile Reviews**: Verify mobile experience