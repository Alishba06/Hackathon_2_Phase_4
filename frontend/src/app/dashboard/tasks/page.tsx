'use client';

import React, { useState, useEffect } from 'react';
import TaskList from '../../../components/TaskList';
import { useAuth } from '@/providers/AuthProvider';
import { useRouter } from 'next/navigation';
import ProtectedRoute from '@/components/ProtectedRoute';
import { Task } from '@/types/Task';

const TasksPage: React.FC = () => {
  const { user, loading: authLoading } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all');
  const router = useRouter();

  const handleTaskUpdate = () => {
    // Trigger a refresh - implement actual task fetching logic here
    console.log('Task updated');
  };

  const handleToggle = (id: string) => {
    console.log('Toggle task:', id);
  };

  const handleDelete = (id: string) => {
    console.log('Delete task:', id);
  };

  const handleUpdate = (id: string, title: string) => {
    console.log('Update task:', id, title);
  };

  const handleFilterChange = (newFilter: 'all' | 'active' | 'completed') => {
    setFilter(newFilter);
  };

  if (authLoading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
      </div>
    );
  }

  return (
    <ProtectedRoute>
      <div className="tasks-page">
        <h1>My Tasks</h1>
        <TaskList
          tasks={tasks}
          onToggle={handleToggle}
          onDelete={handleDelete}
          onUpdate={handleUpdate}
          filter={filter}
          onFilterChange={handleFilterChange}
        />
      </div>
    </ProtectedRoute>
  );
};

export default TasksPage;