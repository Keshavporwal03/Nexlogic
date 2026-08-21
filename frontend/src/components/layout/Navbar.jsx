import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { cn } from '../ui/Button';

export function Navbar() {
  const location = useLocation();

  const links = [
    { name: 'Job Management', path: '/jobs' },
    { name: 'Candidate Search', path: '/' },
    { name: 'Banner Generator', path: '/banner' },
    { name: 'Post Generator', path: '/post' },
    { name: 'Company Profile', path: '/profile' },
  ];

  return (
    <nav className="bg-white border-b border-sandstone-light sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <div className="flex-shrink-0 flex items-center">
              <span className="text-xl font-bold font-sans text-dark-olive tracking-tight">
                ARA
              </span>
            </div>
            <div className="hidden sm:ml-8 sm:flex sm:space-x-8">
              {links.map((link) => (
                <Link
                  key={link.path}
                  to={link.path}
                  className={cn(
                    "inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors",
                    location.pathname === link.path
                      ? "border-dark-olive text-charcoal"
                      : "border-transparent text-brown-grey hover:border-sandstone hover:text-charcoal"
                  )}
                >
                  {link.name}
                </Link>
              ))}
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}
