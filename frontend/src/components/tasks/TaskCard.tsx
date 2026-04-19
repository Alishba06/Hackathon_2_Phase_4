import React from 'react';
import { taskApi } from '@/lib/api/endpoints';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '../ui/Card';
import { Button } from '../ui/Button';
import { CheckCircleIcon, ClockIcon, ExclamationTriangleIcon } from '@heroicons/react/24/outline';

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

interface TaskCardProps {
  task: Task;
  onUpdate: () => void;
}

export const TaskCard: React.FC<TaskCardProps> = ({ task, onUpdate }) => {
  const handleToggleCompletion = async () => {
    try {
      await taskApi.patchTask(task.id, { is_completed: !task.is_completed });
      onUpdate();
    } catch (error) {
      console.error('Error toggling task completion:', error);
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await taskApi.deleteTask(task.id);
        onUpdate();
      } catch (error) {
        console.error('Error deleting task:', error);
      }
    }
  };

  const formatDate = (dateString?: string) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString();
  };

  const priorityStyles = {
    low: {
      bg: 'bg-green-100 dark:bg-green-900/30',
      text: 'text-green-800 dark:text-green-200',
      icon: 'text-green-500 dark:text-green-400',
      border: 'border-green-200 dark:border-green-800'
    },
    medium: {
      bg: 'bg-yellow-100 dark:bg-yellow-900/30',
      text: 'text-yellow-800 dark:text-yellow-200',
      icon: 'text-yellow-500 dark:text-yellow-400',
      border: 'border-yellow-200 dark:border-yellow-800'
    },
    high: {
      bg: 'bg-red-100 dark:bg-red-900/30',
      text: 'text-red-800 dark:text-red-200',
      icon: 'text-red-500 dark:text-red-400',
      border: 'border-red-200 dark:border-red-800'
    }
  };

  const priorityIcons = {
    low: CheckCircleIcon,
    medium: ClockIcon,
    high: ExclamationTriangleIcon
  };

  const PriorityIcon = priorityIcons[task.priority];
  const priorityStyle = priorityStyles[task.priority];

  return (
    <Card className={`border-0 shadow-lg transition-all duration-200 hover:shadow-xl ${task.is_completed ? 'opacity-70' : ''}`}>
      <CardHeader className={`pb-3 ${priorityStyle.border} border-l-4`}>
        <div className="flex justify-between items-start">
          <div className="flex items-start space-x-2">
            <div className={`mt-0.5 ${priorityStyle.icon}`}>
              <PriorityIcon className="h-5 w-5" />
            </div>
            <CardTitle className={`text-lg ${task.is_completed ? 'line-through text-gray-500 dark:text-gray-400' : 'text-gray-900 dark:text-white'}`}>
              {task.title}
            </CardTitle>
          </div>
          <span className={`text-xs px-2 py-1 rounded-full font-medium ${priorityStyle.bg} ${priorityStyle.text}`}>
            {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}
          </span>
        </div>
      </CardHeader>
      <CardContent className="pb-3">
        {task.description && (
          <p className={`text-sm mb-3 ${task.is_completed ? 'line-through text-gray-500 dark:text-gray-400' : 'text-gray-600 dark:text-gray-300'}`}>
            {task.description}
          </p>
        )}
        {task.due_date && (
          <div className="flex items-center text-xs text-gray-500 dark:text-gray-400">
            <ClockIcon className="h-4 w-4 mr-1" />
            <span>Due: {formatDate(task.due_date)}</span>
          </div>
        )}
      </CardContent>
      <CardFooter className="flex justify-between pt-3 border-t border-gray-200 dark:border-gray-700">
        <Button
          variant={task.is_completed ? 'secondary' : 'outline'}
          size="sm"
          onClick={handleToggleCompletion}
          className={`flex items-center ${task.is_completed ? 'text-green-600 dark:text-green-400' : ''}`}
        >
          {task.is_completed ? (
            <>
              <CheckCircleIcon className="h-4 w-4 mr-1" />
              Completed
            </>
          ) : (
            'Mark Complete'
          )}
        </Button>
        <div className="space-x-2">
          <Button variant="outline" size="sm" asChild>
            <a href={`/tasks/${task.id}`} className="flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
              View
            </a>
          </Button>
          <Button variant="destructive" size="sm" onClick={handleDelete} className="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            Delete
          </Button>
        </div>
      </CardFooter>
    </Card>
  );
};