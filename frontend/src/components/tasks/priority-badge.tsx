"use client";

interface PriorityBadgeProps {
  priority: "high" | "medium" | "low";
}

export function PriorityBadge({ priority }: PriorityBadgeProps) {
  const styles = {
    high: "bg-danger-100 text-danger-700 dark:bg-danger-900/30 dark:text-danger-400",
    medium: "bg-primary-100 text-primary-700 dark:bg-primary-900/30 dark:text-primary-400",
    low: "bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-400",
  };

  const labels = {
    high: "High",
    medium: "Medium",
    low: "Low",
  };

  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${styles[priority]}`}
    >
      {labels[priority]}
    </span>
  );
}
