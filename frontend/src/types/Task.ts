// frontend/src/types/Task.ts

export interface Task {
  id: string;
  title: string;
  completed: boolean;
  createdAt: Date;
  updatedAt: Date;
  description?: string;
  dueDate?: string;
  priority?: 'low' | 'medium' | 'high';
}