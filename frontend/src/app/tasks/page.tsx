'use client';

import React, { useState, useEffect } from 'react';
import { useTheme } from 'next-themes';
import { useAuth } from '@/providers/AuthProvider';
import { taskApi } from '@/lib/api/endpoints';
import ProtectedRoute from '@/components/ProtectedRoute';

// Define the Task type
type Task = {
  id: string;
  title: string;
  description?: string;
  is_completed: boolean;
  due_date?: string;
  priority: 'low' | 'medium' | 'high';
  user_id: string;
  created_at: string;
  updated_at: string;
};

const TasksPage = () => {
  const { theme } = useTheme();
  const { user } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (user && user.id) {
      fetchTasks();
    }
  }, [user]);

  const fetchTasks = async () => {
    if (!user) return;

    try {
      setLoading(true);
      const tasksData = await taskApi.getAllTasks();
      setTasks(tasksData || []);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch tasks');
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  // Function to toggle task completion
  const toggleTaskCompletion = async (taskId: string) => {
    if (!user) return;

    try {
      // Toggle the completion status in the UI immediately
      setTasks(prevTasks =>
        prevTasks.map(task =>
          task.id === taskId ? { ...task, is_completed: !task.is_completed } : task
        )
      );

      // Then update on the server
      await taskApi.patchTask(taskId, { is_completed: !tasks.find(t => t.id === taskId)?.is_completed });
      // Note: The server response is handled in the API service
    } catch (err: any) {
      console.error('Error toggling task completion:', err);
      // Revert the UI change if the API call fails
      setTasks(prevTasks =>
        prevTasks.map(task =>
          task.id === taskId ? { ...task, is_completed: !task.is_completed } : task
        )
      );
    }
  };

  // Function to delete a task
  const deleteTaskHandler = async (taskId: string) => {
    if (!user) return;

    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await taskApi.deleteTask(taskId);
        setTasks(prevTasks => prevTasks.filter(task => task.id !== taskId));
      } catch (err: any) {
        console.error('Error deleting task:', err);
        setError(err.message || 'Failed to delete task');
      }
    }
  };

  return (
    <ProtectedRoute>
      <div className={`min-h-screen ${theme === 'dark' ? 'bg-gray-900 text-white' : 'bg-gray-50 text-gray-900'} transition-colors duration-200`}>
        <div className="container mx-auto px-4 py-8">
          <div className="flex justify-between items-center mb-8">
            <h1 className="text-3xl font-bold">Tasks</h1>
            <button
              className={`px-4 py-2 rounded-md font-medium ${
                theme === 'dark'
                  ? 'bg-blue-600 hover:bg-blue-700 text-white'
                  : 'bg-blue-500 hover:bg-blue-600 text-white'
              } transition-colors`}
              onClick={() => window.location.href = '/tasks/new'}
            >
              Add New Task
            </button>
          </div>

          {/* Task List */}
          <div className="space-y-4">
            {loading ? (
              <div className="flex justify-center py-10">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
              </div>
            ) : error ? (
              <div className="text-center py-10">
                <p className="text-red-500">{error}</p>
                <button
                  className={`mt-4 px-4 py-2 rounded-md font-medium ${
                    theme === 'dark'
                      ? 'bg-blue-600 hover:bg-blue-700 text-white'
                      : 'bg-blue-500 hover:bg-blue-600 text-white'
                  } transition-colors`}
                  onClick={fetchTasks}
                >
                  Retry
                </button>
              </div>
            ) : tasks.length === 0 ? (
              <div className={`text-center py-12 rounded-lg ${theme === 'dark' ? 'bg-gray-800' : 'bg-white'} border border-gray-200 dark:border-gray-700`}>
                <p className="text-gray-500 dark:text-gray-400">No tasks found. Add a new task to get started!</p>
              </div>
            ) : (
              tasks.map((task) => (
                <div
                  key={task.id}
                  className={`rounded-lg shadow-md p-6 border ${
                    theme === 'dark'
                      ? 'bg-gray-800 border-gray-700'
                      : 'bg-white border-gray-200'
                  }`}
                >
                  <div className="flex items-start">
                    <input
                      type="checkbox"
                      checked={task.is_completed}
                      onChange={() => toggleTaskCompletion(task.id)}
                      className="mt-1 h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    />
                    <div className="ml-4 flex-1">
                      <div className="flex justify-between">
                        <h3 className={`text-lg font-medium ${task.is_completed ? 'line-through text-gray-500' : ''}`}>
                          {task.title}
                        </h3>
                        <div className="flex space-x-2">
                          <button
                            className={`px-3 py-1 rounded text-sm ${
                              theme === 'dark'
                                ? 'bg-gray-700 hover:bg-gray-600'
                                : 'bg-gray-200 hover:bg-gray-300'
                            }`}
                            onClick={() => window.location.href = `/tasks/${task.id}/edit`}
                          >
                            Edit
                          </button>
                          <button
                            onClick={() => deleteTaskHandler(task.id)}
                            className={`px-3 py-1 rounded text-sm ${
                              theme === 'dark'
                                ? 'bg-red-700 hover:bg-red-600'
                                : 'bg-red-500 hover:bg-red-600 text-white'
                            }`}
                          >
                            Delete
                          </button>
                        </div>
                      </div>
                      {task.description && (
                        <p className={`mt-2 ${task.is_completed ? 'text-gray-500 dark:text-gray-400' : 'text-gray-600 dark:text-gray-300'}`}>
                          {task.description}
                        </p>
                      )}
                      <div className="mt-3 text-sm text-gray-500 dark:text-gray-400 flex flex-wrap gap-4">
                        <span>Created: {new Date(task.created_at).toLocaleDateString()}</span>
                        {task.due_date && <span>Due: {new Date(task.due_date).toLocaleDateString()}</span>}
                        <span className={`px-2 py-1 rounded ${
                          task.priority === 'high' ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100' :
                          task.priority === 'medium' ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100' :
                          'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100'
                        }`}>
                          {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)} Priority
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
};

export default TasksPage;