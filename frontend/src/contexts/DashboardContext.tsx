'use client';

import React, { createContext, useContext, ReactNode } from 'react';

// Define the context type
interface DashboardContextType {
  refreshTasks: () => void;
}

// Create the context
const DashboardContext = createContext<DashboardContextType | undefined>(undefined);

// Provider component
interface DashboardProviderProps {
  children: ReactNode;
  onRefreshTasks: () => void;
}

export const DashboardProvider: React.FC<DashboardProviderProps> = ({ children, onRefreshTasks }) => {
  return (
    <DashboardContext.Provider value={{ refreshTasks: onRefreshTasks }}>
      {children}
    </DashboardContext.Provider>
  );
};

// Custom hook to use the context
export const useDashboard = (): DashboardContextType => {
  const context = useContext(DashboardContext);
  if (context === undefined) {
    throw new Error('useDashboard must be used within a DashboardProvider');
  }
  return context;
};