import React from 'react';
import { Navbar } from './Navbar';

export function AppLayout({ children }) {
  return (
    <div className="min-h-screen bg-cream font-sans text-charcoal">
      <Navbar />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>
    </div>
  );
}
