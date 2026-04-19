'use client';

import { Task } from '@/types/Task';
import { TaskItem } from './TaskItem';
import { Button } from '@/components/ui/Button';

interface TaskListProps {
  tasks: Task[];
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
  onUpdate: (id: string, title: string) => void;
  filter: 'all' | 'active' | 'completed';
  onFilterChange: (filter: 'all' | 'active' | 'completed') => void;
}

export const TaskList: React.FC<TaskListProps> = ({
  tasks,
  onToggle,
  onDelete,
  onUpdate,
  filter,
  onFilterChange
}) => {
  const filteredTasks = tasks.filter(task => {
    if (filter === 'active') return !task.completed;
    if (filter === 'completed') return task.completed;
    return true;
  });

  return (
    <div className="overflow-hidden">
      {filteredTasks.length === 0 ? (
        <div className="text-center py-12 px-4">
          <svg
            className="mx-auto h-12 w-12 text-gray-400"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={1.5}
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
            />
          </svg>
          <h3 className="mt-2 text-sm font-medium text-gray-900">No tasks</h3>
          <p className="mt-1 text-sm text-gray-500">Get started by creating a new task.</p>
          <div className="mt-6">
            <Button>Add New Task</Button>
          </div>
        </div>
      ) : (
        <ul className="divide-y divide-gray-200">
          {filteredTasks.map((task) => (
            <li key={task.id}>
              <TaskItem
                task={task}
                onToggle={onToggle}
                onDelete={onDelete}
                onUpdate={onUpdate}
              />
            </li>
          ))}
        </ul>
      )}

      {tasks.length > 0 && (
        <div className="px-6 py-4 bg-gray-50 border-t border-gray-200 flex items-center justify-between">
          <p className="text-sm text-gray-700">
            {tasks.filter(t => !t.completed).length}{' '}
            <span className="hidden sm:inline">tasks</span> remaining
          </p>
          <Button
            variant="outline"
            size="sm"
            onClick={() => {
              const confirmed = window.confirm('Are you sure you want to delete all completed tasks?');
              if (confirmed) {
                tasks.filter(t => t.completed).forEach(t => onDelete(t.id));
              }
            }}
            className="text-sm"
          >
            Clear completed
          </Button>
        </div>
      )}
    </div>
  );
};

export default TaskList;