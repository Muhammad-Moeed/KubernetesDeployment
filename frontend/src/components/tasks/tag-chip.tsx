"use client";

interface TagChipProps {
  tag: string;
  onRemove?: () => void;
}

export function TagChip({ tag, onRemove }: TagChipProps) {
  return (
    <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300">
      {tag}
      {onRemove && (
        <button
          onClick={onRemove}
          className="hover:text-gray-900 dark:hover:text-white"
          aria-label={`Remove ${tag} tag`}
        >
          ×
        </button>
      )}
    </span>
  );
}
