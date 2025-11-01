# Database Schema

This document defines the PostgreSQL database schema for the Crypto Curriculum Platform.

## Entity Relationship Overview

```
                    Cohort
                   /      \
              Student    Instructor
                 │
    ┌────────────┼────────────┬──────────────┐
    │            │            │              │
UserProgress  QuizAttempt  Achievement  ForumPost
    │            │                           │
  Module      Assessment                (replies)
    │
  Lesson

LearningResource → Module

Note: AI Trading Bot configuration (BotConfiguration, TradingStrategy) 
is content-only for Module 17 - no actual bot execution in platform.
```

**Total Tables:** 12 core tables (simplified LMS scope)

## Core Entities

### Users Table
Stores student and teacher accounts.

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    role VARCHAR(20) NOT NULL DEFAULT 'student',  -- 'student', 'teacher', 'admin'
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
```

**Fields:**
- `id` - Unique identifier (UUID)
- `email` - User's email (unique, for login)
- `username` - Display name
- `password_hash` - Bcrypt hashed password
- `role` - User role (student, teacher, admin)
- `is_active` - Account status
- `created_at` - Account creation timestamp
- `updated_at` - Last update timestamp
- `last_login` - Last successful login

---

### Modules Table
Represents curriculum modules (1-17).

```sql
CREATE TABLE modules (
    id INTEGER PRIMARY KEY,  -- Module number (1-17)
    title VARCHAR(200) NOT NULL,
    description TEXT,
    track VARCHAR(50) NOT NULL,  -- 'user', 'power-user', 'developer', 'architect'
    duration_hours DECIMAL(4,2),
    order_index INTEGER NOT NULL,
    is_published BOOLEAN DEFAULT false,
    prerequisites INTEGER[],  -- Array of prerequisite module IDs
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_modules_track ON modules(track);
CREATE INDEX idx_modules_order ON modules(order_index);
```

**Fields:**
- `id` - Module number (1-17)
- `title` - Module title (e.g., "Blockchain Technology")
- `track` - Which curriculum track (user, power-user, developer, architect)
- `duration_hours` - Estimated completion time
- `order_index` - Display order
- `prerequisites` - Array of module IDs that must be completed first

---

### Lessons Table
Individual lessons within modules.

```sql
CREATE TABLE lessons (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    module_id INTEGER NOT NULL REFERENCES modules(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,  -- Markdown content
    lesson_type VARCHAR(50) DEFAULT 'reading',  -- 'reading', 'video', 'interactive', 'coding'
    order_index INTEGER NOT NULL,
    estimated_minutes INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_lessons_module ON lessons(module_id);
CREATE INDEX idx_lessons_order ON lessons(order_index);
```

**Fields:**
- `id` - Unique identifier
- `module_id` - Parent module
- `content` - Lesson content (Markdown format)
- `lesson_type` - Type of lesson
- `order_index` - Order within module

---

### Assessments Table
Quizzes and practical tasks for each module.

```sql
CREATE TABLE assessments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    module_id INTEGER NOT NULL REFERENCES modules(id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    question_type VARCHAR(50) NOT NULL,  -- 'multiple-choice', 'true-false', 'short-answer', 'coding-task'
    options JSONB,  -- For multiple choice: {"A": "...", "B": "...", "C": "...", "D": "..."}
    correct_answer TEXT,
    explanation TEXT,
    points INTEGER DEFAULT 10,
    order_index INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_assessments_module ON assessments(module_id);
CREATE INDEX idx_assessments_type ON assessments(question_type);
```

**Fields:**
- `question_type` - Type of question
- `options` - JSON object for multiple choice options
- `correct_answer` - Correct answer (for auto-grading)
- `explanation` - Why the answer is correct
- `points` - Point value

---

### User Progress Table
Tracks student progress through modules.

```sql
CREATE TABLE user_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    module_id INTEGER NOT NULL REFERENCES modules(id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'not-started',  -- 'not-started', 'in-progress', 'completed'
    progress_percent DECIMAL(5,2) DEFAULT 0.00,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    last_accessed TIMESTAMP,
    time_spent_minutes INTEGER DEFAULT 0,
    
    UNIQUE(user_id, module_id)
);

CREATE INDEX idx_progress_user ON user_progress(user_id);
CREATE INDEX idx_progress_status ON user_progress(status);
```

**Fields:**
- `status` - Current status
- `progress_percent` - Completion percentage (0-100)
- `time_spent_minutes` - Total time spent on module

---

### Quiz Attempts Table
Stores student quiz attempts and scores.

```sql
CREATE TABLE quiz_attempts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    assessment_id UUID NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
    user_answer TEXT,
    is_correct BOOLEAN,
    points_earned INTEGER,
    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    time_spent_seconds INTEGER
);

CREATE INDEX idx_attempts_user ON quiz_attempts(user_id);
CREATE INDEX idx_attempts_assessment ON quiz_attempts(assessment_id);
CREATE INDEX idx_attempts_date ON quiz_attempts(attempted_at);
```

**Fields:**
- `user_answer` - Student's submitted answer
- `is_correct` - Whether answer was correct
- `points_earned` - Points awarded
- `time_spent_seconds` - Time to answer

---

**Note:** Module 17 (AI Trading Bot) is taught as curriculum content only. Students build their bots externally in Cursor/VS Code. No bot execution or storage within the platform.

---

### Cohorts Table
Represents classes or course offerings.

```sql
CREATE TABLE cohorts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    start_date DATE,
    end_date DATE,
    is_active BOOLEAN DEFAULT true,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_cohorts_active ON cohorts(is_active);
CREATE INDEX idx_cohorts_dates ON cohorts(start_date, end_date);
```

**Fields:**
- `name` - Cohort name (e.g., "Fall 2025 - Beginners")
- `start_date` / `end_date` - Course duration
- `is_active` - Whether cohort is currently running
- `created_by` - Admin or instructor who created it

---

### Cohort Members Table
Links students and instructors to cohorts.

```sql
CREATE TABLE cohort_members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cohort_id UUID NOT NULL REFERENCES cohorts(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL,  -- 'student', 'instructor'
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(cohort_id, user_id)
);

CREATE INDEX idx_cohort_members_cohort ON cohort_members(cohort_id);
CREATE INDEX idx_cohort_members_user ON cohort_members(user_id);
```

---

### Forum Posts Table
Discussion forums for each module.

```sql
CREATE TABLE forum_posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    module_id INTEGER REFERENCES modules(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    parent_post_id UUID REFERENCES forum_posts(id) ON DELETE CASCADE,  -- NULL = top-level
    title VARCHAR(200),  -- NULL if reply
    content TEXT NOT NULL,
    is_pinned BOOLEAN DEFAULT false,
    is_solved BOOLEAN DEFAULT false,
    upvotes INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_forum_module ON forum_posts(module_id);
CREATE INDEX idx_forum_user ON forum_posts(user_id);
CREATE INDEX idx_forum_parent ON forum_posts(parent_post_id);
CREATE INDEX idx_forum_pinned ON forum_posts(is_pinned) WHERE is_pinned = true;
```

---

### Forum Votes Table
Track upvotes/downvotes on forum posts.

```sql
CREATE TABLE forum_votes (
    post_id UUID REFERENCES forum_posts(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    vote_type VARCHAR(10),  -- 'upvote', 'downvote'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (post_id, user_id)
);
```

---

### Achievements Table
Defines available badges and achievements.

```sql
CREATE TABLE achievements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    icon VARCHAR(50),
    category VARCHAR(50),  -- 'completion', 'score', 'engagement', 'helper'
    criteria JSONB,  -- Conditions to earn
    points INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT true
);
```

---

### User Achievements Table
Tracks which achievements users have earned.

```sql
CREATE TABLE user_achievements (
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    achievement_id UUID REFERENCES achievements(id) ON DELETE CASCADE,
    earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    progress JSONB,  -- For multi-step achievements
    PRIMARY KEY (user_id, achievement_id)
);

CREATE INDEX idx_user_achievements_user ON user_achievements(user_id);
```

---

### Learning Resources Table
External resources linked to modules.

```sql
CREATE TABLE learning_resources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    module_id INTEGER REFERENCES modules(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    url VARCHAR(500) NOT NULL,
    resource_type VARCHAR(50),  -- 'video', 'article', 'tutorial', 'documentation'
    difficulty VARCHAR(20),  -- 'beginner', 'intermediate', 'advanced'
    upvotes INTEGER DEFAULT 0,
    added_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_resources_module ON learning_resources(module_id);
```

---

## Relationships

### One-to-Many
- `User` → `UserProgress` (one user has many module progress records)
- `User` → `QuizAttempt` (one user has many quiz attempts)
- `User` → `ForumPost` (one user creates many posts)
- `Module` → `Lesson` (one module has many lessons)
- `Module` → `Assessment` (one module has many assessments)
- `Module` → `LearningResource` (one module has many external resources)
- `Module` → `ForumPost` (one module has many discussion posts)
- `Cohort` → `CohortMember` (one cohort has many members)
- `ForumPost` → `ForumPost` (self-referencing for replies)

### Many-to-Many
- `User` ↔ `Module` (through `UserProgress`)
- `User` ↔ `Cohort` (through `CohortMember`)
- `User` ↔ `Achievement` (through `UserAchievement`)

### Simplified from Original Plan
**Removed tables (not needed for LMS):**
- ~~CodeSubmissions~~ - Students code externally
- ~~PeerReviews~~ - Code review done offline
- ~~BotConfigurations~~ - Bots built externally
- ~~TradingStrategies~~ - Not executed in platform

**Final count: 12 tables** (streamlined for content delivery)

---

## Indexes

Performance-critical indexes:
- `users(email)` - Fast login lookups
- `user_progress(user_id)` - Fast progress queries
- `quiz_attempts(user_id, assessment_id)` - Fast score lookups
- `lessons(module_id)` - Fast module content retrieval

---

## Sample Queries

### Get user's completed modules
```sql
SELECT m.* 
FROM modules m
JOIN user_progress up ON m.id = up.module_id
WHERE up.user_id = :user_id 
  AND up.status = 'completed'
ORDER BY m.order_index;
```

### Get module with lessons and assessments
```sql
SELECT 
    m.*,
    json_agg(DISTINCT l.*) as lessons,
    json_agg(DISTINCT a.*) as assessments
FROM modules m
LEFT JOIN lessons l ON m.id = l.module_id
LEFT JOIN assessments a ON m.id = a.module_id
WHERE m.id = :module_id
GROUP BY m.id;
```

### Get user's quiz performance
```sql
SELECT 
    m.title as module,
    COUNT(qa.id) as attempts,
    SUM(CASE WHEN qa.is_correct THEN 1 ELSE 0 END) as correct,
    AVG(CASE WHEN qa.is_correct THEN 100.0 ELSE 0.0 END) as accuracy
FROM quiz_attempts qa
JOIN assessments a ON qa.assessment_id = a.id
JOIN modules m ON a.module_id = m.id
WHERE qa.user_id = :user_id
GROUP BY m.id, m.title
ORDER BY m.id;
```

---

## Migration Strategy

### Initial Setup
1. Create database: `createdb crypto_curriculum`
2. Initialize Alembic: `alembic init alembic`
3. Create initial migration: `alembic revision --autogenerate -m "Initial schema"`
4. Apply migration: `alembic upgrade head`

### Updating Schema
1. Modify models in `app/backend/models/`
2. Generate migration: `alembic revision --autogenerate -m "Description of changes"`
3. Review migration file
4. Apply: `alembic upgrade head`

---

## Data Seeding

After creating tables, seed with:
1. **17 Modules** - From curriculum outline
2. **Lessons** - From curriculum parts 1-4
3. **Assessments** - 10 per module (170 total)
4. **Sample Users** - For testing
5. **Sample Progress** - For UI development

See `scripts/seed-db.py` (to be created)

---

**Last Updated:** 2025-11-01

