import React from 'react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs) {
  return twMerge(clsx(inputs));
}

export function Button({ className, variant = 'primary', ...props }) {
  const baseStyles = "inline-flex items-center justify-center px-6 py-3 border text-base font-medium rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 transition-all duration-200 ease-in-out disabled:opacity-50 disabled:cursor-not-allowed";
  
  const variants = {
    primary: "border-transparent text-white bg-dark-olive hover:bg-dark-olive/90 focus:ring-dark-olive",
    secondary: "border-transparent text-charcoal bg-sage hover:bg-sage/80 focus:ring-sage",
    outline: "border-dark-olive text-dark-olive bg-transparent hover:bg-dark-olive hover:text-white focus:ring-dark-olive",
    ghost: "border-transparent text-charcoal bg-transparent hover:bg-sandstone focus:ring-sandstone shadow-none",
  };

  return (
    <button
      className={cn(baseStyles, variants[variant], className)}
      {...props}
    />
  );
}
