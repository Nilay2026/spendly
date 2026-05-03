# Spec: Date Filter for Profile Page

## Overview
This step adds a date-range filter to the profile page so that the logged-in
user can view their expense history scoped to a chosen start and end date.
The profile page (implemented in Step 4) currently shows static account details;
this feature extends it with a filterable expense list that queries the `expenses`
table and displays totals and individual rows within the selected period. This is
the first step that surfaces real expense data to the user in a meaningful way,
bridging the profile UI and the expenses database table.

## Depends on
- Step 1: Database setup (users and expenses tables must exist)
- Step 2: Registration (users can be created)
- Step 3: Login and Logout (session must be populated with `user_id`)
- Step 4: Profile Page Design (`/profile` route and `profile.html` template must exist)

## Routes
- `GET /profile` — extend existing route to accept optional `from_date` and `to_date`
  query parameters; pass filtered expenses and totals to the template — logged-in

No new routes.

## Database changes
No schema changes. One new helper function in `database/db.py`:

- `get_expenses_by_user_and_date_range(user_id, from_date, to_date)` — returns all
  expense rows for the given user where `date` is between `from_date` and `to_date`
  (both inclusive), ordered by `date DESC`. Both date parameters are strings in
  `YYYY-MM-DD` format. Uses a parameterised query — no string formatting.

## Templates
- **Create:** none

- **Modify:**
  - `templates/profile.html` — add a date-filter form (two `<input type="date">`
    fields for From and To dates, plus a Filter button); add an expense table below
    the existing account-info section that shows filtered results (date, category,
    description, amount); add a summary line showing total spend and number of
    transactions for the filtered period; pre-populate the date inputs with the
    current query values so the user can see what they filtered on; show a
    friendly "No expenses found for this period." message when the result set is empty.

## Files to change
- `app.py` — update `GET /profile` to read `from_date` and `to_date` from
  `request.args`, validate them (both must be valid `YYYY-MM-DD` dates; `from_date`
  must not be after `to_date`), call the new DB helper, and pass `expenses`,
  `total_amount`, `from_date`, and `to_date` to the template. Default both dates
  to empty string when not provided (no filter applied, no table shown).
- `database/db.py` — add `get_expenses_by_user_and_date_range`
- `templates/profile.html` — add filter form and expense table (see Templates above)

## Files to create
No new files.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never use f-strings or `%` formatting in SQL
- Passwords hashed with `werkzeug`; verified with `check_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Guard `/profile`: redirect to `/login` if `user_id` not in session
- Date validation must happen in Python (in `app.py`), not only in the browser
- Use `datetime.strptime` to validate date strings; catch `ValueError` and return
  an inline error to the template
- If only one date is provided (the other is blank), show a validation error — both
  fields are required when the filter is used
- Amount column must be formatted to 2 decimal places in the template (e.g. `£12.50`)
- The expense table must only render when both dates are present and valid; otherwise
  show only the filter form

## Definition of done
- [ ] Visiting `/profile?from_date=2026-04-01&to_date=2026-04-30` while logged in
      shows only expenses within April 2026
- [ ] The From and To date inputs are pre-populated with the submitted values after
      filtering
- [ ] Total amount and transaction count are correct for the filtered period
- [ ] Submitting the filter with `from_date` after `to_date` shows an inline error
      and no table
- [ ] Submitting with only one date filled shows a validation error
- [ ] Submitting with both dates empty (clearing the form) hides the table and shows
      no error
- [ ] A date range with no matching expenses shows "No expenses found for this period."
- [ ] Visiting `/profile` with no query params shows the account info but no table
- [ ] Visiting `/profile` while logged out redirects to `/login`
- [ ] The filter form and expense table use only CSS variables — no hardcoded hex
      values
