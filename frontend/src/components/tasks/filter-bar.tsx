"use client";

import { useI18n } from "@/contexts/i18n-context";

interface FilterBarProps {
  status: "all" | "pending" | "completed";
  priority: string;
  onStatusChange: (status: "all" | "pending" | "completed") => void;
  onPriorityChange: (priority: string) => void;
}

export function FilterBar({
  status,
  priority,
  onStatusChange,
  onPriorityChange,
}: FilterBarProps) {
  const { t } = useI18n();

  return (
    <div className="flex flex-wrap gap-4">
      <div className="flex-1 min-w-[200px]">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          {t("tasks.status.all")}
        </label>
        <select
          value={status}
          onChange={(e) => onStatusChange(e.target.value as "all" | "pending" | "completed")}
          className="w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent dark:bg-gray-800 dark:text-white"
        >
          <option value="all">{t("tasks.status.all")}</option>
          <option value="pending">{t("tasks.status.pending")}</option>
          <option value="completed">{t("tasks.status.completed")}</option>
        </select>
      </div>

      <div className="flex-1 min-w-[200px]">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          {t("tasks.taskPriority")}
        </label>
        <select
          value={priority}
          onChange={(e) => onPriorityChange(e.target.value)}
          className="w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent dark:bg-gray-800 dark:text-white"
        >
          <option value="">{t("tasks.status.all")}</option>
          <option value="high">{t("tasks.priority.high")}</option>
          <option value="medium">{t("tasks.priority.medium")}</option>
          <option value="low">{t("tasks.priority.low")}</option>
        </select>
      </div>
    </div>
  );
}
