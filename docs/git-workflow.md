# Git and pull-request workflow

## Branches

Use a short-lived topic branch from the repository's current default branch. Keep one logical change per branch and avoid committing unrelated local work. Rebase or update from the base branch according to the repository's collaboration policy.

## Commits

Write commit messages that explain the intent. A common optional format is type(scope): summary, using types such as feat, fix, docs, test, refactor, build, ci and chore. Follow the repository's existing convention; do not reformat history solely to adopt a new style.

Keep commits reviewable. Do not include secrets, generated build output unless required, local settings or unrelated formatting changes.

## Pull requests

A PR should state:
- The problem and why the change is needed.
- Scope, non-goals and affected modules.
- Design and compatibility implications.
- Tests and checks actually run, with exact results.
- Risks, operational impact and rollback or recovery notes.
- Documentation and decision records updated.

Review the complete diff against the intended base. Resolve comments with code or a reasoned explanation. A green CI run is necessary when required, but does not replace human review.

## Protected operations

Do not force-push shared branches, change branch protection, merge, deploy, release or publish without authorization. Production operations and data migrations follow their own approval process.
