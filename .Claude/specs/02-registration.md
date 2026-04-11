# Spec: Registration

## Overview
Implement user registration so that new visitors can create a Spendly account.
This step wires up the existing `register.html` form to a POST handler that
validates input, checks for duplicate emails, hashes the password, inserts the
user into the database, and redirects to the login page on success. It also
configures Flask's `secret_key` (required for sessions used in later steps).

## Depends on
- Step 01 — Database Setup (users table must exist)

## Routes
- `GET  /register` — Render the registration form — public (already exists, no change)
- `POST /register` — Process registration form submission — public

## Database changes
No schema changes. Two new helper functions in `database/db.py`:

- `create_user(name, email, password)` — hashes password, inserts row into
  `users`, returns the new user's `id`.
- `find_user_by_email(email)` — returns the matching `users` row or `None`.

## Templates
- **Modify:** `templates/register.html` — already renders `{{ error }}`; no
  structural changes needed. Ensure the form `action="/register"` and
  `method="POST"` are present (they already are).

## Files to change
- `app.py` — add `secret_key`, convert `/register` to accept both GET and POST,
  add POST logic (validate → check duplicate → create user → redirect to login).
- `database/db.py` — add `create_user()` and `find_user_by_email()`.

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never use string formatting in SQL
- Passwords hashed with `werkzeug.security.generate_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- `app.secret_key` must be set before any session usage; use a hard-coded dev
  string for now (e.g. `"spendly-dev-secret"`) — do not read from env yet
- On duplicate email show the error inline via `render_template("register.html", error=...)` — do **not** redirect
- On success redirect to `/login` with no session set (login is Step 3)
- Validate server-side: name non-empty, valid email format not required (browser
  handles it via `type="email"`), password ≥ 8 characters

## Definition of done
- [ ] `POST /register` with valid data inserts a new user and redirects to `/login`
- [ ] Submitting a duplicate email re-renders the form with the message
      "An account with that email already exists."
- [ ] Submitting a password shorter than 8 characters re-renders the form with
      "Password must be at least 8 characters."
- [ ] Submitting an empty name re-renders the form with "Name is required."
- [ ] The stored password is a bcrypt/werkzeug hash, never plaintext
- [ ] `find_user_by_email()` returns `None` for unknown emails
- [ ] App starts without errors after changes
