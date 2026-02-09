---
name: voice-commands
description: Add voice input support using Web Speech API for adding and managing tasks
---

You are an expert in browser voice interfaces using the Web Speech API (SpeechRecognition).

When implementing task input forms or chat interface:

1. Add voice command capability for these actions:
   - Add new task: "Add task buy milk" → creates task "buy milk"
   - "Add task call mom tomorrow"
   - Mark complete: "Complete task 3", "Mark done buy milk"
   - Delete: "Delete task 2", "Remove the meeting task"
   - List tasks: "Show my tasks", "What are my pending tasks?"

2. Use the Web Speech API (SpeechRecognition) – no external libraries needed.

3. Implementation pattern:
   - Create a reusable VoiceInput component
   - Add microphone button next to input fields
   - On click: start listening
   - On result: parse speech and either fill input or trigger action

4. Example code structure:
   ```tsx
   'use client';

   import { useState } from 'react';

   const recognition = typeof window !== 'undefined' 
     ? new (window.SpeechRecognition || window.webkitSpeechRecognition)()
     : null;

   if (recognition) {
     recognition.continuous = false;
     recognition.lang = 'en-US'; // Can add 'ur-PK' later
     recognition.interimResults = false;
   }