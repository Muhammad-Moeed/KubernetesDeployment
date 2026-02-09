import Header from "@/components/ui/Header";
import Footer from "@/components/ui/Footer";
import { FeatureCard } from "@/components/ui/FeatureCard";
import { Step } from "@/components/ui/Step";
import Link from "next/link";

export default function LandingPage() {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-b from-blue-50 to-white dark:from-gray-900 dark:to-gray-950">
      <Header />

      <main className="flex-1">
        {/* Hero */}
        <section className="container mx-auto px-4 py-24 text-center max-w-5xl">
          <h1 className="text-5xl md:text-6xl font-extrabold text-gray-900 dark:text-white mb-6">
            Work Smarter.
            <br /> Get More Done.
          </h1>

          <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto mb-10">
            Listify helps you organize tasks, focus on priorities, and stay
            productive with powerful features like voice input, multilingual
            support, and intelligent filtering.
          </p>

          <div className="flex justify-center gap-4">
            <Link
              href="/signup"
              className="px-10 py-4 bg-primary text-white rounded-xl text-lg font-semibold hover:bg-primary-700 transition"
            >
              Start Free
            </Link>
            <Link
              href="/login"
              className="px-10 py-4 border border-gray-300 dark:border-gray-700 rounded-xl text-lg font-semibold hover:bg-gray-100 dark:hover:bg-gray-800 transition"
            >
              Sign In
            </Link>
          </div>
        </section>

        {/* Features */}
        <section id="features" className="container mx-auto px-4 py-20">
          <h2 className="text-4xl font-bold text-center mb-12">
            Everything You Need to Stay Organized
          </h2>

          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-4">
            <FeatureCard
              icon="🔐"
              title="Secure by Design"
              description="JWT-based authentication ensures your tasks remain private."
            />
            <FeatureCard
              icon="⚡"
              title="Fast & Responsive"
              description="Optimized UI for instant task creation and updates."
            />
            <FeatureCard
              icon="🌐"
              title="Multilingual"
              description="English & Urdu support with RTL layout handling."
            />
            <FeatureCard
              icon="🎙️"
              title="Voice Powered"
              description="Add tasks using voice commands for maximum efficiency."
            />
          </div>
        </section>

        {/* Workflow */}
        <section id="workflow" className="bg-gray-100 dark:bg-gray-900 py-20">
          <div className="container mx-auto px-4">
            <h2 className="text-4xl font-bold text-center mb-12">
              Simple Workflow
            </h2>

            <div className="grid gap-12 md:grid-cols-3">
              <Step
                number="01"
                title="Sign Up"
                description="Create your account in seconds."
              />
              <Step
                number="02"
                title="Plan Tasks"
                description="Organize and prioritize with smart filters."
              />
              <Step
                number="03"
                title="Execute"
                description="Stay productive and track progress daily."
              />
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}
