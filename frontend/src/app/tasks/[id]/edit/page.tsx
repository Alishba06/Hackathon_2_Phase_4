'use client';

import React, { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useAuth } from '@/providers/AuthProvider';
import { taskApi } from '@/lib/api/endpoints';
import TaskForm from '@/components/tasks/TaskForm';
import { Button } from '@/components/ui/Button';
import Link from 'next/link';
import ProtectedRoute from '@/components/ProtectedRoute';

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

export default function EditTaskPage() {
  const { id } = useParams();
  const router = useRouter();
  const { user } = useAuth();

  const [task, setTask] = useState<Task | null>(null);
  const [loadingTask, setLoadingTask] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (user && id) {
      fetchTask();
    }
  }, [user, id]);

  const fetchTask = async () => {
    if (!user || !id) return;

    try {
      setLoadingTask(true);
      const response = await taskApi.getTaskById(id as string);
      setTask(response);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch task');
      console.error('Error fetching task:', err);
    } finally {
      setLoadingTask(false);
    }
  };

  if (loadingTask) {
    return (
      <ProtectedRoute>
        <div className="min-h-screen flex items-center justify-center">
          <p>Loading...</p>
        </div>
      </ProtectedRoute>
    );
  }

  if (error) {
    return (
      <ProtectedRoute>
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <p className="text-red-500">Error: {error}</p>
            <Button onClick={fetchTask} className="mt-4">Retry</Button>
          </div>
        </div>
      </ProtectedRoute>
    );
  }

  if (!task) {
    return (
      <ProtectedRoute>
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <p>Task not found.</p>
            <Link href="/dashboard">
              <Button className="mt-4">Back to Dashboard</Button>
            </Link>
          </div>
        </div>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center mb-8">
            <h1 className="text-3xl font-bold text-gray-900">Edit Task</h1>
            <Link href={`/tasks/${task.id}`}>
              <Button variant="outline">Back to Task</Button>
            </Link>
          </div>

          <div className="bg-white shadow sm:rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <TaskForm
                initialData={{
                  id: task.id,
                  title: task.title,
                  description: task.description,
                  dueDate: task.due_date,
                  priority: task.priority
                }}
                isEditing={true}
              />
            </div>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}