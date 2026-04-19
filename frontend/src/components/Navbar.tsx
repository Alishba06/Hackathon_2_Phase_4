'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Button } from '@/components/ui/Button';
import { Sheet, SheetContent, SheetTitle, SheetTrigger } from '@/components/ui/sheet';
import { Menu, User, Sun, Moon, Bot } from 'lucide-react';
import { useTheme } from 'next-themes';
import { useAuth } from '@/providers/AuthProvider';

export default function Navbar() {
  const pathname = usePathname();
  const { theme, setTheme } = useTheme();
  const { user, loading } = useAuth();
  const [mounted, setMounted] = useState(false);

  // Set mounted to true on client side to prevent SSR mismatch
  useEffect(() => {
    setMounted(true);
  }, []);

  const navLinks = [
    { name: 'Home', href: '/' },
    { name: 'Dashboard', href: '/dashboard' },
    { name: 'Tasks', href: '/tasks' },
  ];

  const toggleTheme = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark');
  };

  // Check if we're on auth pages
  const isAuthPage = pathname === '/sign-in' || pathname === '/sign-up';

  return (
    <nav className="bg-white dark:bg-gray-900 shadow-sm border-b border-gray-100 dark:border-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="flex-shrink-0 flex items-center">
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center">
                  <span className="text-white font-bold text-lg">T</span>
                </div>
                <span className="text-xl font-bold text-gray-900 dark:text-white hidden sm:block">TodoApp</span>
              </div>
            </Link>

            <div className="hidden md:ml-10 md:flex md:space-x-8">
              {navLinks.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${
                    pathname === link.href
                      ? 'border-indigo-500 text-gray-900 dark:text-white'
                      : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 dark:hover:text-gray-300'
                  }`}
                >
                  {link.name}
                </Link>
              ))}
              
              {/* AI Chat Assistant - Left nav, only for logged-in users */}
              {!loading && user && (
                <Link
                  href="/chat"
                  className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${
                    pathname === '/chat'
                      ? 'border-indigo-500 text-gray-900 dark:text-white'
                      : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 dark:hover:text-gray-300'
                  }`}
                >
                  <Bot className="w-4 h-4 mr-1" />
                  AI Chat
                </Link>
              )}
            </div>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-4">
            {/* Theme Toggle Button - Only render after mounting to prevent hydration mismatch */}
            {mounted && (
              <button
                onClick={toggleTheme}
                className="p-2 rounded-full text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 focus:outline-none"
                aria-label={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
              >
                {theme === 'dark' ? (
                  <Sun className="h-5 w-5" />
                ) : (
                  <Moon className="h-5 w-5" />
                )}
              </button>
            )}
            {/* Render a placeholder during SSR to maintain layout */}
            {!mounted && (
              <div className="p-2 rounded-full text-gray-700 dark:text-gray-300">
                <div className="h-5 w-5" />
              </div>
            )}

            {/* Auth Section - Only render after auth state is loaded */}
            {loading ? (
              // Auth loading skeleton
              <div className="flex items-center space-x-2">
                <div className="h-9 w-20 bg-gray-200 dark:bg-gray-700 rounded-md animate-pulse" />
                <div className="h-9 w-24 bg-gray-200 dark:bg-gray-700 rounded-md animate-pulse" />
              </div>
            ) : (
              <>
                {/* Sign In - Always visible (except on auth pages) */}
                {!isAuthPage && (
                  <Link href="/sign-in">
                    <Button variant="ghost" className="text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800">
                      Sign In
                    </Button>
                  </Link>
                )}

                {/* Sign Up - Only for non-authenticated users */}
                {!isAuthPage && !user && (
                  <Link href="/sign-up">
                    <Button className="bg-indigo-600 hover:bg-indigo-700 dark:bg-indigo-700 dark:hover:bg-indigo-800">
                      <User className="mr-2 h-4 w-4" /> Sign Up
                    </Button>
                  </Link>
                )}

                {/* User Profile - Only for logged-in users */}
                {!isAuthPage && user && (
                  <div className="ml-4 relative flex-shrink-0">
                    <div className="h-8 w-8 rounded-full bg-indigo-100 dark:bg-indigo-900 flex items-center justify-center">
                      <span className="text-indigo-800 dark:text-indigo-200 font-medium text-sm">
                        {user.email?.charAt(0).toUpperCase() || 'U'}
                      </span>
                    </div>
                  </div>
                )}
              </>
            )}
          </div>

          {/* Mobile Navigation */}
          <div className="md:hidden flex items-center">
            <Sheet>
              <SheetTrigger asChild>
                <Button variant="ghost" size="icon" className="text-gray-700 dark:text-gray-300">
                  <Menu className="h-6 w-6" />
                </Button>
              </SheetTrigger>
              <SheetContent side="right" className="w-[300px] sm:w-[400px] bg-white dark:bg-gray-900">
                <SheetTitle className="sr-only">Navigation Menu</SheetTitle>
                <div className="flex flex-col space-y-4 mt-8">
                  <div className="flex items-center space-x-3 pb-4 border-b border-gray-200 dark:border-gray-700">
                    {loading ? (
                      // Mobile auth loading skeleton
                      <>
                        <div className="h-10 w-10 rounded-full bg-gray-200 dark:bg-gray-700 animate-pulse" />
                        <div className="flex-1">
                          <div className="h-4 w-32 bg-gray-200 dark:bg-gray-700 rounded animate-pulse mb-2" />
                          <div className="h-3 w-20 bg-gray-200 dark:bg-gray-700 rounded animate-pulse" />
                        </div>
                      </>
                    ) : user ? (
                      <>
                        <div className="h-10 w-10 rounded-full bg-indigo-100 dark:bg-indigo-900 flex items-center justify-center">
                          <span className="text-indigo-800 dark:text-indigo-200 font-medium">
                            {user.email?.charAt(0).toUpperCase() || 'U'}
                          </span>
                        </div>
                        <div>
                          <p className="text-sm font-medium text-gray-900 dark:text-white">
                            {user.email || 'User Account'}
                          </p>
                          <p className="text-xs text-gray-500 dark:text-gray-400">Free Plan</p>
                        </div>
                      </>
                    ) : (
                      <>
                        <div className="h-10 w-10 rounded-full bg-indigo-100 dark:bg-indigo-900 flex items-center justify-center">
                          <span className="text-indigo-800 dark:text-indigo-200 font-medium">U</span>
                        </div>
                        <div>
                          <p className="text-sm font-medium text-gray-900 dark:text-white">User Account</p>
                          <p className="text-xs text-gray-500 dark:text-gray-400">Free Plan</p>
                        </div>
                      </>
                    )}
                  </div>

                  {navLinks.map((link) => (
                    <Link key={link.href} href={link.href}>
                      <Button
                        variant={pathname === link.href ? 'secondary' : 'ghost'}
                        className={`w-full justify-start ${
                          pathname === link.href
                            ? 'bg-indigo-50 dark:bg-indigo-800 text-indigo-700 dark:text-indigo-200 border border-indigo-200 dark:border-indigo-700'
                            : 'text-gray-700 dark:text-gray-300'
                        }`}
                        asChild
                      >
                        <span>{link.name}</span>
                      </Button>
                    </Link>
                  ))}
                  
                  {/* AI Chat Assistant - Mobile - Only for logged-in users */}
                  {!loading && user && (
                    <Link href="/chat">
                      <Button
                        variant={pathname === '/chat' ? 'secondary' : 'ghost'}
                        className={`w-full justify-start ${
                          pathname === '/chat'
                            ? 'bg-indigo-50 dark:bg-indigo-800 text-indigo-700 dark:text-indigo-200 border border-indigo-200 dark:border-indigo-700'
                            : 'text-gray-700 dark:text-gray-300'
                        }`}
                        asChild
                      >
                        <span>
                          <Bot className="w-4 h-4 mr-2 inline" />
                          AI Chat Assistant
                        </span>
                      </Button>
                    </Link>
                  )}

                  {/* Mobile Auth Buttons - Only show after loading complete */}
                  {!loading && !isAuthPage && !user && (
                    <>
                      <div className="pt-4 mt-4 border-t border-gray-200 dark:border-gray-700">
                        <Link href="/sign-in">
                          <Button variant="outline" className="w-full mb-2 text-gray-700 dark:text-gray-300 border-gray-300 dark:border-gray-700">Sign In</Button>
                        </Link>
                        <Link href="/sign-up">
                          <Button className="w-full bg-indigo-600 hover:bg-indigo-700 dark:bg-indigo-700 dark:hover:bg-indigo-800">
                            <User className="mr-2 h-4 w-4" /> Sign Up
                          </Button>
                        </Link>
                      </div>
                    </>
                  )}
                </div>
              </SheetContent>
            </Sheet>
          </div>
        </div>
      </div>
    </nav>
  );
}