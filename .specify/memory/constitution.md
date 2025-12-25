<!--
Sync Impact Report:
- Version change: none → 1.0.0
- List of modified principles:
  - Principle 1: Technical Accuracy
  - Principle 2: Hands-on Learning
  - Principle 3: Clear, Structured Teaching
  - Principle 4: Consistent Python/ROS 2 Examples
  - Principle 5: Separation of Concerns
  - Principle 6: MDX-Ready Content
  - Principle 7: Spec-Kit Plus Workflow
  - Principle 8: Defined Tech Stack
  - Principle 9: Standardized Lesson Structure
- Added sections:
  - Constraints
  - Success Criteria
- Removed sections: None
- Templates requiring updates:
  - ✅ .specify/templates/plan-template.md
  - ✅ .specify/templates/spec-template.md
  - ✅ .specify/templates/tasks-template.md
- Follow-up TODOs: None
-->

# Physical AI & Humanoid Robotics — Textbook + RAG Chatbot Constitution

## Core Principles

### I. Technical Accuracy
All content must be technically accurate and reflect the best practices for ROS 2, Gazebo, Unity, NVIDIA Isaac, and VLA systems.

### II. Hands-on Learning
The textbook must prioritize hands-on learning through practical labs and code demonstrations.

### III. Clear, Structured Teaching
Content must be organized logically into Modules, Chapters, and Lessons to facilitate a clear learning path.

### IV. Consistent Python/ROS 2 Examples
All code examples must be written in Python and use ROS 2, ensuring consistency throughout the textbook.

### V. Separation of Concerns
The book's content and the chatbot's logic must remain strictly separate. No chatbot code should be included within the textbook chapters.

### VI. MDX-Ready Content
All output must be in valid MDX format, ready for use with Docusaurus.

### VII. Spec-Kit Plus Workflow
Development must follow the Spec-Kit Plus workflow: Constitution → Spec → Plan → Tasks → Implement.

### VIII. Defined Tech Stack
The RAG system will be built using FastAPI, Neon Postgres, Qdrant Cloud, and OpenAI Agents/ChatKit.

### IX. Standardized Lesson Structure
Each lesson must include learning goals, a clear explanation, code examples, and a hands-on lab.

## Constraints

- The textbook will consist of exactly four modules:
  1.  ROS 2 — Robotic Nervous System
  2.  Gazebo & Unity — Digital Twin
  3.  NVIDIA Isaac — AI-Robot Brain
  4.  VLA — Vision-Language-Action Robotics
- No chatbot code is to be embedded within the textbook chapters.
- All content must be authored in valid MDX for Docusaurus.

## Success Criteria

- A complete textbook is produced, including all specified modules, chapters, and lessons.
- The Docusaurus site builds successfully and is deployable to GitHub Pages.
- The RAG chatbot answers user questions using only the text from the book.
- A student can successfully complete the final humanoid robot capstone project using the knowledge from the book.

## Governance

This Constitution is the single source of truth for project principles and governance. All development activities, reviews, and artifacts must align with it. Amendments require a documented proposal, review, and an approved migration plan. All team members are responsible for upholding these principles.

**Version**: 1.0.0 | **Ratified**: 2025-12-07 | **Last Amended**: 2025-12-07