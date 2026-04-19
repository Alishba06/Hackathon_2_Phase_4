// frontend/src/components/TaskDetail.tsx
import React from 'react';
import { Task } from '../types/Task';
import { toggleTaskCompletion } from '../services/api';
import { getUserIdFromToken } from '../services/auth';

interface TaskDetailProps {
  task: Task;
  onTaskUpdate: () => void;
}

const TaskDetail: React.FC<TaskDetailProps> = ({ task, onTaskUpdate }) => {
  const userId = getUserIdFromToken();

  const handleToggleCompletion = async () => {
    if (!userId) return;

    try {
      await toggleTaskCompletion(userId, task.id, !task.completed);
      onTaskUpdate(); // Refresh the task
    } catch (error) {
      console.error('Error toggling task completion:', error);
    }
  };

  return (
    <div className={`task-detail ${task.completed ? 'completed' : ''}`}>
      <div className="task-header">
        <h2>
          <input
            type="checkbox"
            checked={task.completed}
            onChange={handleToggleCompletion}
            disabled={!userId}
          />
          {task.title}
        </h2>
      </div>

      <div className="task-body">
        {task.description && (
          <div className="task-description">
            <h3>Description</h3>
            <p>{task.description}</p>
          </div>
        )}

        <div className="task-details">
          <div className="detail-item">
            <strong>Status:</strong> {task.completed ? 'Completed' : 'Pending'}
          </div>

          {task.dueDate && (
            <div className="detail-item">
              <strong>Due Date:</strong> {new Date(task.dueDate).toLocaleDateString()}
            </div>
          )}

          {task.priority && (
            <div className="detail-item">
              <strong>Priority:</strong>
              <span className={`priority ${task.priority}`}>
                {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}
              </span>
            </div>
          )}

          <div className="detail-item">
            <strong>Created:</strong> {new Date(task.createdAt).toLocaleString()}
          </div>

          <div className="detail-item">
            <strong>Last Updated:</strong> {new Date(task.updatedAt).toLocaleString()}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TaskDetail;