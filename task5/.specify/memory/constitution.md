# TaskPKMS Constitution

 ## Core Principles

 ### I. Library-First
Every distinct capability (storage, sync, encryption, CLI parser, import/export, renderer) is first designed as a small, self-contained library with a stable API and unit tests. Libraries must be independently usable and testable so core features can be reused in GUIs, services, or other tools.

 ### II. CLI-First (Text I/O Contract)
Every public feature is accessible from a canonical CLI interface. The CLI follows a text I/O contract:
- Arguments/flags and stdin → stdout for successful output.
- Errors and diagnostics → stderr with machine-readable details when `--json` is provided.
- Default human-readable output, optional `--json`/`--yaml` for automation.
This ensures automation, scripting, and debugging are first-class.

 ### III. Test-First (Non-Negotiable)
All new behavior must have tests before implementation: unit tests for library APIs, integration tests for CLI workflows, and property or fuzz tests for data conversion and sync logic. CI must run the full suite on PRs and block merges on failures.

 ### IV. Data Safety & Privacy
User data is the highest priority. The system must:
- Persist a clear, documented canonical data model (notes, tasks, links, tags, metadata, history).
- Support optional at-rest encryption (AES-256) with user-provided passphrases or key files; encryption is opt-in but fully supported.
- Offer atomic write semantics and safe crash recovery (journaling or write-then-rename patterns).

 ### V. Simplicity, Interoperability & Minimalism
Start simple but design for interoperability: plain-text-first storage (Markdown + frontmatter), open import/export (Markdown, Org, JSON), and minimal surface area for the CLI. Avoid premature optimization; prefer clear behavior and predictable defaults.

 ## Additional Constraints & Requirements

 ### Project Scope
- Provide a CLI-based Task Manager + Personal Knowledge Management System (PKMS).
- Primary goals: create/edit/list/search tasks and notes; link notes; persistent storage; optional syncing; secure export/import.

### Data Model
- Entities: `Note`, `Task`, `Project`, `Tag`, `Link`, `Attachment`, `Revision`.
- Each entity has a stable schema (human-readable metadata + body). Example: file storage uses Markdown files with YAML/TOML frontmatter containing stable keys: `id`, `title`, `created`, `modified`, `status`, `due`, `tags`, `links`.
- Every entity MUST include a stable `id` (UUID v4) and revision metadata for conflict detection.

### Storage Backends
- File-based backend (default): directory-per-repo or single-folder flat files; Markdown + frontmatter.
- Optional SQLite backend for advanced querying and atomic transactions.
- Backend interface must be pluggable so additional backends (remote, cloud) can be added.

### Sync & Collaboration
- Optional two-way sync modeled as a pluggable adapter (remote adapter). Sync must be conflict-aware and provide clear conflict resolution strategies (last-writer-wins, merge helpers, manual resolution).
- Offline-first design: local operations always succeed; syncing is background/explicit.

### Security
- Optional encryption-at-rest for all content. Keys must be user-controlled.
- Sensitive operations that reveal secrets should require explicit flags and warnings in human-readable output.
- Follow least-privilege for file permissions; created files default to user-only access where OS allows.

### CLI UX and Commands
- Core commands and behaviors:
	- `taskpkms init [PATH]` — initialize a repository/storage.
	- `taskpkms new note "TITLE" [-t tags]` — create a note.
	- `taskpkms new task "TITLE" [-p project] [--due DATE] [--priority N]`
	- `taskpkms edit <id|path>` — open item in editor defined by `$EDITOR`.
	- `taskpkms list [notes|tasks] [--filter 'query'] [--json]`
	- `taskpkms show <id> [--history] [--json]`
	- `taskpkms search 'query' [--fields=title,body,tags] [--json]`
	- `taskpkms tag add|rm <id> <tag>`
	- `taskpkms link add <from-id> <to-id>`
	- `taskpkms export --format md|json|org [--out PATH]`
	- `taskpkms import --format md|json|org --src PATH`
	- `taskpkms sync [--push|--pull|--both]`
	- `taskpkms doctor` — repository health checks (corruption, missing metadata, permissions).
- Command behavior rules:
	- Support `--json` for all commands that output structured data.
	- Exit codes: `0` success, `>0` errors. Define a small set of documented numeric codes for common failures (e.g., `2` = usage error, `3` = data error, `4` = permission error).

### Input/Output Formats
- Canonical storage: Markdown files with YAML/TOML frontmatter.
- Machine formats for interchange: JSON (schema documented and versioned) and optional YAML.
- Include a schema file (`schema/v1.json`) in the repository describing the JSON interchange format.

### Plugin Architecture
- Provide a simple plugin hook model for pre/post operations (e.g., `pre-save`, `post-sync`) and for search/index providers.
- Plugins run as separate processes or scripts (avoid in-process arbitrary code execution by default) and communicate via stdin/stdout (JSON RPC or simple newline-delimited JSON).

### Performance & Scale
- Designed for single-user repositories with thousands of notes/tasks; CLI operations should complete interactively (< 200–500 ms) for common queries. Use indexing (SQLite or simple file-based cache) when necessary.

### Observability & Logging
- Provide structured logs when `--verbose` or `--log-format=json` are enabled. Default logging muted to only warnings/errors.

## Development Workflow & Quality Gates

### Testing
- Unit tests for all library code. Integration tests for end-to-end CLI flows. Contract tests for storage backends and sync adapters.
- Provide an automated test harness that can run against both file and SQLite backends.

### CI Requirements
- PRs must pass: lint, unit tests, integration tests (where fast), schema validation, and basic CLI smoke tests.

### Code Review & Change Policy
- Major changes (data model, storage format, default encryption behavior) require a design doc, migration plan, and at least two reviewers.
- Backwards-incompatible changes to on-disk formats must include migration tooling and be gated by a major version bump.

### Versioning and Releases
- Use semantic versioning: MAJOR.MINOR.PATCH.
- Document breaking changes in the release notes and the migration guide in `docs/migrations.md`.

### Documentation
- `README.md` with quickstart and core command list.
- `docs/` contains: schema, plugin API, migration guide, CLI reference, security guide, and examples.

## Governance

- Constitution authority: this document is the canonical source for architectural and UX constraints; deviations require an explicit amendment recorded in `docs/constitution-amendments.md`.
- Amendment process: propose amendment as a PR; include rationale, migration steps (if any), and at least two approvals from maintainers. For major policy changes, include a 7-day comment period.
- **Documentation Policy**: User documentation MUST always be created and kept up-to-date when merging into the master branch. This ensures that users have access to accurate and current information about the system's features and usage.

**Version**: 0.1.0 | **Ratified**: 2025-11-19 | **Last Amended**: 2025-11-19

