# Calendar connect (optional integration)

Connect a calendar so the morning brief can see today's actual schedule, not just the task list. This is a **read-only** integration: the calendar is read live each morning and folded into the brief. Calendar data is never stored in the vault (doctrine section 3, the rows iron law: high-frequency live data stays external, the vault holds pointers and judgment, not a mirror of your agenda).

Two supported providers. Google is the recommended path because it is a one-click first-party connector. Lark is for owners already living in Lark / Feishu.

## Provider A: Google Calendar (recommended, one-click)

Google Calendar is a first-party connector in the Claude Code connector directory (Anthropic and Partners). No config files, no manual OAuth.

1. Open the connector directory: the Directory panel, then the Connectors tab. Under Anthropic and Partners, find **Google Calendar**.
2. Click the `+` and authorize with the Google account that holds the calendar.
3. Leave the four read-only tools on **Always allow** (`list_events`, `list_calendars`, `get_event`, `suggest_time`) so the morning read never triggers a permission prompt. Leave the write and delete tools (`create_event`, `delete_event`, `respond_to_event`, `update_event`) on **Needs approval**, which is their default. The morning brief only reads.
4. Record `calendar_provider: google` in `99_Meta/bootstrap-progress.md`.

That is the whole setup.

## Provider B: Lark / Feishu (via CLI)

There is no first-party Lark connector, so Lark goes through the official CLI (github.com/larksuite/cli), which covers Calendar and is built for AI agents.

1. Install: `npm install -g @larksuite/cli`.
2. Configure app credentials: `lark-cli config init`.
3. Authenticate: `lark-cli auth login --recommend`.
4. Verify it can read the agenda: `lark-cli calendar +agenda`.
5. Record `calendar_provider: lark` in `99_Meta/bootstrap-progress.md`. If the binary is not on PATH, record its full path too (`calendar_lark_bin:`), so the morning read can call it directly.

If the owner wants to connect Lark later rather than install inline (to keep setup short), record `calendar_provider: none` for now and point them back here when they are ready.

## Skip

Record `calendar_provider: none`. The morning brief works fully without a calendar; it just will not show a schedule line. The owner can connect any time later by saying "connect my calendar".

## How the morning read uses this

At session start, the command-base skill reads `calendar_provider:` and, if set, pulls today's events:

- `google`: call the Google Calendar connector's `list_events` tool for today on the primary calendar. Refer to the tool by its logical name; the actual tool is namespaced with a per-install id, so never hardcode that id.
- `lark`: run `lark-cli calendar +agenda` (use the recorded full path if the binary is not on PATH).

The read is **fail-soft** by contract: if the connector is not authorized, the CLI is missing, the auth has expired, or the call errors or returns nothing, the skill omits the schedule line and carries on. A calendar problem never blocks or delays the morning brief.
