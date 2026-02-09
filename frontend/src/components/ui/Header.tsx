import Link from "next/link";

export default function Header() {
  return (
    <header className="sticky top-0 z-50 bg-white/80 dark:bg-gray-950/80 backdrop-blur border-b border-gray-200 dark:border-gray-800">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <div className="text-2xl font-extrabold text-primary tracking-tight">
          Listify
        </div>

        <nav className="hidden md:flex gap-8 text-gray-700 dark:text-gray-300 font-medium">
          <Link href="#features" className="hover:text-primary transition">
            Features
          </Link>
          <Link href="#workflow" className="hover:text-primary transition">
            Workflow
          </Link>
          <Link href="#benefits" className="hover:text-primary transition">
            Benefits
          </Link>
        </nav>

        <div className="flex gap-3">
          <Link
            href="/login"
            className="px-4 py-2 border border-primary text-primary rounded-lg font-semibold hover:bg-primary hover:text-white transition"
          >
            Sign In
          </Link>
          <Link
            href="/signup"
            className="px-4 py-2 bg-primary text-white rounded-lg font-semibold hover:bg-primary-700 transition"
          >
            Get Started
          </Link>
        </div>
      </div>
    </header>
  );
}
