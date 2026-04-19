/**
 * Chat Service - API client for AI Todo Chatbot
 * Handles communication with the backend chat endpoint
 */

import axios from 'axios';
import { getToken } from '@/lib/auth/tokenUtils';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

export interface ToolCall {
  tool: string;
  input: Record<string, any>;
  output?: Record<string, any>;
}

export interface ChatResponse {
  conversation_id: string;
  response: string;
  tool_calls: ToolCall[];
}

export interface ChatRequest {
  message: string;
  conversation_id?: string;
}

/**
 * Send a message to the AI chatbot
 * @param userId - User ID
 * @param request - Chat request with message and optional conversation_id
 * @returns Chat response with AI reply and tool calls
 */
export async function sendMessage(
  userId: string,
  request: ChatRequest
): Promise<ChatResponse> {
  const token = getToken();

  if (!token) {
    throw new Error('Authentication token not found. Please sign in again.');
  }

  const url = `${API_BASE_URL}/api/${userId}/chat`;

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
  };

  // Add conversation ID to headers if provided
  if (request.conversation_id) {
    headers['X-Conversation-ID'] = request.conversation_id;
  }

  try {
    const response = await axios.post(url, {
      message: request.message,
      conversation_id: request.conversation_id,
    }, { headers });

    return response.data;
  } catch (error: any) {
    if (error.response?.status === 401) {
      throw new Error('Authentication failed. Please sign in again.');
    }
    throw error;
  }
}

/**
 * Get conversation history (optional - for loading previous messages)
 * @param userId - User ID
 * @param conversationId - Conversation ID
 * @returns Array of messages
 */
export async function getConversationHistory(
  userId: string,
  conversationId: string
): Promise<any[]> {
  const token = getToken();

  if (!token) {
    throw new Error('Authentication token not found. Please sign in again.');
  }

  const url = `${API_BASE_URL}/api/${userId}/conversations/${conversationId}/messages`;

  const headers = {
    'Authorization': `Bearer ${token}`,
  };

  try {
    const response = await axios.get(url, { headers });
    return response.data;
  } catch (error: any) {
    if (error.response?.status === 401) {
      throw new Error('Authentication failed. Please sign in again.');
    }
    throw error;
  }
}
