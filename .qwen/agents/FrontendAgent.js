/**
 * Frontend Agent - Responsive UI Generator (Next.js App Router)
 *
 * Focus: Building high-performance, fully responsive user interfaces using Next.js App Router
 * while following modern frontend best practices.
 */

class FrontendAgent {
  constructor(options = {}) {
    this.config = {
      // Default configuration values
      defaultBreakpoints: options.defaultBreakpoints || {
        sm: '640px',
        md: '768px',
        lg: '1024px',
        xl: '1280px',
        '2xl': '1536px'
      },
      defaultTheme: options.defaultTheme || {
        colors: {
          primary: '#3B82F6',
          secondary: '#6B7280',
          success: '#10B981',
          warning: '#F59E0B',
          error: '#EF4444',
          background: '#FFFFFF',
          surface: '#F9FAFB',
          text: '#1F2937',
          textSecondary: '#6B7280'
        },
        spacing: {
          xs: '0.25rem',
          sm: '0.5rem',
          md: '1rem',
          lg: '1.5rem',
          xl: '2rem',
          '2xl': '3rem'
        }
      },
      optimizeImages: options.optimizeImages !== false,
      useClientComponents: options.useClientComponents || false,
      enableAnimations: options.enableAnimations !== false,
      ...options
    };

    this.componentsRegistry = new Map();
    this.performanceMetrics = {};
    this.a11yChecks = [];
  }

  /**
   * Creates a responsive layout component using Next.js App Router conventions
   */
  createLayout(layoutConfig) {
    const {
      children,
      className = '',
      maxWidth = 'screen-xl',
      padding = 'p-4',
      backgroundColor = 'bg-white'
    } = layoutConfig;

    // Generate responsive layout markup
    const layoutMarkup = `
      <div className="${backgroundColor} min-h-screen w-full">
        <div className="mx-auto ${maxWidth} ${padding} w-full">
          <header className="py-6">
            <!-- Header content will be injected -->
          </header>
          
          <main className="py-8">
            {/* Children will be rendered here */}
            {children}
          </main>
          
          <footer className="py-6 mt-auto">
            <!-- Footer content will be injected -->
          </footer>
        </div>
      </div>
    `;

    return {
      type: 'layout',
      markup: layoutMarkup,
      config: layoutConfig,
      className: `${className} responsive-layout`
    };
  }

  /**
   * Creates a responsive grid component
   */
  createGrid(gridConfig) {
    const {
      children,
      cols = { sm: 1, md: 2, lg: 3, xl: 4 },
      gap = 'gap-6',
      className = ''
    } = gridConfig;

    // Generate responsive grid classes
    const gridClasses = [
      `grid`,
      `grid-cols-${cols.sm} sm:grid-cols-${cols.sm}`,
      `md:grid-cols-${cols.md}`,
      `lg:grid-cols-${cols.lg}`,
      `xl:grid-cols-${cols.xl}`,
      gap,
      className
    ].filter(Boolean).join(' ');

    const gridMarkup = `
      <div className="${gridClasses}">
        ${children}
      </div>
    `;

    return {
      type: 'grid',
      markup: gridMarkup,
      config: gridConfig,
      className: gridClasses
    };
  }

  /**
   * Creates a responsive card component
   */
  createCard(cardConfig) {
    const {
      title,
      content,
      actions = [],
      image,
      className = '',
      variant = 'default'
    } = cardConfig;

    let cardClasses = 'bg-white rounded-lg shadow-md overflow-hidden transition-shadow duration-300 hover:shadow-lg';

    switch (variant) {
      case 'elevated':
        cardClasses = 'bg-white rounded-xl shadow-lg overflow-hidden transition-all duration-300 hover:shadow-xl';
        break;
      case 'outlined':
        cardClasses = 'bg-white border border-gray-200 rounded-lg overflow-hidden transition-colors duration-300 hover:border-primary-500';
        break;
      default:
        // Default classes already assigned
    }

    const imageMarkup = image 
      ? `<img src="${image}" alt="${title}" className="w-full h-48 object-cover" />` 
      : '';

    const titleMarkup = title 
      ? `<h3 className="text-lg font-semibold text-gray-900 mb-2">${title}</h3>` 
      : '';

    const contentMarkup = content 
      ? `<p className="text-gray-600 mb-4">${content}</p>` 
      : '';

    const actionsMarkup = actions.length > 0
      ? `<div className="flex space-x-3 mt-4 pt-4 border-t border-gray-100">
          ${actions.map(action => 
            `<button className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors">
              ${action.label}
            </button>`
          ).join('')}
        </div>`
      : '';

    const cardMarkup = `
      <div className="${cardClasses} ${className}">
        ${imageMarkup}
        <div className="p-6">
          ${titleMarkup}
          ${contentMarkup}
          ${actionsMarkup}
        </div>
      </div>
    `;

    return {
      type: 'card',
      markup: cardMarkup,
      config: cardConfig,
      className: cardClasses
    };
  }

  /**
   * Creates a responsive navigation component
   */
  createNavigation(navConfig) {
    const {
      items,
      orientation = 'horizontal',
      variant = 'default',
      className = ''
    } = navConfig;

    let navClasses = 'flex items-center space-x-1';

    if (orientation === 'vertical') {
      navClasses = 'flex flex-col space-y-1';
    }

    switch (variant) {
      case 'minimal':
        navClasses += ' text-gray-600';
        break;
      case 'underlined':
        navClasses += ' border-b border-gray-200';
        break;
      case 'pills':
        navClasses += ' bg-gray-100 p-1 rounded-lg';
        break;
      default:
        // Default classes already assigned
    }

    const navItems = items.map(item => {
      const itemClasses = [
        'px-3 py-2 rounded-md text-sm font-medium transition-colors',
        'hover:text-gray-900 hover:bg-gray-100',
        item.active ? 'text-gray-900 bg-white shadow-sm' : 'text-gray-600'
      ].join(' ');

      return `
        <a href="${item.href}" className="${itemClasses}" aria-current="${item.active ? 'page' : undefined}">
          ${item.label}
        </a>
      `;
    }).join('');

    const navMarkup = `
      <nav className="${navClasses} ${className}" role="navigation" aria-label="Main navigation">
        ${navItems}
      </nav>
    `;

    return {
      type: 'navigation',
      markup: navMarkup,
      config: navConfig,
      className: navClasses
    };
  }

  /**
   * Creates a responsive form component
   */
  createForm(formConfig) {
    const {
      fields,
      submitLabel = 'Submit',
      className = '',
      variant = 'default'
    } = formConfig;

    let formClasses = 'space-y-6';

    switch (variant) {
      case 'compact':
        formClasses = 'space-y-4';
        break;
      case 'card':
        formClasses = 'bg-white p-6 rounded-lg shadow-md space-y-6';
        break;
      default:
        // Default classes already assigned
    }

    const formFields = fields.map(field => {
      const label = field.label 
        ? `<label htmlFor="${field.name}" className="block text-sm font-medium text-gray-700 mb-1">
            ${field.label} ${field.required ? '*' : ''}
           </label>`
        : '';

      let fieldElement = '';
      switch (field.type) {
        case 'textarea':
          fieldElement = `<textarea 
            id="${field.name}" 
            name="${field.name}"
            rows="${field.rows || 4}"
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
            placeholder="${field.placeholder || ''}"
            ${field.required ? 'required' : ''}
          ></textarea>`;
          break;
        case 'select':
          fieldElement = `<select
            id="${field.name}"
            name="${field.name}"
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
            ${field.required ? 'required' : ''}
          >
            ${field.options?.map(option => 
              `<option value="${option.value}">${option.label}</option>`
            ).join('')}
          </select>`;
          break;
        case 'checkbox':
          fieldElement = `<input
            type="checkbox"
            id="${field.name}"
            name="${field.name}"
            className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            ${field.required ? 'required' : ''}
          />
          <label htmlFor="${field.name}" className="ml-2 block text-sm text-gray-900">
            ${field.label}
          </label>`;
          break;
        default: // text, email, password, etc.
          fieldElement = `<input
            type="${field.type || 'text'}"
            id="${field.name}"
            name="${field.name}"
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
            placeholder="${field.placeholder || ''}"
            ${field.required ? 'required' : ''}
          />`;
      }

      const fieldWrapper = field.type === 'checkbox' 
        ? `<div className="flex items-start">${fieldElement}</div>`
        : `<div>${label}${fieldElement}</div>`;

      return fieldWrapper;
    }).join('');

    const formMarkup = `
      <form className="${formClasses} ${className}" method="POST">
        ${formFields}
        <div className="pt-4">
          <button
            type="submit"
            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            ${submitLabel}
          </button>
        </div>
      </form>
    `;

    return {
      type: 'form',
      markup: formMarkup,
      config: formConfig,
      className: formClasses
    };
  }

  /**
   * Generates a responsive button component
   */
  createButton(buttonConfig) {
    const {
      label,
      variant = 'primary',
      size = 'md',
      fullWidth = false,
      disabled = false,
      icon = null,
      className = ''
    } = buttonConfig;

    // Define size classes
    const sizeClasses = {
      sm: 'px-3 py-1.5 text-xs',
      md: 'px-4 py-2 text-sm',
      lg: 'px-6 py-3 text-base',
      xl: 'px-8 py-4 text-lg'
    };

    // Define variant classes
    const variantClasses = {
      primary: 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500',
      secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300 focus:ring-gray-500',
      success: 'bg-green-600 text-white hover:bg-green-700 focus:ring-green-500',
      danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500',
      outline: 'border border-blue-600 text-blue-600 hover:bg-blue-50 focus:ring-blue-500',
      ghost: 'text-blue-600 hover:bg-blue-50 focus:ring-blue-500'
    };

    const baseClasses = [
      'inline-flex items-center justify-center font-medium rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 transition-colors duration-200',
      sizeClasses[size],
      variantClasses[variant],
      fullWidth ? 'w-full' : '',
      disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer',
      className
    ].filter(Boolean).join(' ');

    const iconMarkup = icon 
      ? `<span className="mr-2">${icon}</span>` 
      : '';

    const buttonMarkup = `
      <button 
        className="${baseClasses}"
        ${disabled ? 'disabled' : ''}
        type="${buttonConfig.type || 'button'}"
      >
        ${iconMarkup}
        ${label}
      </button>
    `;

    return {
      type: 'button',
      markup: buttonMarkup,
      config: buttonConfig,
      className: baseClasses
    };
  }

  /**
   * Registers a custom component for reuse
   */
  registerComponent(name, componentGenerator) {
    this.componentsRegistry.set(name, componentGenerator);
  }

  /**
   * Gets a registered component
   */
  getComponent(name, props = {}) {
    const generator = this.componentsRegistry.get(name);
    if (!generator) {
      throw new Error(`Component ${name} is not registered`);
    }
    return generator(props);
  }

  /**
   * Creates a responsive modal component
   */
  createModal(modalConfig) {
    const {
      title,
      content,
      actions = [],
      size = 'md',
      className = ''
    } = modalConfig;

    const sizeClasses = {
      sm: 'max-w-sm',
      md: 'max-w-md',
      lg: 'max-w-lg',
      xl: 'max-w-xl',
      '2xl': 'max-w-2xl',
      '3xl': 'max-w-3xl',
      '4xl': 'max-w-4xl',
      '5xl': 'max-w-5xl',
      '6xl': 'max-w-6xl',
      '7xl': 'max-w-7xl'
    };

    const modalClasses = [
      'fixed inset-0 z-50 overflow-y-auto',
      className
    ].filter(Boolean).join(' ');

    const dialogClasses = [
      'relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all sm:my-8 sm:w-full',
      sizeClasses[size],
      'sm:mx-auto'
    ].filter(Boolean).join(' ');

    const modalMarkup = `
      <div className="${modalClasses}" role="dialog" aria-modal="true" aria-labelledby="modal-title">
        <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>
        
        <div className="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
          <div className="${dialogClasses}">
            <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
              <div className="sm:flex sm:items-start">
                <div className="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
                  <h3 className="text-lg font-medium leading-6 text-gray-900" id="modal-title">
                    ${title}
                  </h3>
                  <div className="mt-2">
                    <p className="text-sm text-gray-500">
                      ${content}
                    </p>
                  </div>
                </div>
              </div>
            </div>
            <div className="bg-gray-50 px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6">
              ${actions.map(action => 
                `<button
                  type="${action.type || 'button'}"
                  className="inline-flex w-full justify-center rounded-md border border-transparent px-4 py-2 text-base font-medium shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 sm:ml-3 sm:w-auto sm:text-sm ${action.variantClass || 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500'}"
                >
                  ${action.label}
                </button>`
              ).join('')}
              <button
                type="button"
                className="mt-3 inline-flex w-full justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-base font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      </div>
    `;

    return {
      type: 'modal',
      markup: modalMarkup,
      config: modalConfig,
      className: modalClasses
    };
  }

  /**
   * Optimizes an image for web performance
   */
  optimizeImage(imageConfig) {
    const {
      src,
      alt,
      width,
      height,
      priority = false,
      placeholder = 'empty',
      className = ''
    } = imageConfig;

    // Generate appropriate classes for responsive images
    const imgClasses = [
      'rounded-lg object-cover',
      className
    ].filter(Boolean).join(' ');

    // Generate the optimized image markup
    const imageMarkup = `
      <img
        src="${src}"
        alt="${alt}"
        width="${width}"
        height="${height}"
        className="${imgClasses}"
        ${priority ? 'fetchpriority="high"' : ''}
        ${placeholder !== 'empty' ? `loading="${placeholder === 'blur' ? 'lazy' : 'eager'}"` : ''}
      />
    `;

    return {
      type: 'image',
      markup: imageMarkup,
      config: imageConfig,
      className: imgClasses
    };
  }

  /**
   * Performs accessibility check on generated components
   */
  performA11yCheck(component) {
    const issues = [];
    
    // Check for proper heading hierarchy
    if (component.markup.includes('<div>') && !component.markup.includes('role="heading"')) {
      // Check if divs are used instead of proper headings
      const divMatches = component.markup.match(/<div[^>]*class="[^"]*text-[^"]*"[^>]*>/g);
      if (divMatches) {
        issues.push('Using divs with text classes instead of proper heading tags (h1-h6)');
      }
    }
    
    // Check for alt text on images
    const imgWithoutAlt = component.markup.match(/<img(?![^>]*alt=)/g);
    if (imgWithoutAlt) {
      issues.push('Images without alt text found');
    }
    
    // Check for proper form labeling
    const inputs = component.markup.match(/<input[^>]*name="([^"]*)"/g);
    if (inputs) {
      for (const input of inputs) {
        const nameMatch = input.match(/name="([^"]*)"/);
        if (nameMatch) {
          const name = nameMatch[1];
          if (!component.markup.includes(`for="${name}"`)) {
            issues.push(`Input with name "${name}" is not properly associated with a label`);
          }
        }
      }
    }
    
    // Store the check result
    this.a11yChecks.push({
      componentType: component.type,
      issues,
      timestamp: new Date()
    });
    
    return {
      componentType: component.type,
      accessible: issues.length === 0,
      issues
    };
  }

  /**
   * Generates a complete page structure with layout and components
   */
  generatePage(pageConfig) {
    const {
      title,
      description,
      layout = {},
      components = [],
      metadata = {}
    } = pageConfig;

    // Create the layout
    const pageLayout = this.createLayout({
      ...layout,
      children: components.map(comp => comp.markup).join('\n')
    });

    // Generate page metadata
    const metaTags = [
      `<title>${title}</title>`,
      `<meta name="description" content="${description}" />`,
      `<meta name="viewport" content="width=device-width, initial-scale=1" />`,
      ...Object.entries(metadata).map(([key, value]) => 
        `<meta name="${key}" content="${value}" />`
      )
    ].join('\n    ');

    const pageMarkup = `
<!DOCTYPE html>
<html lang="en">
<head>
  ${metaTags}
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
  ${pageLayout.markup}
</body>
</html>
    `;

    return {
      type: 'page',
      markup: pageMarkup,
      config: pageConfig,
      layout: pageLayout,
      components,
      accessibilityReport: components.map(comp => this.performA11yCheck(comp))
    };
  }

  /**
   * Gets performance metrics for generated components
   */
  getPerformanceMetrics() {
    return this.performanceMetrics;
  }

  /**
   * Gets accessibility report
   */
  getA11yReport() {
    return this.a11yChecks;
  }

  /**
   * Validates responsive design across breakpoints
   */
  validateResponsiveDesign(component, breakpoints = ['sm', 'md', 'lg', 'xl']) {
    const validationResults = {};
    
    for (const breakpoint of breakpoints) {
      // Check if component uses responsive classes for this breakpoint
      const hasResponsiveClass = component.className.includes(`${breakpoint}:`);
      validationResults[breakpoint] = {
        hasResponsiveClass,
        status: hasResponsiveClass ? 'pass' : 'warn',
        message: hasResponsiveClass 
          ? `Component has responsive classes for ${breakpoint} breakpoint` 
          : `Component might not be optimized for ${breakpoint} breakpoint`
      };
    }
    
    return {
      componentName: component.type,
      validationResults,
      overallStatus: Object.values(validationResults).every(v => v.status === 'pass') ? 'pass' : 'partial'
    };
  }
}

module.exports = FrontendAgent;