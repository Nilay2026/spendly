# Spec: Profile Page Design

## Overview
This step replaces the `/profile` placeholder with a fully designed profile page
that displays the logged-in user's account details and provides two self-service
forms: one to update their display name and one to change their password. It also
refactors `dashboard.html` to extend `base.html` (removing its standalone inline
styles) and adds an authenticated navigation state to `base.html` so that
Dashboard, Profile, and Logout links appear when a user is signed in.

## Depends on
- Step 1: Database setup (users table must exist)
- Step 2: Registration (users can be created)
- Step 3: Login and Logout (session must be populated with `user_id`, `user_name`, `user_email`)

## Routes
- `GET /profile` — display profile page with user info and edit forms — logged-in
- `POST /profile/update-name` — process name-change form — logged-in
- `POST /profile/update-password` — process password-change form — logged-in

## Database changes
Three new helper functions in `database/db.py` (no schema changes — `users` table
already has all required columns):

- `get_user_by_id(user_id)` — fetch a single user row by primary key
- `update_user_name(user_id, name)` — update the `name` column
- `update_user_password(user_id, new_password)` — hash and update `password_hash`

## Templates
- **Create:**
  - `templates/profile.html` — profile page with account info card, update-name form, and change-password form

- **Modify:**
  - `templates/base.html` — add authenticated nav state: when `session.user_id` is set show links to Dashboard, Profile, and a Logout button; hide the Sign in / Get started links
  - `templates/dashboard.html` — refactor to extend `base.html`; replace all inline `<style>` blocks and hardcoded hex values with CSS-variable classes from `style.css`

## Files to change
- `app.py` — replace `/profile` placeholder with real view; add `POST /profile/update-name` and `POST /profile/update-password` routes
- `database/db.py` — add `get_user_by_id`, `update_user_name`, `update_user_password`
- `templates/base.html` — add authenticated nav links
- `templates/dashboard.html` — extend `base.html`, remove inline styles

## Files to create
- `templates/profile.html`

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with `werkzeug.security.generate_password_hash`; verified with `check_password_hash`
- Use CSS variables (`var(--accent)`, `var(--danger)`, etc.) — never hardcode hex values
- All templates extend `base.html`
- Guard every route: redirect to `/login` if `user_id` not in session
- On POST routes, always redirect after success (PRG pattern) to prevent double-submit
- Flash-style feedback: pass `success` or `error` context variables to the template; do not use Flask's `flash()` — keep it simple with template variables
- The change-password form must require the current password before accepting a new one
- New password must be at least 8 characters

## Definition of done
- [ ] Visiting `/profile` while logged out redirects to `/login`
- [ ] Visiting `/profile` while logged in shows the user's name, email, and member-since date
- [ ] Submitting the update-name form with a valid name updates the name shown on the page and in the session
- [ ] Submitting the update-name form with an empty name shows an inline error without changing the database
- [ ] Submitting the change-password form with the wrong current password shows an error
- [ ] Submitting the change-password form with a new password shorter than 8 characters shows an error
- [ ] Submitting the change-password form with a valid current password and valid new password succeeds, and the user can log out and back in with the new password
- [ ] The navbar on every page shows Dashboard / Profile / Logout when logged in, and Sign in / Get started when logged out
- [ ] `dashboard.html` no longer contains any `<style>` blocks or hardcoded hex colour values
- [ ] The profile page passes W3C HTML validation (no stray tags, valid nesting)
