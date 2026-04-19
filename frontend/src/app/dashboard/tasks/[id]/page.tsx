// frontend/src/app/dashboard/tasks/[id]/page.tsx
'use client';

import React, { useState, useEffect } from 'react';
import TaskDetail from '../../../../components/TaskDetail';
import { getTaskById } from '../../../../services/api';
import { getUserIdFromToken } from '../../../../services/auth';

interface TaskDetailPageProps {
  params: {
    id: string;
  };
}

const TaskDetailPage: React.FC<{ params: { id: string } }> = ({ params }) => {
  const [task, setTask] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const userId = getUserIdFromToken();
  const taskId = params.id;

  useEffect(() => {
    if (!userId) {
      setError('User not authenticated');
      setLoading(false);
      return;
    }

    const fetchTask = async () => {
      try {
        setLoading(true);
        const taskData = await getTaskById(userId, taskId);
        setTask(taskData);
      } catch (err) {
        setError((err as Error).message);
      } finally {
        setLoading(false);
      }
    };

    fetchTask();
  }, [userId, taskId]);

  const handleTaskUpdate = () => {
    // Refresh the task data
    if (userId) {
      getTaskById(userId, taskId)
        .then(setTask)
        .catch(err => setError((err as Error).message));
    }
  };

  if (loading) return <div>Loading task...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!task) return <div>Task not found</div>;

  return (
    <div className="task-detail-page">
      <h1>Task Detail</h1>
      <TaskDetail task={task} onTaskUpdate={handleTaskUpdate} />
    </div>
  );
};

export default TaskDetailPage;