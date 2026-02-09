---
name: urdu-support
description: ALWAYS apply Urdu language support and RTL layout in all frontend components
priority: high
---

WHEN IMPLEMENTING ANY FRONTEND COMPONENT OR PAGE:

YOU MUST MAKE ALL TEXT TRANSLATABLE AND SUPPORT URDU.

1. Use a simple dictionary-based i18n system (no external library needed for hackathon).

Create this file: frontend/lib/i18n.ts
```ts
export const translations = {
  en: {
    appTitle: "My Todo App",
    addTask: "Add Task",
    taskTitle: "Task Title",
    description: "Description (optional)",
    myTasks: "My Tasks",
    completed: "Completed",
    pending: "Pending",
    edit: "Edit",
    delete: "Delete",
    markComplete: "Mark as Complete",
    login: "Login",
    signup: "Sign Up",
    welcome: "Welcome",
    noTasks: "No tasks yet. Add one!",
    language: "Language"
  },
  ur: {
    appTitle: "میرا ٹوڈو ایپ",
    addTask: "ٹاسک شامل کریں",
    taskTitle: "ٹاسک کا عنوان",
    description: "تفصیل (اختیاری)",
    myTasks: "میرے ٹاسکس",
    completed: "مکمل شدہ",
    pending: "زیر التواء",
    edit: "ترمیم",
    delete: "حذف کریں",
    markComplete: "مکمل کے طور پر نشان زد کریں",
    login: "لاگن ان",
    signup: "سائن اپ",
    welcome: "خوش آمدید",
    noTasks: "ابھی کوئی ٹاسک نہیں۔ ایک شامل کریں!",
    language: "زبان"
  }
};

export type Lang = 'en' | 'ur';

export const getT = (lang: Lang) => (key: keyof typeof translations.en) => 
  translations[lang][key] || translations.en[key];