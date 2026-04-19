'use client';

import React from 'react';
import { useAuth } from '@/providers/AuthProvider';
import TaskForm from '@/components/tasks/TaskForm';
import Link from 'next/link';
import { Button } from '@/components/ui/Button';
import Header from '@/components/ui/Header';
import ProtectedRoute from '@/components/ProtectedRoute';

export default function NewTaskPage() {
  const { user, loading } = useAuth();

  // Show loading state while user data is being fetched
  if (loading || !user) {
    return (
      <ProtectedRoute>
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
          <Header />
          <div className="flex justify-center items-center min-h-[calc(100vh-80px)]">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
          </div>
        </div>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
        <Header />

        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex justify-between items-center mb-8">
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Create New Task</h1>
            <Link href="/dashboard">
              <Button variant="outline">Back to Dashboard</Button>
            </Link>
          </div>

          <div className="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
            <TaskForm />
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}