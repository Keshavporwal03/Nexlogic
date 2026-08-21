import React from 'react';
import { cn } from './Button';

export const Input = React.forwardRef(({ className, type, ...props }, ref) => {
  return (
    <input
      type={type}
      className={cn(
        "block w-full rounded-md border border-sandstone shadow-sm focus:border-dark-olive focus:ring-1 focus:ring-dark-olive sm:text-sm bg-sandstone-light/50 text-charcoal placeholder-brown-grey px-4 py-3 outline-none transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed",
        className
      )}
      ref={ref}
      {...props}
    />
  );
});

Input.displayName = "Input";
