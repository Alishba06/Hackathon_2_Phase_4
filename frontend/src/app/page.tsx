'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/Button';
import { useAuth } from '@/providers/AuthProvider';
import { taskApi } from '@/lib/api/endpoints';

// Define the Task type based on the backend model
interface Task {
  id: string;
  title: string;
  description?: string;
  is_completed: boolean;
  due_date?: string;
  priority: 'low' | 'medium' | 'high';
  user_id: string;
  created_at: string;
  updated_at: string;
}

const HomePage = () => {
  const { isAuthenticated } = useAuth();
  
  // State for tasks and statistics
  const [tasks, setTasks] = useState<Task[]>([]);
  const [totalTasks, setTotalTasks] = useState<number>(0);
  const [completedTasks, setCompletedTasks] = useState<number>(0);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch tasks when component mounts (only if authenticated)
  useEffect(() => {
    // Only fetch tasks if user is authenticated
    if (!isAuthenticated) {
      setLoading(false);
      return;
    }

    const fetchTasks = async () => {
      try {
        setLoading(true);
        const fetchedTasks = await taskApi.getAllTasks();
        setTasks(fetchedTasks);

        // Calculate statistics
        const total = fetchedTasks.length;
        const completed = fetchedTasks.filter((task: Task) => task.is_completed).length;

        setTotalTasks(total);
        setCompletedTasks(completed);

        setError(null);
      } catch (err: any) {
        console.error('Error fetching tasks:', err);
        // Don't show error for unauthenticated users - they should just see empty state
        if (err.message !== 'Authentication failed. Please log in again.') {
          setError('Failed to load tasks. Please refresh the page.');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, [isAuthenticated]);

  // Format due date for display
  const formatDate = (dateString: string | undefined) => {
    if (!dateString) return '';
    
    const date = new Date(dateString);
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);
    
    if (date.toDateString() === today.toDateString()) {
      return 'Today';
    } else if (date.toDateString() === tomorrow.toDateString()) {
      return 'Tomorrow';
    } else {
      return date.toLocaleDateString();
    }
  };

  // Get priority color
  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'text-red-500';
      case 'medium': return 'text-yellow-500';
      case 'low': return 'text-green-500';
      default: return 'text-gray-500';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-cyan-50 flex flex-col">
      {/* Hero Section */}
      <div className="flex-grow flex items-center py-8 sm:py-12 px-4">
        <div className="max-w-7xl mx-auto w-full">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 md:gap-12 items-center">
            <div className="text-center lg:text-left order-2 lg:order-1">
              <h1 className="text-4xl md:text-5xl font-bold text-gray-900 leading-tight">
                Organize Your Life with <span className="text-indigo-600">TodoApp</span>
              </h1>
              <p className="mt-6 text-lg text-gray-600 max-w-xl mx-auto lg:mx-0">
                A beautiful, responsive task manager that helps you stay productive and organized.
                Track your tasks, set priorities, and achieve your goals.
              </p>

              <div className="mt-10 flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
                <Link href="/tasks">
                  <Button className="bg-indigo-600 hover:bg-indigo-700 text-white px-8 py-3 text-base font-medium rounded-lg transition-all duration-300 transform hover:-translate-y-0.5">
                    Get Started
                  </Button>
                </Link>
                <Link href="/dashboard">
                  <Button variant="outline" className="px-8 py-3 text-base font-medium rounded-lg transition-all duration-300">
                    View Dashboard
                  </Button>
                </Link>
              </div>
            </div>

            <div className="relative order-1 lg:order-2">
              <div className="bg-white rounded-2xl shadow-xl p-4 sm:p-6 border border-gray-100">
                <div className="flex items-center space-x-2 mb-4">
                  <div className="w-3 h-3 rounded-full bg-red-400"></div>
                  <div className="w-3 h-3 rounded-full bg-yellow-400"></div>
                  <div className="w-3 h-3 rounded-full bg-green-400"></div>
                </div>

                <div className="space-y-4">
                  {loading ? (
                    <div className="text-center py-6">
                      <p>Loading tasks...</p>
                    </div>
                  ) : error ? (
                    <div className="text-center py-6 text-red-500">
                      <p>{error}</p>
                    </div>
                  ) : tasks.length > 0 ? (
                    tasks.slice(0, 3).map((task) => (
                      <div 
                        key={task.id} 
                        className={`flex items-start space-x-3 p-3 rounded-lg hover:bg-gray-50 transition-colors ${
                          task.is_completed ? 'bg-indigo-50 border border-indigo-100' : ''
                        }`}
                      >
                        <div className={`mt-1 h-5 w-5 rounded-full border flex items-center justify-center ${
                          task.is_completed ? 'border-indigo-300' : 'border-gray-300'
                        }`}>
                          <div className={`h-3 w-3 rounded-full bg-indigo-500 ${
                            task.is_completed ? 'opacity-100' : 'opacity-0'
                          }`}></div>
                        </div>
                        <div className="flex-1 min-w-0">
                          <h3 className={`font-medium truncate ${
                            task.is_completed 
                              ? 'line-through text-gray-400' 
                              : 'text-gray-900'
                          }`}>
                            {task.title}
                          </h3>
                          <p className="text-xs sm:text-sm text-gray-500 mt-1">
                            {task.is_completed 
                              ? `Completed • Priority: ${task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}`
                              : `Due: ${formatDate(task.due_date)} • Priority: ${task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}`
                            }
                          </p>
                        </div>
                      </div>
                    ))
                  ) : (
                    <div className="text-center py-6 text-gray-500">
                      <p>No tasks yet. Create your first task!</p>
                    </div>
                  )}
                </div>

                <div className="mt-6 pt-4 border-t border-gray-100 flex justify-between items-center">
                  <span className="text-sm text-gray-500">
                    {loading ? '...' : `${totalTasks} task${totalTasks !== 1 ? 's' : ''} total`}
                  </span>
                  <span className="text-sm font-medium text-indigo-600">
                    {loading ? '...' : `${completedTasks} completed`}
                  </span>
                </div>
              </div>

              {/* Floating elements for visual interest */}
              <div className="hidden lg:block absolute -top-6 -left-6 w-24 h-24 bg-purple-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob"></div>
              <div className="hidden lg:block absolute top-10 -right-6 w-24 h-24 bg-indigo-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob animation-delay-2000"></div>
              <div className="hidden lg:block absolute -bottom-8 left-20 w-24 h-24 bg-cyan-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob animation-delay-4000"></div>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-12 sm:py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-10 sm:mb-12">
            <h2 className="text-3xl font-bold text-gray-900">Powerful Features</h2>
            <p className="mt-4 text-lg text-gray-600 max-w-2xl mx-auto">
              Everything you need to manage your tasks efficiently
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 sm:gap-8">
            <div className="bg-white p-6 sm:p-8 rounded-xl shadow-sm border border-gray-100 text-center">
              <div className="w-12 h-12 rounded-full bg-indigo-100 flex items-center justify-center mx-auto">
                <span className="text-indigo-600 font-bold">✓</span>
              </div>
              <h3 className="mt-6 text-lg font-semibold text-gray-900">Task Management</h3>
              <p className="mt-2 text-gray-600">
                Create, update, and organize your tasks with due dates and priority levels
              </p>
            </div>

            <div className="bg-white p-6 sm:p-8 rounded-xl shadow-sm border border-gray-100 text-center">
              <div className="w-12 h-12 rounded-full bg-indigo-100 flex items-center justify-center mx-auto">
                <span className="text-indigo-600 font-bold">📊</span>
              </div>
              <h3 className="mt-6 text-lg font-semibold text-gray-900">Progress Tracking</h3>
              <p className="mt-2 text-gray-600">
                Visualize your productivity with statistics and completion rates
              </p>
            </div>

            <div className="bg-white p-6 sm:p-8 rounded-xl shadow-sm border border-gray-100 text-center">
              <div className="w-12 h-12 rounded-full bg-indigo-100 flex items-center justify-center mx-auto">
                <span className="text-indigo-600 font-bold">🔒</span>
              </div>
              <h3 className="mt-6 text-lg font-semibold text-gray-900">Secure & Private</h3>
              <p className="mt-2 text-gray-600">
                Your data is protected with industry-standard security measures
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;