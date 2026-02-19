# Specification: Personal Memo Web Application

## Metadata
- **Version**: 1.0.0
- **Status**: Draft
- **Author**: Spec-Write Agent
- **Created**: 2026-02-16
- **Last Updated**: 2026-02-16

## Overview

Personal Memo Web Application is a single-user note-taking web application designed for personal memo/note management with full Markdown support. The application follows a modern architecture with React frontend and Express backend, utilizing SQLite for data persistence and Docker for self-hosted deployment on VPS.

The application emphasizes simplicity, security, and user experience with features including WYSIWYG Markdown editing, dark mode support, responsive design, and session-based authentication.

### Core Principles
- **Simplicity**: Single-user focus, no unnecessary complexity
- **Security**: Password hashing, httpOnly cookies, CSRF protection
- **Performance**: Fast page loads (< 2s) and API responses (< 500ms)
- **Accessibility**: WCAG 2.1 AA compliance
- **Self-hosted**: Docker deployment for full control

## Requirements

### Functional Requirements

#### Authentication
- **FR-1**: User can log in with a password (single-user system)
- **FR-2**: User can log out and terminate the session
- **FR-3**: User can change their password
- **FR-4**: Session persists for 7 days with httpOnly cookie
- **FR-5**: System validates authentication on all protected routes

#### Session Storage Note
For single-user simplicity, sessions are stored in memory using a Map structure. This is sufficient for a personal application. Session tokens are random 32-byte hex strings with 7-day expiration.

#### Memo Management
- **FR-6**: User can create a new memo with title and Markdown content
- **FR-7**: User can edit an existing memo (title and content)
- **FR-8**: User can delete a memo with confirmation dialog
- **FR-9**: User can view a list of all memos sorted by update time (newest first)
- **FR-10**: User can view a single memo with rendered Markdown

#### Markdown Support
- **FR-11**: System provides WYSIWYG Markdown editing with Milkdown editor
- **FR-12**: System renders Markdown content with GitHub Flavored Markdown support
- **FR-13**: System sanitizes Markdown content to prevent XSS attacks

#### User Interface
- **FR-14**: System supports dark mode toggle between light and dark themes
- **FR-15**: System persists theme preference to localStorage
- **FR-16**: System defaults to system preference for initial theme
- **FR-17**: System prevents flash of unstyled content (FOUC) on page load
- **FR-18**: System supports responsive layouts for mobile, tablet, and desktop

### Non-functional Requirements

#### Performance
- **NFR-1**: Page load time < 2 seconds on 3G connection
- **NFR-2**: API response time < 500ms for all endpoints
- **NFR-3**: Frontend bundle size optimized for fast initial load

#### Security
- **NFR-4**: Passwords hashed with bcrypt (cost factor >= 10)
- **NFR-5**: Session tokens stored in httpOnly cookies
- **NFR-6**: CSRF protection via sameSite cookie attribute
- **NFR-7**: Security headers via Helmet middleware
- **NFR-8**: Rate limiting on login endpoint (max 5 attempts per minute)
- **NFR-9**: Input validation on all API endpoints
- **NFR-10**: XSS prevention in Markdown rendering

#### Accessibility
- **NFR-11**: WCAG 2.1 AA compliance
- **NFR-12**: Keyboard navigation support
- **NFR-13**: Screen reader compatibility
- **NFR-14**: Color contrast ratio >= 4.5:1

#### Mobile Support
- **NFR-15**: Works on screens 320px and above
- **NFR-16**: Touch-friendly interface elements

#### Maintainability
- **NFR-17**: TypeScript for type safety
- **NFR-18**: Test coverage: Backend 85%+, Frontend 80%+
- **NFR-19**: E2E tests covering 100% of critical user flows

## Architecture

### Technology Stack

#### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Routing**: React Router v6
- **Styling**: Tailwind CSS with `darkMode: 'class'` strategy
- **State Management**: Zustand
- **Markdown Editor**: Milkdown (WYSIWYG)
- **Markdown Rendering**: react-markdown with remark-gfm
- **HTTP Client**: fetch with wrapper
- **Testing**: Vitest + React Testing Library + MSW

#### Backend
- **Runtime**: Node.js 20+
- **Framework**: Express with TypeScript
- **Database**: SQLite with Prisma ORM
- **Authentication**: Session-based with httpOnly cookies (in-memory for single user)
- **Password Hashing**: bcrypt
- **Rate Limiting**: express-rate-limit
- **Validation**: zod
- **Testing**: Jest + Supertest

#### Deployment
- **Containers**: Docker Compose (frontend + backend)
- **Reverse Proxy**: Nginx
- **Data Persistence**: Volume mount for SQLite database

### Initial Setup

#### Generate Password Hash
Before deployment, generate a password hash for the admin user:

```bash
# Using Node.js
node -e "const bcrypt = require('bcryptjs'); console.log(bcrypt.hashSync('your-password', 10));"

# Or using ts-node in the server directory
npx ts-node -e "import bcrypt from 'bcryptjs'; console.log(bcrypt.hashSync('your-password', 10));"
```

Add the generated hash to your `.env` file:
```
ADMIN_PASSWORD_HASH=$2a$10$...generated-hash-here...
```

### Project Structure
```
memo-app/
├── client/                    # Frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── hooks/            # Custom hooks
│   │   ├── store/            # Zustand stores
│   │   ├── utils/            # Utility functions
│   │   ├── types/            # TypeScript types
│   │   ├── mocks/            # MSW handlers
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── public/
│   ├── tests/                # Playwright E2E tests
│   ├── package.json
│   └── vite.config.ts
├── server/                    # Backend
│   ├── src/
│   │   ├── routes/           # API routes
│   │   ├── middleware/       # Express middleware
│   │   ├── db/               # Prisma client
│   │   ├── utils/            # Utilities
│   │   ├── types/            # TypeScript types
│   │   ├── app.ts
│   │   └── index.ts
│   ├── prisma/
│   │   └── schema.prisma
│   ├── tests/                # Jest tests
│   ├── package.json
│   └── tsconfig.json
├── data/                      # SQLite database (volume mount)
├── docker-compose.yml
├── docker-compose.prod.yml
└── README.md
```

### Database Schema
```prisma
model Note {
  id        String   @id @default(uuid())
  title     String
  content   String   @default("")
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}
```

### API Endpoints

| Method | Endpoint                  | Description           | Auth Required |
|--------|---------------------------|-----------------------|---------------|
| POST   | /api/auth/login           | Login with password   | No            |
| POST   | /api/auth/logout          | Logout                | Yes           |
| POST   | /api/auth/change-password | Change password       | Yes           |
| GET    | /api/notes                | Get all notes         | Yes           |
| GET    | /api/notes/:id            | Get single note       | Yes           |
| POST   | /api/notes                | Create note           | Yes           |
| PUT    | /api/notes/:id            | Update note           | Yes           |
| DELETE | /api/notes/:id            | Delete note           | Yes           |

### User Interface Design

#### Pages
1. **Login Page** - Simple password form with error feedback
2. **Notes List Page** - Grid/list view of all notes sorted by update time
3. **Note Editor Page** - Split view: WYSIWYG editor + Markdown preview
4. **Settings Page** - Change password functionality

#### Components
- **NoteCard** - Preview card in list view showing title and content snippet
- **NoteEditor** - Milkdown editor with formatting toolbar
- **NotePreview** - Markdown rendered preview pane
- **ThemeToggle** - Sun/moon toggle button in header
- **ConfirmDialog** - Modal dialog for delete confirmation
- **LoadingSpinner** - Loading state indicator
- **Toast** - Success/error notification system

#### Responsive Breakpoints
- **Mobile**: < 640px (single column, hamburger menu)
- **Tablet**: 640px - 1024px (two columns)
- **Desktop**: > 1024px (three columns)

## Test Steps

### Testing Strategy

The project follows Test-Driven Development (TDD) with a testing pyramid approach:
- **Unit Tests (70%)**: Vitest (frontend) + Jest (backend)
- **Integration Tests (20%)**: Supertest (API) + MSW (frontend)
- **E2E Tests (10%)**: Playwright

### Backend Test Steps

#### Unit Tests
```bash
# Run backend unit tests
cd server
npm test

# Run with coverage
npm run test:coverage
```

**Test Categories:**
1. Auth middleware tests
   - Valid session token validation
   - Expired session token rejection
   - Missing token rejection

2. Validation utilities tests
   - Note title validation
   - Note content validation
   - Password strength validation

3. Error handling tests
   - Database error handling
   - Invalid input handling
   - Authentication failure handling

#### Integration Tests
```bash
# Run backend integration tests
cd server
npm run test:integration
```

**Test Categories:**
1. Notes API tests
   - GET /api/notes - Retrieve all notes
   - GET /api/notes/:id - Retrieve single note
   - POST /api/notes - Create new note
   - PUT /api/notes/:id - Update existing note
   - DELETE /api/notes/:id - Delete note

2. Auth API tests
   - POST /api/auth/login - Successful login
   - POST /api/auth/login - Failed login with wrong password
   - POST /api/auth/logout - Successful logout
   - POST /api/auth/change-password - Password change

3. Database operations tests
   - Prisma CRUD operations
   - Database connection handling
   - Transaction handling

### Frontend Test Steps

#### Unit Tests
```bash
# Run frontend unit tests
cd client
npm test

# Run with coverage
npm run test:coverage
```

**Test Categories:**
1. Custom hooks tests
   - useDarkMode hook - toggle, persist, system preference

2. Store tests
   - Note store (Zustand) - add, update, delete notes
   - Auth store - login state management

3. Utility functions tests
   - Date formatting
   - Text truncation
   - Markdown sanitization

#### Component Tests
```bash
# Run component tests
cd client
npm run test:components
```

**Test Categories:**
1. NoteList component
   - Renders list of notes
   - Empty state display
   - Click navigation

2. NoteEditor component
   - Markdown input handling
   - Toolbar interactions
   - Save functionality

3. LoginForm component
   - Password input
   - Error display
   - Submit handling

4. ThemeToggle component
   - Light/dark mode toggle
   - Icon state change

### E2E Tests (Playwright)

```bash
# Run E2E tests
cd client
npm run test:e2e

# Run in headed mode
npm run test:e2e:headed
```

**Test Scenarios:**
1. Authentication flow
   - Login with correct password
   - Login with wrong password
   - Logout flow
   - Session persistence

2. Memo CRUD operations
   - Create new memo
   - Edit existing memo
   - Delete memo with confirmation

3. Theme functionality
   - Toggle dark mode
   - Persist theme preference
   - FOUC prevention

4. Responsive design
   - Mobile layout (320px)
   - Tablet layout (768px)
   - Desktop layout (1280px)

### Manual Test Steps

#### Prerequisites
1. Ensure Docker and Docker Compose are installed
2. Clone the repository
3. Copy `.env.example` to `.env` and configure

#### Setup
```bash
# Build and start containers
docker-compose up -d

# Check container status
docker-compose ps

# View logs
docker-compose logs -f
```

#### Test Scenarios

**Scenario 1: Login Flow**
1. Navigate to `http://localhost`
2. Verify login page is displayed
3. Enter correct password
4. Click "Login" button
5. Verify redirect to notes list page
6. Verify session cookie is set

**Scenario 2: Create Memo**
1. Ensure logged in
2. Click "New Memo" button
3. Enter title "Test Note"
4. Enter Markdown content "# Hello\nThis is **bold**"
5. Click "Save" button
6. Verify note appears in list
7. Verify note content renders correctly

**Scenario 3: Edit Memo**
1. Click on an existing memo
2. Modify the title
3. Modify the content
4. Click "Save" button
5. Verify changes are persisted
6. Navigate back to list
7. Verify updated title appears

**Scenario 4: Delete Memo**
1. Click on an existing memo
2. Click "Delete" button
3. Verify confirmation dialog appears
4. Click "Confirm" button
5. Verify note is removed from list

**Scenario 5: Dark Mode Toggle**
1. Note current theme (light/dark)
2. Click theme toggle button
3. Verify theme switches
4. Refresh page
5. Verify theme persists
6. Open in new tab
7. Verify theme is consistent

**Scenario 6: Change Password**
1. Navigate to Settings page
2. Enter current password
3. Enter new password
4. Confirm new password
5. Click "Change Password" button
6. Verify success message
7. Logout and login with new password

**Scenario 7: Responsive Design**
1. Open application on desktop (> 1024px)
2. Verify three-column layout
3. Resize to tablet (640px - 1024px)
4. Verify two-column layout
5. Resize to mobile (< 640px)
6. Verify single-column layout and hamburger menu
7. Test all functionality on mobile

### Coverage Verification

```bash
# Backend coverage check
cd server
npm run test:coverage
# Verify coverage >= 85%

# Frontend coverage check
cd client
npm run test:coverage
# Verify coverage >= 80%
```

## Acceptance Criteria

### Authentication

#### AC-1: Login Success
```gherkin
Scenario: User logs in with correct password
  Given I am on the login page
  When I enter the correct password
  And I click "Login" button
  Then I should be redirected to notes list
  And a session cookie should be set
  And the session should expire in 7 days
```

#### AC-2: Login Failure
```gherkin
Scenario: User enters wrong password
  Given I am on the login page
  When I enter the wrong password
  And I click "Login" button
  Then I should see "Invalid password" error message
  And I should remain on login page
  And no session cookie should be set
```

#### AC-3: Logout
```gherkin
Scenario: User logs out
  Given I am logged in
  When I click "Logout" button
  Then I should be redirected to login page
  And the session cookie should be cleared
```

#### AC-4: Session Expiry
```gherkin
Scenario: Session expires after 7 days
  Given I am logged in
  And 7 days have passed
  When I try to access any protected route
  Then I should be redirected to login page
  And I should see "Session expired" message
```

#### AC-5: Change Password
```gherkin
Scenario: User changes password successfully
  Given I am logged in
  And I am on the Settings page
  When I enter my current password correctly
  And I enter a new password
  And I confirm the new password
  And I click "Change Password" button
  Then I should see "Password changed successfully" message
  And I should be able to login with the new password
```

### Memo Management

#### AC-6: Create Memo
```gherkin
Scenario: User creates a new memo
  Given I am logged in
  When I click "New Memo" button
  And I enter title "My First Note"
  And I enter content "# Hello World"
  And I click "Save" button
  Then the memo should be saved to database
  And I should see "My First Note" in the notes list
  And I should see the memo sorted by update time (newest first)
```

#### AC-7: Edit Memo
```gherkin
Scenario: User edits an existing memo
  Given I am logged in
  And there is a memo titled "Old Title"
  When I click on the memo
  And I change the title to "New Title"
  And I click "Save" button
  Then the memo should be updated in database
  And I should see "New Title" in the notes list
  And the "updatedAt" timestamp should be updated
```

#### AC-8: Delete Memo
```gherkin
Scenario: User deletes a memo
  Given I am logged in
  And there is a memo titled "To Delete"
  When I click on the memo
  And I click "Delete" button
  And I confirm the deletion in the dialog
  Then the memo should be removed from database
  And I should not see "To Delete" in the notes list
```

#### AC-9: Cancel Delete
```gherkin
Scenario: User cancels memo deletion
  Given I am logged in
  And there is a memo titled "Keep Me"
  When I click on the memo
  And I click "Delete" button
  And I click "Cancel" in the confirmation dialog
  Then the memo should remain in database
  And I should still see "Keep Me" in the notes list
```

#### AC-10: View Memo List
```gherkin
Scenario: User views all memos
  Given I am logged in
  And there are 5 memos in the system
  When I navigate to the notes list page
  Then I should see all 5 memos
  And they should be sorted by update time (newest first)
  And each memo should show title and content preview
```

#### AC-11: Empty State
```gherkin
Scenario: User sees empty state when no memos exist
  Given I am logged in
  And there are no memos in the system
  When I navigate to the notes list page
  Then I should see "No memos yet" message
  And I should see "Create your first memo" button
```

### Markdown Support

#### AC-12: Markdown Editing
```gherkin
Scenario: User edits Markdown content
  Given I am logged in
  And I am editing a memo
  When I type "# Heading\n**bold** and *italic*"
  Then I should see the WYSIWYG editor showing formatted content
  And the raw Markdown should be preserved
```

#### AC-13: Markdown Rendering
```gherkin
Scenario: System renders Markdown correctly
  Given I am logged in
  And there is a memo with content "# Title\n- Item 1\n- Item 2"
  When I view the memo
  Then I should see "Title" as a heading
  And I should see a bulleted list with "Item 1" and "Item 2"
```

#### AC-14: XSS Prevention
```gherkin
Scenario: System sanitizes malicious Markdown
  Given I am logged in
  When I create a memo with content "<script>alert('xss')</script>"
  And I save the memo
  Then the script tag should be sanitized
  And no JavaScript should execute when viewing the memo
```

### User Interface

#### AC-15: Dark Mode Toggle
```gherkin
Scenario: User toggles dark mode
  Given I am logged in
  And the app is in light mode
  When I click the theme toggle button
  Then the app should switch to dark mode
  And all UI elements should use dark theme colors
  And the preference should be saved to localStorage
  When I reload the page
  Then the app should remain in dark mode
```

#### AC-16: System Preference Default
```gherkin
Scenario: App respects system theme preference
  Given my system is set to dark mode
  And I have no saved theme preference
  When I first open the application
  Then the app should start in dark mode
```

#### AC-17: FOUC Prevention
```gherkin
Scenario: No flash of unstyled content
  Given I have dark mode preference saved
  When I load the application
  Then the page should render directly in dark mode
  And there should be no flash of light mode before dark mode
```

#### AC-18: Responsive Mobile Layout
```gherkin
Scenario: App adapts to mobile screen
  Given I am logged in
  And my screen width is 320px (mobile)
  When I view the notes list
  Then I should see a single-column layout
  And I should see a hamburger menu icon
  And all interactive elements should be touch-friendly (min 44px)
```

#### AC-19: Responsive Tablet Layout
```gherkin
Scenario: App adapts to tablet screen
  Given I am logged in
  And my screen width is 768px (tablet)
  When I view the notes list
  Then I should see a two-column layout
  And the navigation should be visible
```

#### AC-20: Responsive Desktop Layout
```gherkin
Scenario: App adapts to desktop screen
  Given I am logged in
  And my screen width is 1280px (desktop)
  When I view the notes list
  Then I should see a three-column layout
  And the editor should show side-by-side preview
```

### Performance

#### AC-21: Page Load Performance
```gherkin
Scenario: Application loads within performance budget
  Given I am on a 3G connection
  When I load the application
  Then the page should be interactive within 2 seconds
  And the largest contentful paint should be under 2 seconds
```

#### AC-22: API Response Performance
```gherkin
Scenario: API responds within performance budget
  Given I am logged in
  When I request GET /api/notes
  Then the response should be received within 500ms
  When I request POST /api/notes
  Then the response should be received within 500ms
```

### Security

#### AC-23: Password Hashing
```gherkin
Scenario: Password is securely hashed
  Given the application is configured with a password
  Then the password should be stored as a bcrypt hash
  And the bcrypt cost factor should be >= 10
```

#### AC-24: HttpOnly Cookie
```gherkin
Scenario: Session cookie is secure
  Given I log in successfully
  Then the session cookie should have httpOnly flag set
  And the cookie should have secure flag set (in production)
  And the cookie should have sameSite=lax attribute
```

> Using `sameSite=lax` provides CSRF protection while allowing users to navigate directly to the application via links.

#### AC-25: Rate Limiting
```gherkin
Scenario: Login rate limiting prevents brute force
  Given I am on the login page
  When I enter wrong password 5 times in one minute
  Then I should see "Too many login attempts" error
  And I should be temporarily blocked from logging in
```

#### AC-26: Unauthenticated Access
```gherkin
Scenario: Unauthenticated user cannot access protected routes
  Given I am not logged in
  When I try to access /api/notes
  Then I should receive 401 Unauthorized
  And I should not see any note data
```

### Accessibility

#### AC-27: Keyboard Navigation
```gherkin
Scenario: User can navigate with keyboard only
  Given I am logged in
  When I press Tab key repeatedly
  Then focus should move through all interactive elements
  And I should be able to create, edit, and delete memos using only keyboard
```

#### AC-28: Screen Reader Support
```gherkin
Scenario: Application is accessible to screen readers
  Given I am using a screen reader
  And I am logged in
  When I navigate the application
  Then all interactive elements should have appropriate ARIA labels
  And headings should follow logical hierarchy
  And status messages should be announced
```

## Development Phases

### Phase 1: Backend Foundation (TDD)
**Duration**: Week 1

**Tasks**:
1. Initialize Express + TypeScript project
2. Configure Prisma with SQLite
3. Define Note model schema
4. Write unit tests for validation utilities
5. Implement validation utilities
6. Write integration tests for Notes API (CRUD)
7. Implement Notes API endpoints
8. Write integration tests for Auth API
9. Implement Auth API (login, logout)
10. Write middleware tests
11. Implement auth middleware
12. Achieve 85%+ test coverage

**Deliverables**:
- Working Express server with TypeScript
- Prisma schema and migrations
- Fully tested Notes and Auth APIs
- Test coverage report >= 85%

### Phase 2: Frontend Foundation (TDD)
**Duration**: Week 2

**Tasks**:
1. Initialize React + Vite + TypeScript project
2. Configure Tailwind CSS with dark mode
3. Write tests for useDarkMode hook
4. Implement useDarkMode hook
5. Set up Zustand store for notes
6. Write tests for note store
7. Implement note store
8. Configure React Router
9. Write component tests for LoginForm
10. Implement LoginForm component
11. Write component tests for auth flow
12. Implement authentication flow
13. Set up MSW for API mocking
14. Achieve 80%+ test coverage

**Deliverables**:
- Working React application with TypeScript
- Tailwind CSS with dark mode configured
- Authentication flow functional
- Test coverage report >= 80%

### Phase 3: Core Features (TDD)
**Duration**: Week 3

**Tasks**:
1. Write E2E test for create memo flow
2. Integrate Milkdown editor
3. Write component tests for NoteEditor
4. Implement NoteEditor component
5. Write component tests for NoteList
6. Implement NoteList view
7. Write component tests for NoteCard
8. Implement NoteCard component
9. Write E2E test for edit memo flow
10. Implement edit functionality
11. Write E2E test for delete memo flow
12. Implement delete with confirmation dialog
13. Implement Markdown rendering with react-markdown
14. Run all E2E tests and fix issues

**Deliverables**:
- Fully functional memo CRUD operations
- WYSIWYG Markdown editor
- All E2E tests passing

### Phase 4: Polish & Deploy
**Duration**: Week 4

**Tasks**:
1. Write tests for ThemeToggle component
2. Implement ThemeToggle component
3. Implement responsive layouts
4. Write E2E tests for responsive design
5. Write tests for change password feature
6. Implement Settings page with change password
7. Create Dockerfile for client
8. Create Dockerfile for server
9. Create docker-compose.yml for development
10. Create docker-compose.prod.yml for production
11. Configure Nginx reverse proxy
12. Write deployment documentation
13. Final E2E test run
14. Deploy to VPS
15. Verify production deployment

**Deliverables**:
- Dark mode fully functional
- Responsive design implemented
- Docker configuration complete
- Application deployed to VPS
- All tests passing in production

## Out of Scope (Future Enhancements)

The following features are explicitly out of scope for version 1.0.0 and may be considered for future versions:

- **Search Functionality**: Full-text search across memos
- **Tags/Categories**: Organize memos with tags or categories
- **Note Pinning**: Pin important notes to top of list
- **Trash/Recycle Bin**: Soft delete with recovery option
- **Export**: Export to PDF, HTML, or Markdown files
- **Multiple Users**: Support for multiple user accounts
- **Real-time Sync**: Live synchronization across devices
- **Offline Support**: Progressive Web App with offline capability
- **Collaboration**: Share memos with other users
- **Version History**: Track changes and restore previous versions
- **Attachments**: Support for images and file attachments
- **Keyboard Shortcuts**: Power user keyboard shortcuts

## Documentation Requirements

### README.md
- Project overview and features
- Prerequisites (Node.js, Docker)
- Quick start guide
- Development setup instructions
- Testing instructions
- Deployment instructions
- Environment variables reference
- License information

### API Documentation
- OpenAPI/Swagger specification
- Endpoint descriptions
- Request/response schemas
- Authentication requirements
- Error codes and messages
- Example requests and responses

### Deployment Guide
- VPS requirements
- Docker installation
- Environment configuration
- SSL certificate setup
- Backup procedures
- Update procedures
- Troubleshooting guide

### Environment Variables Reference
- `PASSWORD_HASH`: Bcrypt hash of the user password
- `SESSION_SECRET`: Secret key for session signing
- `NODE_ENV`: Environment (development/production)
- `PORT`: Server port (default: 3001)
- `DATABASE_URL`: SQLite database path

## Change Log

| Date       | Version | Description       | Author           |
|------------|---------|-------------------|------------------|
| 2026-02-16 | 1.0.0   | Initial draft     | Spec-Write Agent |
