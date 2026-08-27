# 🗺️ City Companion — Local Activity Discovery Platform

City Companion is a local activity-discovery platform that helps people find and join plans near them (movies, bowling, gaming, sports, food, outdoor hikes, etc.). It allows users to post their plans, discover activities nearby on an interactive map, request to join groups, and get smart recommendations.

---

## 🏗️ Project Architecture

The application is structured as a modular system designed for local discovery:
1. **Frontend**: Next.js + TypeScript + Tailwind CSS + Leaflet/OpenStreetMap.
2. **Backend**: Python + Django + Django REST Framework (DRF) + PostgreSQL (Neon Database) + `django-filter` for granular query parameters.
3. **AI Service (Planned)**: FastAPI service utilizing `pgvector` inside PostgreSQL for semantic searching, recommendations, auto-moderation, and descriptive assistant helpers.

---

## ⚡ Current Status & Rebuilt API Layer

The backend has been completely rebuilt from scratch as a **clean, decoupled, and standalone REST API layer**. It does not enforce any custom camelCase frontend payloads on the API schema, returning to industry-standard REST practices.

### What is Working Now (Implemented)
- **Database Schema**:
  - `Category` model: Normalized dynamic categories with auto-slug generation.
  - `Event` model: Stores activity details, status tracks (`open`, `full`, `cancelled`, `completed`), coordination coordinates, and handles safe deletion via an `is_active` flag.
- **RESTful Endpoints**:
  - Full CRUD operations for `Category` (`/api/v1/categories/`) and `Event` (`/api/v1/events/`).
  - **Dynamic Pagination**: Standardized page-based response payloads (20 items per page).
  - **Granular Filtering**: Built-in filters via `django-filter` allowing clients to query by category slug (`?category__slug=sports`), status (`?status=open`), exact date (`?date=2026-09-01`), active states, etc.
  - **Fuzzy Search**: Search parameter (`?search=`) queries across event titles, descriptions, and location names.
  - **Custom Actions**: Fully implemented status transitions to cancel (`POST /api/v1/events/{id}/cancel/`) or complete (`POST /api/v1/events/{id}/complete/`) activities, complete with state validation.
- **Data Seeding**:
  - Custom command `python manage.py seed_data` creates dynamic dummy categories and events mapped around coordinates to instantly seed a local or remote PostgreSQL database.
- **Full Test Suite**:
  - 31 unit and integration tests verifying all URL routing, model logic, serializers, paginations, and validation rules.

---

## 🎯 Backlog & To Be Implemented

These features are planned to be implemented as the modular backend monolith matures:
- [ ] **Authentication & User Profiles**:
  - User model implementation.
  - Authentication flow utilizing secure JWT tokens (access and refresh token rotations).
- [ ] **Social Workflows & Joining Logic**:
  - Join request state machine (Requested, Approved, Denied).
  - Real-time attendee listing and tracking of spots left based on capacity bounds.
- [ ] **PostGIS Spatial Queries**:
  - Integrate PostGIS coordinates.
  - Query events within a specific radius based on current geographical location.
- [ ] **Realtime Updates**:
  - WebSockets (using Django Channels) for instant notification push and join-request approvals.
- [ ] **Python FastAPI AI Service**:
  - Semantic searching using `pgvector` to find events based on freeform descriptions (e.g. "somewhere dry and fun to go tonight").
  - Content-based compatibility ranking and recommendation scores.
  - Automated spam/scam moderation logic.

---

## 📸 Screenshots

*Below is a placeholder section for frontend screens, backend DRF browsable API views, and terminal testing logs:*

### Django REST Framework Browsable API
![Browsable API Placeholder](https://raw.githubusercontent.com/django/django/main/docs/_static/logo.png)
*(Run your local server and navigate to `http://localhost:8000/api/v1/` to interact with the API directly in your browser)*

### Next.js Interactive Map Interface
*(Add your map and event-browsing screenshots here)*

---

## 🛠️ Local Development & Setup

### Backend (Django)

1. **Navigate to backend and set up environment**:
   ```bash
   cd backend
   # Ensure you have your .env file configured with DATABASE_URL
   ```

2. **Activate Virtual Environment**:
   ```bash
   # On Windows PowerShell
   .\venv\Scripts\Activate.ps1
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Seed the Database**:
   ```bash
   # Add sample events and categories
   python manage.py seed_data
   
   # Or reset existing database and re-seed
   python manage.py seed_data --clear
   ```

6. **Run Test Suite**:
   ```bash
   python manage.py test events -v 2
   ```

7. **Start Server**:
   ```bash
   python manage.py runserver
   ```

### Frontend (Next.js)

1. **Navigate to frontend**:
   ```bash
   cd lessgo
   ```

2. **Install Packages & Run dev server**:
   ```bash
   npm install
   npm run dev
   ```
