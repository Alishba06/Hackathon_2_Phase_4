'use client';

/**
 * Chat Page
 * Main page for AI Todo Chatbot
 */

import React from 'react';
import ChatInterface from '@/components/ChatInterface';
import { useAuth } from '@/providers/AuthProvider';
import { useRouter } from 'next/navigation';

export default function ChatPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();

  if (authLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50 dark:bg-gray-900">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600 dark:text-gray-400">Loading...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    router.push('/sign-in');
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-4 md:p-8">
      <div className="max-w-4xl mx-auto h-[calc(100vh-4rem)]">
        <ChatInterface userId={user.id} />
      </div>
    </div>
  );
}
