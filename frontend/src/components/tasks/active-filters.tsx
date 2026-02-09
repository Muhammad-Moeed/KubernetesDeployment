"use client";

interface ActiveFiltersProps {
  filters: {
    status?: string;
    priority?: string;
    search?: string;
  };
  onClearFilter: (key: string) => void;
  onClearAll: () => void;
}

export function ActiveFilters({
  filters,
  onClearFilter,
  onClearAll,
}: ActiveFiltersProps) {
  const activeFilters = Object.entries(filters).filter(
    ([_, value]) => value && value !== "all"
  );

  if (activeFilters.length === 0) {
    return null;
  }

  return (
    <div className="flex flex-wrap items-center gap-2">
      <span className="text-sm text-gray-600 dark:text-gray-400">
        Active filters:
      </span>
      {activeFilters.map(([key, value]) => (
        <span
          key={key}
          className="inline-flex items-center gap-1 px-3 py-1 bg-primary-100 text-primary-700 dark:bg-primary-900/30 dark:text-primary-400 rounded-full text-sm"
        >
          <span className="font-medium capitalize">{key}:</span>
          <span>{value}</span>
          <button
            onClick={() => onClearFilter(key)}
            className="ml-1 hover:text-primary-900 dark:hover:text-primary-200"
            aria-label={`Remove ${key} filter`}
          >
            ×
          </button>
        </span>
      ))}
      <button
        onClick={onClearAll}
        className="text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 underline"
      >
        Clear all
      </button>
    </div>
  );
}
