# CareerAI — End-to-End System Workflow Architecture (`workflow.md`)

This document provides a detailed breakdown of how the **CareerAI** platform functions from end to end, covering the student user journey, technical component architecture, data flow cycles, scoring algorithms, and resilient offline-first fallbacks.

---

## 1. High-Level Architectural Flowchart

```text
+-----------------------------------------------------------------------------------+
|                                STUDENT TOUCHPOINTS                                |
+-----------------------------------------------------------------------------------+
  |                                 |                                 |
  v                                 v                                 v
[ Landing Page (/) ]       [ University Auth (/login) ]     [ Floating CareerBot ]
  |                          • USN Validation                 • Quick Suggestion Pills
  |                          • Google Workspace SSO           • Instant NLP Replies
  +---------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------------------+
|                           CORE APPLICATION DASHBOARD (/dashboard)                |
+-----------------------------------------------------------------------------------+
  • Holistic Placement Readiness Score (e.g. 84%)
  • Semester-wise CGPA & CIE Internal Score Visualizer (Recharts)
  • Top AI-Matched Career Track & Active Application Tracker
  |
  +----------> [ 🧭 AI Career Matching (/career) ]
  |              • Role Fit Benchmarking (React, Node, Cloud, System Design)
  |              • Market CTC & Tier-1/Tier-2 Recruiter Radar
  |
  +----------> [ ⚡ Skill Gap Diagnostics (/skills) ]
  |              • Current vs. Required Competency Radar
  |              • Critical Gap Prioritization & Curated Course Recommendations
  |
  +----------> [ 🗺️ Milestone Learning Roadmap (/roadmap) ]
  |              • Phased Execution Plan (Foundations -> Frontend -> Backend -> DevOps)
  |              • Interactive Task Checklists with Auto-Recalculating Progress
  |
  +----------> [ 💼 Opportunities & Applications (/jobs & /applications) ]
  |              • Full-Time & Internship Listings with Match Percentages
  |              • One-Click Application Pipeline with Real-Time Status Tracking
  |
  +----------> [ 🤖 AI Placement Mentor (/chatbot) ]
  |              • Deep Conversational Interview Prep & Resume Suggestions
  |
  v
+-----------------------------------------------------------------------------------+
|                        CENTRALIZED DATA & RESILIENCE LAYER                        |
+-----------------------------------------------------------------------------------+
  |                                                                   |
  v (Primary Path)                                                    v (Fault-Tolerant Fallback)
[ Axios HTTP Client (`/src/services/*`) ]                 [ Curated Academic Cache (`data.js`) ]
  • Timeout: 10,000ms                                       • Instant Fallback if Backend Offline
  • BaseURL: `VITE_API_BASE_URL`                            • Full Student Profile, Jobs & Roadmaps
  • JSON Headers & Token Injection
  |
  v
[ Production REST API / Backend Services ]
```

---

## 2. Step-by-Step Student User Journey

The CareerAI experience follows a structured, outcome-driven progression:

```
 ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
 │ 1. Onboarding   │ ───> │ 2. Diagnostics  │ ───> │ 3. Skill Gap    │
 │    & Auth       │      │    & Baseline   │      │    Discovery    │
 └─────────────────┘      └─────────────────┘      └─────────────────┘
           │                                                │
           v                                                v
 ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
 │ 6. Placement    │ <─── │ 5. Applications │ <─── │ 4. Roadmap      │
 │    Achievement  │      │    & Interviews │      │    Execution    │
 └─────────────────┘      └─────────────────┘      └─────────────────┘
```

### Stage 1: Onboarding & Authentication
1. **Entry**: The student visits the platform at `/` or `/login`.
2. **Identification**:
   - The student enters their **University Seat Number (USN)** (e.g., `1EP24CS001`) and college credentials, or logs in using institutional **Google Workspace SSO**.
   - The portal verifies university standing, active semester, and academic branch.
3. **Session Activation**: The user is routed to the authenticated application layout at `/dashboard`.

### Stage 2: Diagnostic Baseline & Dashboard Overview
1. **Aggregated Readiness Ingestion**: The system pulls academic metrics (CGPA, active backlogs, internal CIE tests) and verified technical skills.
2. **Readiness Computation**: The platform computes an aggregate **Placement Readiness Score** (e.g., 84%) using weighted scoring across academic consistency, core CS fundamentals, and project depth.
3. **Executive Dashboard**:
   - Displays real-time radial progress charts.
   - Highlights the highest-matching career track (e.g., *Full Stack Developer - 92% Match*).
   - Surfaces urgent skill deficiencies requiring immediate remediation.

### Stage 3: Skill Gap Analysis & Role Targeting
1. The student navigates to `/skills` or selects a recommended role from `/career`.
2. **Target Benchmark Comparison**:
   - The system contrasts the student's current proficiency ratings against real-time industry recruiter thresholds.
   - *Example*: Student Node.js proficiency is at `60%`, while entry-level SDE requirements demand `85%`.
3. **Prioritized Action Plan**: Skill gaps are tagged by urgency (`Critical`, `Moderate`, `Good`), paired with estimated study durations (e.g., *3 weeks*), and linked to vetted learning resources.

### Stage 4: Roadmap Execution & Milestones
1. The student navigates to `/roadmap`.
2. **Phase Traversal**:
   - **Phase 1: Foundations & CS Core** (Data Structures, Algorithms, OS, Networks).
   - **Phase 2: Frontend Specialization** (Modern React, TypeScript, Component Systems).
   - **Phase 3: Backend & APIs** (Express, REST APIs, Microservices, PostgreSQL).
   - **Phase 4: Cloud & Deployment** (Docker, CI/CD, AWS, System Design).
3. **Interactive Milestone Check**:
   - As students complete tutorials, projects, or assessments, they check off milestone tasks.
   - The UI automatically recalculates phase completion and refreshes the student's global readiness score.

### Stage 5: Opportunity Discovery & Application Submission
1. The student visits `/jobs`.
2. **Algorithmic Role Filtering**:
   - Jobs and internships display an instant match percentage based on the student's verified skills.
   - Roles with high compatibility (>85%) are prioritized.
3. **One-Click Application**:
   - The student applies directly with their pre-loaded profile, GitHub links, and verified resume.
   - The application moves to `/applications` where stages (`Applied` -> `Shortlisted` -> `Interview Scheduled`) are tracked in real-time.

### Stage 6: AI Mentorship & Continuous Preparation
1. Throughout the cycle, the student interacts with **CareerBot** (`/chatbot` or floating widget).
2. The AI assistant provides:
   - Technical interview mock questions for specific companies (e.g., Amazon, Swiggy, Cred).
   - Resume critique and keyword optimization advice.
   - Targeted preparation schedules for upcoming campus drives.

---

## 3. Frontend Architecture & Component Workflow

```text
                 [ main.tsx ]
                      |
                 [ App.tsx ]
                      |
        [ SearchProvider (Context API) ]
                      |
               [ AppRoutes.jsx ]
             /                   \
   (Public Unwrapped)      (Authenticated Layout)
          |                           |
  ┌───────┴────────┐          [ Layout.jsx ]
  │                │          ├── Top Navbar (Global Search, Notifications)
[ / ]          [ /login ]     ├── Navigation Slider / Sidebar
                              └── <Outlet /> Page Components
                                       ├── /dashboard
                                       ├── /career
                                       ├── /skills
                                       ├── /roadmap
                                       ├── /jobs
                                       ├── /applications
                                       ├── /chatbot
                                       ├── /profile
                                       └── /settings
```

### Key Components & Responsibilities
| Component / Layer | Location | Function |
| :--- | :--- | :--- |
| **`SearchContext`** | `/src/context/SearchContext.jsx` | Supplies real-time search term state across Navbar, Suggestions, and Feature Pages. |
| **`TopNavbar`** | `/src/components/layout/Navbar.jsx` | Holds global branding, active search input with instant autocomplete suggestions, and quick actions. |
| **`Sidebar`** | `/src/components/layout/Sidebar.jsx` | Provides clean, icon-driven routing with active-link indicators and hidden scrollbars. |
| **`Layout`** | `/src/components/layout/Layout.jsx` | Responsive flex wrapper managing container widths, smooth margins, and child route outlets. |
| **`CareerBotWidget`** | `/src/features/landing/pages/LandingPage.jsx` | Floating interactive AI bot on the landing page with pre-set suggestion pills and conversational responses. |

---

## 4. Data Flow & Service Integration Cycle

Every data request in CareerAI follows a predictable, resilient 4-stage lifecycle:

```
[ UI Component (e.g. DashboardPage) ]
        |
        | 1. Dispatches hook / API call (e.g., getDashboard())
        v
[ Feature Service (e.g., dashboardApi.js) ]
        |
        | 2. Initiates Axios GET request via api.js instance
        v
[ Axios Client (api.js) ]
        |
    ┌───┴───────────────────────────────┐
    | (Backend Available)               | (Network Timeout or Error)
    v                                   v
[ Remote Server: /api/dashboard ]    [ CATCH Block Triggered ]
    |                                   |
    | 3a. Returns HTTP 200 JSON         | 3b. Loads Fallback Dataset (`data.js`)
    \───────────────────┬───────────────/
                        |
                        v
        [ 4. State Update (`setData(res)`) ]
                        |
                        v
     [ UI Re-renders with Fresh Analytics & Charts ]
```

### Why This Workflow Matters:
- **Zero Breakage Guarantee**: Even if the backend server is temporarily down, in development mode, or experiencing network latency, the student experience is never disrupted.
- **Unified Schema**: Both the live backend responses and the local data cache adhere to the exact same TypeScript/JavaScript schema specifications documented in `axios.md`.

---

## 5. Core Algorithms & Calculation Workflows

### 5.1 Placement Readiness Score Calculation
The student's holistic readiness rating (0–100%) is calculated using a multi-factor formula:

$$\text{Readiness} = (\text{Academic Score} \times 0.25) + (\text{Verified Skill Ratio} \times 0.40) + (\text{Roadmap Progress} \times 0.25) + (\text{Portfolio Factor} \times 0.10)$$

Where:
- **Academic Score**: Derived from normalized CGPA ($\frac{\text{CGPA}}{10} \times 100$) minus backlog penalties.
- **Verified Skill Ratio**: Percentage of skills evaluated at or above `Target Level` (Advanced / Intermediate).
- **Roadmap Progress**: Aggregate percentage of milestone checklist items marked as completed.
- **Portfolio Factor**: Assessment of uploaded resume, live portfolio URL (`arjunreddy.dev`), and verified GitHub repositories.

### 5.2 Role Matching Engine
When evaluating a student against a career profile or job listing:
1. **Required Skills Extraction**: The system retrieves the list of mandatory and optional skills for the target role.
2. **Proficiency Comparison**: Each matching skill in the student's profile is weighted by proficiency (e.g., React.js at 90% contributes full match weight; Node.js at 60% provides proportional partial weight).
3. **Missing Skill Penalty**: Any critical missing skill reduces the overall role match percentage by a calibrated factor.
4. **Final Match Badge**:
   - $\ge 90\%$: `Top Match` (Green pill)
   - $75\% - 89\%$: `High Match` (Teal pill)
   - $< 75\%$: `Skill Gap Alert` (Amber pill)

### 5.3 Roadmap Phase Progress Update Workflow
1. User clicks the task checkbox for a milestone in `/roadmap`.
2. Component triggers `updateTaskStatus(phaseId, taskId, isCompleted)`.
3. The service issues a `PATCH /api/roadmap/phase/:phaseId/task/:taskId`.
4. The local phase state updates the task boolean flag.
5. The phase progress percentage recalculates dynamically:
   $$\text{Phase Progress} = \left( \frac{\text{Completed Tasks in Phase}}{\text{Total Tasks in Phase}} \right) \times 100$$
6. The global roadmap completion status re-syncs across the entire dashboard.

---

## 6. Real-Time Search & Discovery Workflow

CareerAI incorporates an instantaneous multi-domain search pipeline:

```
[ User types in Search Bar (e.g. "React") ]
                     |
                     v
   [ SearchContext receives query update ]
                     |
                     v
[ Autocomplete Engine parses 4 parallel domains ]:
  ├── 1. Career Roles: Matches "Full Stack Developer", "Frontend Engineer"
  ├── 2. Verified Skills: Matches "React.js", "Redux", "React Native"
  ├── 3. Roadmap Modules: Matches "Phase 2: Frontend Specialization"
  └── 4. Active Postings: Matches "Frontend Intern at InnoVibe"
                     |
                     v
  [ Dropdown modal renders grouped suggestions with direct jump links ]
                     |
                     v
  [ User selects suggestion -> App navigates to specific feature with highlight ]
```

---

## 7. Operational Scenarios & Lifecycle Walkthroughs

### Scenario A: Remedying a Critical Skill Gap
1. **Discovery**: On the dashboard, the student sees a notification: *"Node.js & Express: 25% below recruiter requirements"*.
2. **Detail View**: Student clicks on the gap and is taken to `/skills`, where the gap is classified as `Critical` with an estimated 3-week learning runway.
3. **Resource Access**: Student clicks on the recommended course (*"Node.js Microservices Masterclass"*).
4. **Action in Roadmap**: Student switches to `/roadmap` (Phase 3: Backend & APIs) to review the exact hands-on milestone tasks needed.
5. **Validation**: Once completed, the student's verified score climbs from 60% to 85%, and their role match for *Full Stack Developer* rises from 92% to 97%.

### Scenario B: Applying to a Summer Internship
1. **Discovery**: Placement cell broadcasts a new opening for *Frontend Engineering Intern at InnoVibe Technologies* (₹35,000/mo).
2. **Match Verification**: The jobs engine computes a **94% Match** for the student's profile.
3. **Submission**: Student clicks **"Apply Now"**; the system packages student CGPA (8.4), verified GitHub, portfolio link (`https://arjunreddy.dev`), and resume.
4. **Pipeline Tracking**: The opportunity appears in `/applications` with status set to `Applied`.
5. **Status Update**: When shortlisted, the status badge transitions to `Shortlisted`, and a calendar card displays: *"Technical Interview Scheduled for Sep 5, 2026"*.

---

## 8. Summary of Benefits

- **Clear Student Direction**: Eliminates guesswork by providing concrete, measurable steps toward placement readiness.
- **Institutional Scale**: Suitable for university placement cells to track batch-wide student progress and recruitment stats.
- **Architectural Resilience**: Modern, decoupled React 19 architecture with persistent offline data fallbacks and modular Axios services.
- **Frictionless UI/UX**: Designed with Tailwind CSS v4, smooth animations, hidden scrollbars, and high-contrast typography for effortless navigation.
