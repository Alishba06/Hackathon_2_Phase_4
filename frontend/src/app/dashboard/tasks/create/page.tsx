'use client';

import React, { useEffect } from 'react';
import { TaskForm } from '../../../../components/TaskForm';
import { useAuth } from '@/providers/AuthProvider';
import { useRouter } from 'next/navigation';

const CreateTaskPage: React.FC = () => {
  const { isAuthenticated, loading } = useAuth();
  const router = useRouter();

  // 🔐 Protect route using AuthContext
  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.push('/sign-in');
    }
  }, [loading, isAuthenticated, router]);

  // ⏳ Prevent render until auth is confirmed
  if (loading || !isAuthenticated) {
    return null;
  }

  const handleTaskCreated = () => {
    // ✅ Proper Next.js redirect
    router.push('/dashboard/tasks');
  };

  return (
    <div className="create-task-page">
      <h1>Create New Task</h1>
      <TaskForm onTaskCreated={handleTaskCreated} />
    </div>
  );
};

export default CreateTaskPage;




// // frontend/src/app/dashboard/tasks/create/page.tsx
// 'use client';

// import React from 'react';
// import { TaskForm } from '../../../../components/TaskForm';
// import { isAuthenticated } from '../../../../services/auth';

// const CreateTaskPage: React.FC = () => {
//   if (!isAuthenticated()) {
//     // Redirect to login if not authenticated
//     if (typeof window !== 'undefined') {
//       window.location.href = '/login';
//     }
//     return null; // Render nothing while redirecting
//   }

//   const handleTaskCreated = () => {
//     // Optionally redirect to the tasks list after creating a task
//     if (typeof window !== 'undefined') {
//       setTimeout(() => {
//         window.location.href = '/dashboard/tasks';
//       }, 1000); // Redirect after 1 second to allow user to see success
//     }
//   };

//   return (
//     <div className="create-task-page">
//       <h1>Create New Task</h1>
//       <TaskForm onTaskCreated={handleTaskCreated} />
//     </div>
//   );
// };

// export default CreateTaskPage;