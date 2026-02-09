export default function Footer() {
  return (
    <footer className="border-t border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-950">
      <div className="container mx-auto px-4 py-12 grid gap-8 md:grid-cols-3 text-gray-600 dark:text-gray-400">
        <div>
          <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
            Listify
          </h3>
          <p>
            A modern task management platform designed to help professionals
            plan, prioritize, and execute work efficiently.
          </p>
        </div>

        <div>
          <h4 className="font-semibold text-gray-900 dark:text-white mb-3">
            Product
          </h4>
          <ul className="space-y-2">
            <li>Task Management</li>
            <li>Voice Input</li>
            <li>Multilingual Support</li>
            <li>Advanced Filters</li>
          </ul>
        </div>

        <div>
          <h4 className="font-semibold text-gray-900 dark:text-white mb-3">
            Legal
          </h4>
          <ul className="space-y-2">
            <li>Privacy Policy</li>
            <li>Terms of Service</li>
          </ul>
        </div>
      </div>

      <div className="text-center py-4 text-sm text-gray-500">
        © {new Date().getFullYear()} Muhammad Moeed. All rights reserved.
      </div>
    </footer>
  );
}
