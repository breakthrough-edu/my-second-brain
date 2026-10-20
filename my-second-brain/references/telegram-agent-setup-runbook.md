# Telegram AI Agent Setup Runbook

Version: 1.1 (2026-10; written against Claude Code 2.1.240)  
Audience: Business owners building their first bounded AI agent  
Outcome: An owner-only Telegram bot can receive one bounded request, return a draft or approval request, survive a restart, and stop safely.

What changed in 1.1: a section on running headless Claude Code safely, placed before Stage 5, and new lines in Stages 4, 5, 8 and 9.

## Start here

Open a fresh Claude Code session inside a new, dedicated project folder. Use the guided prompt from the Builder Portal. It directs Claude Code to the public copy of this runbook.

If Claude Code cannot access the public URL, download this Markdown file, attach it to the session, then paste:

> Read this entire Markdown file first. Follow it as the setup authority. Begin with Stage 0 and stop at every human gate. Do not ask me to paste secrets into chat.

Claude Code must read this whole file before changing anything.

## Rules for Claude Code

1. Inspect the machine and current project before proposing commands.
2. Ask one bounded question at a time.
3. Never ask the learner to paste a bot token, API key, password, or private credential into chat.
4. Never print a secret into logs, screenshots, URLs, source code, Git history, or terminal output.
5. Pause for explicit approval before installing software, creating an external account, granting permissions, writing outside the chosen project folder, or creating a background service.
6. Never bypass permission checks.
7. Keep the first version owner-only. Do not enable a group or public audience during the initial setup.
8. Give the agent only the tools required for one job.
9. Read every created or changed resource back before claiming success.
10. Do not call the agent Running until a real Telegram message succeeds after the runtime has restarted.

Create `SETUP-STATUS.md` in the project folder. Record each stage as Not started, In progress, Blocked, or Proven. Record evidence without secrets.

## The architecture you are building

```text
Owner message
    ↓
Telegram bot identity
    ↓
Sender and chat allowlist
    ↓
Bounded agent core
    ↓
One approved skill or tool
    ↓
Draft, answer, or approval request
    ↓
Verified Telegram response
```

BotFather creates the Telegram identity and token. It does not create the intelligence. The local or hosted runtime receives messages and calls the bounded agent.

## Honest status ladder

Use only these labels:

1. Designed
2. Local plumbing tested
3. Channel connected
4. Agent path tested
5. Approval tested
6. Restart proven
7. Running

Never skip a label. A successful demo inside the current terminal is not Restart proven.

## Stage 0: Define one job and one boundary

Claude Code must ask for:

- The single job the agent performs.
- The human owner.
- Who may send requests in version one.
- What information it may read.
- What information is explicitly excluded.
- Which skill, SOP, Method, or Playbook it follows.
- Whether it only answers, drafts, writes, sends, or deletes.
- Which actions require approval.
- What counts as proof.
- What failure looks like.
- How the owner disables and stops it.

Recommended first job: receive a question from the owner and return a draft. It should not send an external message or change a business system.

Human gate: The learner approves the written boundary before any bot or runtime is created.

## Stage 1: Inspect the machine and choose the runtime

Claude Code must inspect, not assume:

- Operating system and version.
- Node.js and npm availability.
- Git availability.
- Claude Code version.
- Whether this is an always-on desktop, a laptop, or a VPS.
- Whether the chosen folder is local and dedicated to this bot.

Do not place the project inside the learner's Second Brain. Do not give the bot unrestricted access to the Second Brain or the whole computer.

Choose one agent engine:

### Option A: Claude Code Agent SDK or non-interactive Claude Code

Use this for a personal, owner-operated local agent when the current Claude setup supports it. Claude Code must verify the latest official documentation before generating the implementation.

### Option B: Anthropic Messages API or Managed Agents

Use this when the bot must run as a service independent of an interactive Claude Code login. This needs an API key and may use separate platform billing. Claude Code must explain that boundary before the learner chooses it.

Human gate: The learner chooses the host and agent engine after hearing the operational and billing implications.

Current official references:

- [Claude Code headless mode](https://code.claude.com/docs/en/headless)
- [Claude Code CLI reference](https://code.claude.com/docs/en/cli-usage)
- [Anthropic Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview)
- [Managed Agents](https://platform.claude.com/docs/en/managed-agents/quickstart)

## Stage 2: Create the Telegram bot identity

The learner completes this stage in Telegram:

1. Open the verified `@BotFather` account.
2. Send `/newbot`.
3. Choose a display name.
4. Choose a unique username. Telegram normally requires the username to end in `bot`.
5. Receive the bot token.
6. Store the token in a protected secret location that the runtime can read.

The token is a password. Do not paste it into Claude Code chat. Do not place it inside a Markdown file, source file, screenshot, Git commit, or command that remains in shell history.

If a token is exposed, the learner must revoke it through BotFather before continuing.

Human gate: The learner confirms only that the token exists in protected storage. Claude Code must not ask to see it.

Current official references:

- [Telegram bot tutorial](https://core.telegram.org/bots/tutorial)
- [Telegram Bot API](https://core.telegram.org/bots/api)

## Stage 3: Scaffold a dedicated project

Claude Code should propose a small Node.js and TypeScript project after checking the current supported versions and libraries. The project should contain clear boundaries such as:

```text
telegram-agent/
  src/
    telegram/
    agent/
    approvals/
    tools/
    audit/
    health/
  tests/
  .env.example
  SETUP-STATUS.md
  README.md
```

Requirements:

- The real secret file is excluded from Git.
- `.env.example` contains names only, never values.
- The runtime validates required configuration at startup without printing values.
- Logs omit message content unless the learner explicitly approves a narrow debugging window.
- The bot has one clear stop control.

Human gate: The learner approves the proposed dependencies and file changes before installation.

## Stage 4: Prove the Telegram connection without AI

Start with long polling. It is the simplest first build and does not need a public endpoint.

Claude Code must implement and prove:

1. The bot token is valid through Telegram's `getMe` method.
2. The bot receives an owner message through `getUpdates` or a maintained library that uses it.

   Only one process may poll `getUpdates` for this token, on any machine. Two pollers at once are answered with `409 Conflict`, and any call that passes an `offset` confirms every earlier update for everyone, so a check run by hand (with curl, for example) while the bot is running can swallow updates the bot never saw. Never run `getUpdates` by hand to look up a chat id; have the bot print the ids it sees into its log instead.

3. The update offset advances so the same message is not handled twice.
4. The sender user ID and chat ID are captured for allowlisting without publishing them.
5. The bot returns a static reply.
6. An unapproved sender is rejected before any model call.
7. For an approved sender, a message type the bot does not handle (voice, sticker, photo, document) gets a one-line reply naming the type. An unapproved sender still gets nothing, as in step 6. An approved sender's message dropped with no reply and no log line looks exactly like a dead bot.

Telegram keeps pending updates for a limited period. Long polling and webhooks are mutually exclusive. Do not configure a webhook during this first build.

Proof required:

- A real owner message reached the local runtime.
- One static reply returned to the same chat.
- A rejected sender test did not call the agent.
- An approved sender's voice note or sticker got a reply naming the type.
- The audit log records time, event type, result, and correlation ID without secrets.

Status after proof: Channel connected.

## Headless Claude Code: the cage, the clock, and the false alarms

Applies when the engine is Option A run as `claude -p` from your own runtime. Read this before the agent path stage below builds its first run. Written against Claude Code 2.1.240; on any other version, re-read `claude --help` before trusting a flag, and re-run the proof in rule 4 after every upgrade. If you use the Agent SDK instead, map each rule to its current documentation and keep rule 4 either way.

1. **The tool gate is `--tools`.** `--allowedTools` only pre-approves tools; it does not unload the rest, so `--allowedTools Read` still loads a shell and tools that can start sub-agents or schedule jobs. On 2.1.240, `claude --help` says it: `--tools ""` disables all tools. Zero tools (Pattern B): `--tools ""`. Files only (Pattern A): `--tools Read,Edit,Write,Glob,Grep`. Treat `--disallowedTools` and a settings `deny` list as a second layer, never as the gate.
2. **Put `--permission-mode` on the command line of every run.** On 2.1.240 the values `claude --help` lists are `acceptEdits`, `auto`, `bypassPermissions`, `manual`, `dontAsk` and `plan`. Zero-tool bot: `manual`. Files-only bot: `acceptEdits`. Note that with `manual` the init event (rule 4) reports `permissionMode: "default"`: the cage check compares against the value the init event reports (the table in rule 4), not against the word you typed. Without the flag the run inherits the machine's global default, which on a developer's own machine is often bypass. Never `bypassPermissions`, never `--dangerously-skip-permissions`.
3. **Add `--strict-mcp-config` and pass no `--mcp-config`.** The run then loads zero MCP servers, so the bot cannot reach the integrations configured for your interactive sessions.
4. **Check the cage from the runtime, every run, never from the model.** Run with `--output-format stream-json --verbose` and parse one JSON event per line. Find the event with `type: "system"` and `subtype: "init"` (it is not always the first line). Its `tools` (sorted) and `permissionMode` must match the expected values for the cage you built, exactly; on any mismatch kill the run, log `CAGE BREACH`, and tell the chat. A result with no init event is a breach too. Expected on 2.1.240: zero-tool cage, `tools` `[]` and `permissionMode` `default` (what `--permission-mode manual` reports); files-only cage, `tools` `Edit,Glob,Grep,Read,Write` and `permissionMode` `acceptEdits`. Verify these once on your installed version by running the flags in a terminal before you hard-code them: the chat-bridge repo's `scripts/probe-claude.sh` checks the files-only pair only (its expected tools and mode are fixed in the script); for the zero-tool pair, run the same `claude -p` command yourself with `--tools "" --permission-mode manual` and read the init event. Also read the init event's `memory_paths` (rule 5): with `CLAUDE_CODE_DISABLE_AUTO_MEMORY` set, no `auto` directory should appear in it. Log one line per run, `cage ok: tools=<sorted list> mode=<mode>`, and one line per entry in the result's `permission_denials`, `denied: <tool> <input>`. Do not ask the model what tools it has: a zero-tool model asked to run a command will write a fake tool call in prose. The proof depends on which cage you built, and you never widen `--tools` to make a proof pass:
   - **Zero-tool cage** (`--tools ""`): the init event's `tools` is `[]`, and a successful result has `num_turns` equal to 1 and `permission_denials` equal to `[]`. Breach condition: `num_turns` greater than 1, or `permission_denials` not empty; either means the model tried to act, log it loudly. A result with `is_error` true and `num_turns` 0 is not a breach: it is a run that never got going (a dead `--resume`, rule 9, or a login problem, rule 6), handle those first. There is no `denied:` line to look for here: a run with no tools has nothing to deny.
   - **Files-only cage**: ask the bot to read `/etc/hosts`; the log must show `denied: Read /etc/hosts` and the reply no file contents. A refusal with no `denied:` line is not a pass, the model never tried; ask again more directly. Also expect a write outside the working directory, and a write to `.claude/settings.local.json` inside it, to be denied.
5. **Spawn it right.** Absolute path to `claude` (`which -a claude`, the line starting with `/`); the message as one argv element, never a shell string; `cwd` pinned to the project folder; `detached: true` so a stop can kill the whole process group; a scrubbed environment built by hand, carrying at least `HOME PATH USER SHELL TERM LANG` plus the two switches below, and nothing inherited from the parent. `USER` and `SHELL` are not optional: without them, on macOS, `claude -p` cannot find your login in the keychain and every answer becomes `Failed to authenticate: OAuth session expired and could not be refreshed`, while your login is fine and `claude login` changes nothing. **Keep your own instruction files out of the bot's runs.** A headless run loads the same instruction files your interactive sessions do: your user-level `CLAUDE.md` and your Claude Code auto-memory. Whatever is in them shapes every reply, and anyone who can message the bot can ask it to repeat them. Set `CLAUDE_CODE_DISABLE_CLAUDE_MDS=1` and `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` in the child's environment (both names are present in the 2.1.240 binary; prove the switches are on the live child with `ps eww -p <pid>`, which must show both variables; with the auto-memory switch set, the init event's `memory_paths` should show no `auto` directory). If you followed the chat-bridge approval-card chapter, which tells you to write the draft format into the working directory's `CLAUDE.md`, put that format into `--append-system-prompt` instead, and put the bot's own instructions in the prompt or an `--append-system-prompt` instead. `--setting-sources` (2.1.240 lists `user`, `project`, `local`) is a second lever: `--setting-sources user` keeps the working directory's project settings and `.mcp.json` out of the run, but it also drops any project-level hooks and permission rules you meant to keep; it decides which `CLAUDE.md` files load, but not auto-memory; the two switches above remain the way to keep both out.
6. **Four false alarms while testing, each one looks like a broken bot.** (a) A process started from an SSH session cannot reach the login keychain and reports "Not logged in". (b) Running `claude -p` from inside an AI agent's shell tool with its sandbox on, Claude Code's own Bash tool included, gives the same false "OAuth session expired". (c) A "quick load check" that does `import()` of the bot file runs the bot: a second consumer on the same bot app, competing for the same events. Check that a file loads with `node --check`, never with `import()`. (d) The foreground test is therefore the learner's job: the learner starts the bot in their own terminal window; Claude Code reads the log file, asks the learner what appeared in the chat (it cannot read the chat itself), and does not start the bot from its own shell tool. One probe settles login questions: run `claude -p` once with a clean env that includes `USER` and `SHELL`, from a normal terminal, not over SSH, not from an agent shell. `is_error: false` means your runtime's env was the problem; an error means log in again.
7. **Your global `~/.claude/settings.json` applies to headless runs too, hooks included**, and a `--settings` file merges with it rather than replacing it. A hook that never returns under a background service (one that plays a sound or waits for a prompt) holds the run forever: the answer is written within seconds and no `result` event ever arrives, so the bot looks silent. Read the global file line by line before creating the service; when a run hangs, `pgrep -P <claude pid>` shows the child that never exited. Fix it in the global file; `--bare` is not an escape, it also skips your login.
8. **Time limits: a silence watchdog plus a hard cap, never one fixed timeout.** Reset the watchdog on every stream event, pause it while a tool call is open, and kill when nothing has happened for the idle limit; keep a hard cap behind it for a tool that never returns. A fixed timeout is wrong in both directions: it kills a healthy long job and makes you wait the full time on a hung one. Kill the whole process group (`process.kill(-pid)`), then force the pipes shut: killing only `claude` leaves its hooks and shells holding the pipeline. Tell the chat plainly when a run was stopped and why. Reference defaults in the chat-bridge repo: 5 minutes idle, 45 minutes cap.
9. **Sessions.** If you keep per-sender memory with `--resume`, store a session id only from a run whose result has `is_error: false`. When a stored session is gone, `--resume` prints `No conversation found with session ID` and returns an error with `num_turns` 0: retry that message once without `--resume`, drop the dead id, and never store it again. Otherwise that one sender is stuck on an error for every message until the file is cleared by hand. Give the owner a `/new` command that resets the thread.
10. **Busy is not silent.** If a message arrives while a run is in progress, acknowledge it at once ("Got it, 1 task ahead of yours"). Bound the queue, and when a message is refused, say which limit it hit. Every limit (idle, cap, queue size, message length, send timeout, retries) is a named constant in one place.
11. **Decide what a restart does with messages that arrived while the bot was down, and make it visible.** Default: do not execute them; on startup advance past the backlog and send the owner one line saying how many were skipped and to resend what still matters. Executing a stale command minutes or hours late is the dangerous case; dropping it silently is the other bug. If your job is answer-only or draft-only you may choose to process the backlog instead; write the choice into `SETUP-STATUS.md`.

Reference for these rules, with a runnable probe for the files-only cage (`scripts/probe-claude.sh`), the proofs per cage (`docs/proof.md`), the full list of failures that only show up under a background service (`docs/gotchas.md`), and a reference run (`bridge/run-claude.mjs`): https://github.com/breakthrough-edu/claude-code-chat-bridge. Read it for shape; build the stages in this runbook.

## Stage 5: Connect one bounded agent path

The agent core needs:

- A short system prompt that names the job and finish line.
- The minimum context required for the job.
- One skill, SOP, Method, or Playbook reference.
- A tool set declared with `--tools` (empty for Pattern B), checked from the init event on every run.
- A maximum turn limit.
- A time or cost limit appropriate to the chosen engine.
- Structured output with a result, evidence, status, and proposed next action.

Build the run exactly as the section "Headless Claude Code" above says: `--tools` is the allowlist (`--allowedTools` is not), `--permission-mode` goes on the command line, no MCP servers, and the init event is checked on every run. `claude --help` on 2.1.240 lists `--max-budget-usd` (print mode only) and no `--max-turns`; use a budget cap as an extra layer, not as the gate, and check your installed version for both. Do not copy old flags without checking `claude --help`.

First test:

1. Owner sends one approved request.
2. Allowlist passes.
3. Agent receives only the approved context.
4. Agent produces a draft.
5. Bot returns the draft to the owner.
6. No business system changes.

Status after proof: Agent path tested.

## Stage 6: Add the approval gate

Classify every possible result:

- Answer only: may return immediately.
- Draft only: may return immediately and remain unsent.
- Internal reversible write: requires the boundary defined in Stage 0.
- External, financial, sensitive, or irreversible action: requires explicit human approval.

For version one, the bot should show a short action preview and offer Approve or Reject. Approval state must be tied to the requesting owner, the exact proposed action, and an expiry time. It must not accept an old approval for a changed action.

Claude Code must test:

- Reject performs no action.
- Approve performs only the previewed action.
- Repeated button presses do not repeat the action.
- Expired approval cannot execute.
- Failure returns a clear signal and preserves enough evidence to investigate.

Status after proof: Approval tested.

## Stage 7: Add operational controls

Before background operation, implement:

- A health signal that proves the listener and agent path are available.
- Rate limits and basic abuse protection.
- Timeouts and bounded retries.
- Duplicate-event protection.
- An append-only audit trail without secrets or unnecessary message bodies.
- A visible disable switch.
- A clean stop path.
- A failure notification to the owner.
- Token rotation instructions.

The owner must be able to stop the service without asking the agent itself.

## Stage 8: Create the background service

Only after the foreground tests pass, Claude Code may propose a persistent service:

- macOS: a user-level launch service.
- Linux or VPS: a restricted system service.
- Another managed runtime: only if the learner chooses it and understands cost, secrets, and logs.

Use absolute executable and project paths. Give the service the minimum file and network permissions. Do not enable automatic restart loops without a retry ceiling and failure signal.

On macOS: keep everything the service itself opens (its working directory, its log paths, the file it executes) outside the protected folders: `~/Documents`, `~/Desktop`, `~/Downloads` and cloud-synced folders. A service that points into them works every time you start it by hand and refuses to start after the first cold reboot, with exit code 78 and an empty log. A folder such as `~/Scripts/<bot>/` is the usual choice. The program the service starts can still read protected folders, on one condition: Full Disk Access is granted to that program's binary (the `node` you point the service at) on that machine. The grant is per binary and per machine, it does not sync, and after granting or changing it the job must be unloaded and loaded again (`bootout`, then `bootstrap`); a `kickstart` does not re-evaluate it.

Before this stage, answer the eight questions every unattended worker answers (Reads, Writes, Identity, Limits, Stop, Proof, Heartbeat, Rollback); a question you cannot answer is a hole to name, not a blank. The worksheet is `EIGHT-CELLS.md` in the chat-bridge repo; the Builder Portal's Explore page has the Resident Workers Playbook that explains each one.

Human gate: The learner approves creation of the service after reviewing its location, permissions, start behavior, stop method, and logs.

## Stage 9: Restart and recovery proof

Prove the runtime can restart from saved files:

1. Stop the process through its documented control.
2. Start it through the intended service path.
3. Confirm what the restart did with messages that arrived while it was down: by default they were skipped and the owner got one line saying so.
4. Send a fresh owner message.
5. Confirm the sender filter, agent path, and approval state still behave correctly.
6. Confirm old pending approvals do not execute after restart.
7. Confirm the audit trail shows the new run.

Status after proof: Restart proven.

## Stage 10: Decide whether to broaden access

Do not add a group or team yet unless all earlier stages passed.

If access is broadened:

- Use an explicit user and chat allowlist.
- Require the bot to be mentioned in groups.
- Keep sensitive actions owner-only.
- Test one unapproved user and one unapproved group.
- Document who owns access changes.

Only repeated real use with a current owner justifies Running.

## Optional extensions after the core path works

These are not part of the first completion:

- Read-only access to part of your Second Brain, as a second build after Restart proven, and only once the exclusions are enforced by the runtime, not just written down. Shape: working directory set to a folder of the vault the bot may read (a bot-specific subfolder if that is all the job needs, the vault itself only if the job needs it), `--tools Read,Glob` (no `Grep`: a `Read` deny rule is enforced on `Read` and only best-effort on the search tools, so leave `Grep` out, or prove every excluded folder against `Grep` as well), `--permission-mode manual`, owner-only, the cage logged on every run, and a `permissions.deny` list in the bot's own `--settings` file with one rule per excluded folder, written as a path pattern such as `Read(./<private-folder>/**)` relative to the working directory (or `Read(~/path/**)`, `Read(//absolute/**)`), proved by a `denied: Read <path>` line when you ask the bot to read a file in each excluded folder, and by a `Glob` request on the same folder returning nothing. Accept the consequences before you build it: with the rule 5 switches on, neither the vault's `CLAUDE.md` nor a parent folder's `CLAUDE.md` loads as instructions; if the bot needs the vault's own guidance, have it read those files with `Read`. The vault's project settings and hooks still load from that working directory, with the global settings file merged on top; if the vault sits under a protected folder, the service's binary needs Full Disk Access (macOS); and everything not denied is readable by whoever can message the bot, which is why it stays owner-only. A bot that can also write to the vault is a third build, through the approval gate.

Add one extension at a time and repeat the permission, failure, restart, and stop tests.

## Final verification checklist

- [ ] One job and one owner are written down.
- [ ] The bot token never entered chat, source, logs, screenshots, or Git.
- [ ] Sender and chat filters run before the model.
- [ ] The agent sees only the minimum context.
- [ ] Tools are narrow and explicit.
- [ ] `--tools` and `--permission-mode` are on the command line of every headless run; `--strict-mcp-config` with no `--mcp-config`.
- [ ] Every run logs `cage ok: tools=... mode=...` from the init event, and `--tools` was never widened to make a proof pass.
- [ ] Cage proof for the cage built: zero-tool, every successful result `num_turns` 1 and `permission_denials` `[]`; files-only, a request to read `/etc/hosts` logged `denied: Read /etc/hosts`.
- [ ] The child's live environment (`ps eww -p <pid>`) carries `USER` and `SHELL` and the two `CLAUDE_CODE_DISABLE_*` switches (proved on the live process, not in the plist); with the auto-memory switch set, the init event's `memory_paths` shows no `auto` directory; the global settings file was read for hooks that can wait forever.
- [ ] External consequences stop for approval.
- [ ] Reject, expiry, duplicate, and failure paths were tested.
- [ ] Health, logs, disable, and stop controls exist.
- [ ] A real message succeeded after restart.
- [ ] `SETUP-STATUS.md` contains evidence and the honest current status.

## Completion report

Claude Code should end with:

```text
Current status:
Host:
Agent engine:
Telegram identity:
Allowed users and chats:
Job boundary:
Tools allowed:
Cage (tools and mode from the init event, and which proof passed):
Approval boundary:
Proof completed:
Known limits:
How to disable:
How to stop:
Next safest expansion:
```
