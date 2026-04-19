import * as React from 'react';
import { cn } from '@/lib/utils';

// Define the props for the Input component
export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
  as?: 'input' | 'textarea';
  rows?: number;
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({
    className,
    type,
    label,
    error,
    helperText,
    as = 'input',
    rows = 4,
    ...props
  }, ref) => {
    const hasError = !!error;

    // Check if this is being used as a form element with label (like in auth forms)
    const isFormElement = label || error || helperText;

    if (isFormElement) {
      // Return the form element version with label and error handling
      return (
        <div className="w-full space-y-1">
          {label && (
            <label className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
              {label}
            </label>
          )}
          <input
            type={type}
            className={cn(
              'w-full rounded-md border px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50',
              hasError
                ? 'border-red-500 bg-red-50'
                : 'border-input bg-background',
              className
            )}
            ref={ref as React.ForwardedRef<HTMLInputElement>}
            {...props}
          />
          {helperText && !hasError && (
            <p className="text-xs text-gray-500">{helperText}</p>
          )}
          {error && (
            <p className="text-xs text-red-500">{error}</p>
          )}
        </div>
      );
    } else {
      // Return the standard shadcn/ui style input
      return (
        <input
          type={type}
          className={cn(
            'flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50',
            className
          )}
          ref={ref as React.ForwardedRef<HTMLInputElement>}
          {...props}
        />
      );
    }
  }
);
Input.displayName = 'Input';

export { Input };
export default Input;