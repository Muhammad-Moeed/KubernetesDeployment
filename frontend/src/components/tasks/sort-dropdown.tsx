"use client";

interface SortDropdownProps {
  sortBy: "created_at" | "due_date" | "priority";
  order: "asc" | "desc";
  onSortChange: (sortBy: "created_at" | "due_date" | "priority") => void;
  onOrderChange: (order: "asc" | "desc") => void;
}

export function SortDropdown({
  sortBy,
  order,
  onSortChange,
  onOrderChange,
}: SortDropdownProps) {
  return (
    <div className="flex gap-2">
      <div className="flex-1">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          Sort By
        </label>
        <select
          value={sortBy}
          onChange={(e) => onSortChange(e.target.value as "created_at" | "due_date" | "priority")}
          className="w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent dark:bg-gray-800 dark:text-white"
        >
          <option value="created_at">Created Date</option>
          <option value="due_date">Due Date</option>
          <option value="priority">Priority</option>
        </select>
      </div>

      <div className="flex-1">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          Order
        </label>
        <select
          value={order}
          onChange={(e) => onOrderChange(e.target.value as "asc" | "desc")}
          className="w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent dark:bg-gray-800 dark:text-white"
        >
          <option value="desc">Newest First</option>
          <option value="asc">Oldest First</option>
        </select>
      </div>
    </div>
  );
}
