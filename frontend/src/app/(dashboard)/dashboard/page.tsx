"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import { useAuth } from "@/contexts/auth-context";
import { useI18n } from "@/contexts/i18n-context";
import { apiClient } from "@/lib/api-client";
import { Task } from "@/types/task";
import { DashboardLayout } from "@/components/layout/dashboard-layout";

/* ================= Dashboard Page ================= */
export default function DashboardPage() {
  const { user } = useAuth();
  const { t } = useI18n();
  const [tasks, setTasks] = useState<Task[]>([]);
  const loadingRef = useRef(false);

  // ===== Load Tasks =====
  const loadTasks = useCallback(async () => {
    if (!user?.id || loadingRef.current) return;
    loadingRef.current = true;
    try {
      const fetchedTasks = await apiClient.getTasks(user.id, {});
      setTasks(fetchedTasks || []);
    } catch {
      setTasks([]);
    } finally {
      loadingRef.current = false;
    }
  }, [user?.id]);

  useEffect(() => { if (user?.id) loadTasks(); }, [user?.id, loadTasks]);

  // ===== Task Stats =====
  const totalTasks = tasks.length;
  const completedTasks = tasks.filter(t => t.completed).length;
  const incompleteTasks = totalTasks - completedTasks;
  const completionPercent = totalTasks ? Math.round((completedTasks / totalTasks) * 100) : 0;

  // ===== Last 5 Tasks =====
  const lastTasks = tasks.slice(0, 5);

  return (
    <DashboardLayout>
      <div className="max-w-7xl mx-auto space-y-8">

        {/* ===== Welcome Header ===== */}
        <div>
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
            {t("dashboard.title")}
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-400">
            {t("dashboard.welcome")}, {user?.name || user?.email}!
          </p>
        </div>

        {/* ===== Dashboard Stats Cards ===== */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          <DashboardCard title={t("dashboard.totalTasks")} count={totalTasks} color="bg-blue-500" icon="📋" />
          <DashboardCard title={t("dashboard.completedTasks")} count={completedTasks} color="bg-green-500" icon="✅" />
          <DashboardCard title={t("dashboard.incompleteTasks")} count={incompleteTasks} color="bg-red-500" icon="⚠️" />
        </div>

        {/* ===== Task Completion Bar ===== */}
        <div className="bg-white dark:bg-gray-900 p-6 rounded-xl shadow-lg">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            {t("dashboard.taskCompletion")}
          </h3>
          <div className="w-full h-6 bg-gray-200 dark:bg-gray-800 rounded-full overflow-hidden">
            <div
              className="h-6 bg-green-500 transition-all duration-1000 ease-in-out"
              style={{ width: `${completionPercent}%` }}
            />
          </div>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-2 font-medium">
            {completedTasks} / {totalTasks} {t("dashboard.tasksCompleted")} ({completionPercent}%)
          </p>
        </div>

        {/* ===== Recently Added / Updated Tasks ===== */}
        <div className="bg-white dark:bg-gray-900 rounded-xl shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            {t("dashboard.recentlyAdded")}
          </h3>
          {lastTasks.length === 0 ? (
            <p className="text-gray-600 dark:text-gray-400">{t("dashboard.noTasksInDashboard")}</p>
          ) : (
            <ul className="space-y-2">
              {lastTasks.map(task => (
                <li
                  key={task.id}
                  className="flex justify-between items-center p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition"
                >
                  <span className={`${task.completed ? "line-through text-gray-400" : "text-gray-900 dark:text-white"}`}>
                    {task.title}
                  </span>
                  <span className="text-sm text-gray-500 dark:text-gray-400">
                    {task.completed ? "✅ " + t("tasks.status.completed") : "⚠️ " + t("tasks.status.pending")}
                  </span>
                </li>
              ))}
            </ul>
          )}
        </div>

      </div>
    </DashboardLayout>
  );
}

/* ================= Dashboard Card Component ================= */
function DashboardCard({ title, count, color, icon }: { title: string; count: number; color: string; icon: string }) {
  return (
    <div className="flex items-center gap-5 p-6 rounded-2xl shadow-lg transform hover:scale-105 transition bg-white dark:bg-gray-900 h-32">
      <div className={`flex items-center justify-center w-16 h-16 rounded-full text-white text-3xl ${color}`}>
        {icon}
      </div>
      <div className="flex flex-col justify-center">
        <span className="text-sm text-gray-500 dark:text-gray-400">{title}</span>
        <span className="text-3xl font-bold text-gray-900 dark:text-white">{count}</span>
      </div>
    </div>
  );
}
