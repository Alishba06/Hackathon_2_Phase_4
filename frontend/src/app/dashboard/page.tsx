'use client';

import React, { useState, useEffect } from 'react';
import { useTheme } from 'next-themes';
import { useAuth } from '@/providers/AuthProvider';
import ProtectedRoute from '@/components/ProtectedRoute';
import { taskApi } from '@/lib/api/endpoints';
import { DashboardProvider } from '@/contexts/DashboardContext';

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

const DashboardPage = () => {
  const { theme } = useTheme();
  const { user } = useAuth();
  
  // State for tasks and statistics
  const [tasks, setTasks] = useState<Task[]>([]);
  const [totalTasks, setTotalTasks] = useState<number>(0);
  const [completedTasks, setCompletedTasks] = useState<number>(0);
  const [pendingTasks, setPendingTasks] = useState<number>(0);
  const [recentActivity, setRecentActivity] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch tasks when component mounts
  useEffect(() => {
    const fetchTasks = async () => {
      try {
        setLoading(true);
        const fetchedTasks = await taskApi.getAllTasks();
        setTasks(fetchedTasks);
        
        // Calculate statistics
        const total = fetchedTasks.length;
        const completed = fetchedTasks.filter((task: Task) => task.is_completed).length;
        const pending = total - completed;
        
        setTotalTasks(total);
        setCompletedTasks(completed);
        setPendingTasks(pending);
        
        // Get recent activities (latest 5 tasks)
        const sortedTasks = [...fetchedTasks].sort((a, b) => 
          new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
        );
        setRecentActivity(sortedTasks.slice(0, 5));
        
        setError(null);
      } catch (err: any) {
        console.error('Error fetching tasks:', err);
        setError('Failed to load dashboard data. Please refresh the page.');
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, []);

  // Refresh tasks when a new task is created (this would be triggered by a custom event or context)
  const refreshTasks = async () => {
    try {
      const fetchedTasks = await taskApi.getAllTasks();
      setTasks(fetchedTasks);
      
      // Recalculate statistics
      const total = fetchedTasks.length;
      const completed = fetchedTasks.filter((task: Task) => task.is_completed).length;
      const pending = total - completed;
      
      setTotalTasks(total);
      setCompletedTasks(completed);
      setPendingTasks(pending);
      
      // Update recent activities
      const sortedTasks = [...fetchedTasks].sort((a, b) => 
        new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      );
      setRecentActivity(sortedTasks.slice(0, 5));
      
      setError(null);
    } catch (err: any) {
      console.error('Error refreshing tasks:', err);
      setError('Failed to refresh dashboard data.');
    }
  };

  return (
    <ProtectedRoute>
      <DashboardProvider onRefreshTasks={refreshTasks}>
        <div className={`min-h-screen ${theme === 'dark' ? 'bg-gray-900 text-white' : 'bg-gray-50 text-gray-900'} transition-colors duration-200`}>
          <div className="container mx-auto px-4 py-8">
            <h1 className="text-3xl font-bold mb-8">Dashboard</h1>

            {user && (
              <div className="mb-6 p-4 bg-blue-50 dark:bg-blue-900/30 rounded-lg">
                <p>Welcome back, <span className="font-semibold">{user.firstName || user.email}</span>!</p>
              </div>
            )}

            {error && (
              <div className="mb-6 p-4 bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-200 rounded-lg">
                {error}
              </div>
            )}

            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              {/* Total Tasks Card */}
              <div className={`${theme === 'dark' ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700`}>
                <h2 className="text-lg font-semibold mb-2 text-gray-500 dark:text-gray-400">Total Tasks</h2>
                <p className="text-3xl font-bold">{loading ? '...' : totalTasks}</p>
              </div>

              {/* Completed Tasks Card */}
              <div className={`${theme === 'dark' ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700`}>
                <h2 className="text-lg font-semibold mb-2 text-green-500">Completed</h2>
                <p className="text-3xl font-bold">{loading ? '...' : completedTasks}</p>
              </div>

              {/* Pending Tasks Card */}
              <div className={`${theme === 'dark' ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700`}>
                <h2 className="text-lg font-semibold mb-2 text-yellow-500">Pending</h2>
                <p className="text-3xl font-bold">{loading ? '...' : pendingTasks}</p>
              </div>
            </div>
          </div>

          {/* Recent Activity Section */}
          <div className={`${theme === 'dark' ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700 mb-8`}>
            <h2 className="text-xl font-semibold mb-4">Recent Activity</h2>
            {loading ? (
              <p className="text-gray-500 dark:text-gray-400">Loading recent activity...</p>
            ) : recentActivity.length > 0 ? (
              <ul className="space-y-3">
                {recentActivity.map((task) => (
                  <li key={task.id} className="border-b border-gray-200 dark:border-gray-700 pb-3 last:border-0 last:pb-0">
                    <div className="flex justify-between items-start">
                      <div>
                        <h3 className="font-medium">{task.title}</h3>
                        <p className="text-sm text-gray-500 dark:text-gray-400">
                          {new Date(task.created_at).toLocaleString()}
                        </p>
                      </div>
                      <span className={`px-2 py-1 rounded text-xs ${
                        task.is_completed 
                          ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-200' 
                          : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-200'
                      }`}>
                        {task.is_completed ? 'Completed' : 'Pending'}
                      </span>
                    </div>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500 dark:text-gray-400">No recent activity to display.</p>
            )}
          </div>

          {/* Quick Stats */}
          <div className={`${theme === 'dark' ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700`}>
            <h2 className="text-xl font-semibold mb-4">Quick Stats</h2>
            <div className="flex flex-wrap gap-4">
              <div className="flex items-center">
                <div className="w-3 h-3 bg-blue-500 rounded-full mr-2"></div>
                <span>Productivity: {totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0}%</span>
              </div>
              <div className="flex items-center">
                <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
                <span>Completion Rate: {totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0}%</span>
              </div>
              <div className="flex items-center">
                <div className="w-3 h-3 bg-purple-500 rounded-full mr-2"></div>
                <span>On-time Delivery: N/A</span>
              </div>
            </div>
          </div>
        </div>
      </DashboardProvider>
    </ProtectedRoute>
  );
};

export default DashboardPage;