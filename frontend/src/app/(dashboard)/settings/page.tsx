"use client";

import { useAuth } from "@/contexts/auth-context";
import { DashboardLayout } from "@/components/layout/dashboard-layout";

export default function SettingsPage() {
  // Auth is globally available through context
  const { user, session, isAuthenticated } = useAuth();
  
  // You can use user.id, session.token, etc. here if needed
  // For example: console.log("Current user:", user?.id);
  
  return (
    <DashboardLayout>
      <div className="max-w-4xl mx-auto">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Settings
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-2">
            Manage your preferences
          </p>
        </div>

        <div className="bg-white dark:bg-gray-900 rounded-lg shadow p-6">
          <div className="space-y-6">
            <div>
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                Appearance
              </h2>
              <p className="text-gray-600 dark:text-gray-400">
                Theme and language settings are available in the header
              </p>
            </div>

            <div>
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                Account
              </h2>
              <p className="text-gray-600 dark:text-gray-400">
                Account settings will be implemented here
              </p>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
