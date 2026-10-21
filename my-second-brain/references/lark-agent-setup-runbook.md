# Lark AI Agent Setup Runbook

Version: 1.2 (2026-10; written against Claude Code 2.1.240 and lark-cli 1.0.89)  
Audience: Business owners building their first bounded AI agent  
Outcome: An owner-only Lark bot can receive one bounded request, return a draft or approval request, survive a restart, and stop safely.

What changed in 1.2: Stage 2 names a read-only command for listing Lark CLI profiles, rule 4 says the learner runs the cage check in their own terminal, and the Stage 7 turn-limit line says what replaces it.

What changed in 1.1: a section on running headless Claude Code safely, placed before Stage 7, and new lines in Stages 4, 5, 6, 7, 10 and 11.

## Start here

Open a fresh Claude Code session inside a new, dedicated project folder. Use the guided prompt from the Builder Portal. It directs Claude Code to the public copy of this runbook.

If Claude Code cannot access the public URL, download this Markdown file, attach it to the session, then paste:

> Read this entire Markdown file first. Follow it as the setup authority. Begin with Stage 0 and stop at every human gate. Do not ask me to paste secrets into chat.

Claude Code must read this whole file before changing anything.

## Rules for Claude Code

1. Inspect the machine, Lark CLI state, and current project before proposing commands.
2. Ask one bounded question at a time.
3. Never ask the learner to paste an app secret, API key, password, tenant credential, or private token into chat.
4. Never print a secret into logs, screenshots, source code, Git history, or terminal output.
5. Pause for explicit approval before installing software, creating or changing a Lark app, granting permissions, writing outside the chosen project folder, or creating a background service.
6. Never bypass permission checks.
7. Keep the first version owner-only or limited to one test chat.
8. Filter chat, sender, and mention requirements before any model call.
9. Read every created or changed Lark resource back before claiming success.
10. Do not call the agent Running until a real Lark message succeeds after the runtime has restarted.

Create `SETUP-STATUS.md` in the project folder. Record each stage as Not started, In progress, Blocked, or Proven. Record evidence without secrets.

## The architecture you are building

```text
Lark message
    ↓
Custom app and bot identity
    ↓
Long connection event listener
    ↓
Chat, sender, and mention filters
    ↓
Bounded agent core
    ↓
One approved skill or tool
    ↓
Bot reply or approval card
    ↓
Read-back verification
```

Lark is the channel. The custom app supplies the bot identity. The runtime and bounded agent perform the work.

## Honest status ladder

Use only these labels:

1. Designed
2. Local plumbing tested
3. Channel connected
4. Agent path tested
5. Approval tested
6. Restart proven
7. Running

Never skip a label. A successful reply inside the current terminal is not Restart proven.

## Stage 0: Define one job and one boundary

Claude Code must ask for:

- The single job the agent performs.
- The human owner.
- The Lark users and chats allowed in version one.
- Whether the bot should respond only when mentioned.
- What information it may read.
- What information is explicitly excluded.
- Which skill, SOP, Method, or Playbook it follows.
- Whether it only answers, drafts, writes, sends, or deletes.
- Which actions require approval.
- What counts as proof.
- What failure looks like.
- How the owner disables and stops it.

Recommended first job: receive a question from the owner and return a draft. It should not change a Lark Base, send on behalf of a user, or update a company source of truth.

Human gate: The learner approves the written boundary before any app or runtime is created.

## Stage 1: Choose the bot pattern

Select one pattern before building:

### Pattern A: AI worker with narrow tools

The bot can reason and call a small allowlist of tools. This is powerful and carries the highest security burden.

### Pattern B: Retrieval question and answer

The runtime retrieves approved context and gives it to a model with no tools. This is the safest starting point for broad internal access.

### Pattern C: Deterministic workflow bot

Fixed code receives an event and performs a fixed action. Use this when the process does not need model judgment.

For a first AI agent, prefer Pattern B or a tightly bounded Pattern A.

Human gate: The learner chooses the pattern and explains why it matches the job.

## Stage 2: Inspect the machine and runtime

Claude Code must inspect, not assume:

- Operating system and version.
- Node.js and npm availability.
- Git availability.
- Claude Code version.
- Whether `lark-cli` is installed and authenticated.
- Existing Lark CLI profiles without exposing their secrets: `lark-cli profile list` is read-only and prints each profile's name, app ID, active flag and token status, never the App Secret.
- Whether this is an always-on desktop, a laptop, or a VPS.
- Whether the chosen folder is local and dedicated to this bot.

Do not place the project inside the learner's Second Brain. Do not give the bot unrestricted access to the Second Brain or the whole computer.

If `lark-cli` is missing, Claude Code must verify the current official installation method before proposing it. Do not rely on a copied package name or an old command.

Before generating any Lark command, Claude Code should inspect the installed CLI surface:

```bash
lark-cli --help
lark-cli event consume --help
lark-cli im +messages-send --help
```

If the installed `lark-cli` version differs from the one on this runbook's version line, read the `--help` of every command before following a command shape in this runbook.

Choose an agent engine:

### Option A: Claude Code Agent SDK or non-interactive Claude Code

Use this for a personal, owner-operated runtime when the current Claude setup supports it.

### Option B: Anthropic Messages API or Managed Agents

Use this when the bot must run as a service independent of an interactive Claude Code login. This needs an API key and may use separate platform billing.

Human gate: The learner chooses the host and engine after hearing the operational and billing implications.

## Stage 3: Create one Lark custom app

The learner completes this stage in the Lark Developer Console with Claude Code guiding one screen at a time:

1. Create a custom app for the agent.
2. Enable the bot capability.
3. Add only the event and API permissions required for the first job.
4. Create an app version and make the bot available to the chosen test users or test chat.
5. Obtain the App ID and App Secret.
6. Store the App Secret in protected storage.

One app creates one bot identity. If the company later needs separate bot identities, create separate apps and separate profiles.

The App Secret is a password. Do not paste it into Claude Code chat. Do not place it in Markdown, source code, screenshots, Git, or terminal history.

Human gate: The learner confirms the app exists, the bot is enabled, and the secret is stored. Claude Code must not ask to see the secret.

## Stage 4: Register and verify the Lark CLI profile

Claude Code should use the current Lark CLI help and official documentation as the source for exact commands. It must:

1. Confirm which tenant and app are being configured.
2. Register a named bot profile without exposing the App Secret.
3. Confirm the profile can authenticate as the bot.
4. Resolve the owner and test chat IDs using read-only operations.

   A person's `open_id` is different under every Lark app (only `union_id` is stable across apps; `chat_id` is stable too). An allowlist copied from a test app silently rejects the same person under the production app. Resolve every id under the app the bot will run as: listen for one real message under that app's profile and take the `sender_id` from the event, or use `scripts/whoami.sh <profile>` from the chat-bridge repo.

5. Record identifiers in protected configuration, not in learner-facing documentation.

Lark identities matter:

- Bot identity receives events and replies as the bot.
- User identity accesses resources available to that user.

Do not use user identity just because it has broader access. Use the identity that matches the job.

Human gate: The learner approves the resolved tenant, app, owner, and test chat before the listener begins.

## Stage 5: Prove the Lark connection without AI

Use Lark's outbound long connection for the first build. It does not require a public server, domain, or inbound webhook.

The current command shapes are:

```bash
lark-cli event consume im.message.receive_v1 --as bot
lark-cli im +messages-send --as bot
```

Claude Code must read each command's current help before adding required arguments. The first command keeps listening and emits events. The second sends a reply as the bot.

Claude Code must implement and prove:

1. Subscribe to the message-received event using the bot profile.
2. Start the event listener and wait for its ready line on stderr, `[event] ready event_key=<key>`, before reading events. Do not pass `--quiet`: it suppresses that line and the warnings about dropped events. For an unbounded `event consume`, keep the child's stdin open: stdin EOF is treated as a request to exit, so a listener spawned with a closed stdin exits at once under a service. One consumer per event key per app: a second consumer on the same app splits the events.
3. Only then ask the learner to send a test message.
4. Parse the event envelope and message content safely.
5. Reject messages outside the approved chat and sender allowlists.
6. In a group, require a bot mention before continuing.
7. For a message that passed the chat, sender and mention filters but is of a type you do not handle (sticker, image, voice, file), reply with one line naming the type. A message that failed the filters stays silent, as before; one that passed and is dropped with no reply and no log line looks exactly like a dead bot.
8. Return a static reply as the bot.

The long connection does not replay messages sent while the listener was offline. A test message sent before the ready signal is not a valid test.

Proof required:

- A real owner message reached the listener after it was ready.
- One static reply returned as the bot.
- An unapproved sender or chat did not call the agent.
- A group message without a mention did not call the agent.
- An approved sender's sticker or voice message got a reply naming the type.
- The audit log records time, event type, result, and correlation ID without secrets.

Status after proof: Channel connected.

## Stage 6: Scaffold the agent project

Claude Code should propose a small Node.js and TypeScript project after checking current supported versions and libraries:

```text
lark-agent/
  src/
    lark/
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

- Real secrets are excluded from Git.
- `.env.example` contains names only, never values.
- The runtime validates configuration without printing secret values.
- Filters run before the model.
- Logs omit sensitive message bodies by default.
- The bot has one clear disable and stop control.

For the shape of the hardened run, you may read `bridge/run-claude.mjs` in the chat-bridge repo; build the stages here, do not adopt the whole bridge.

Human gate: The learner approves dependencies and file changes before installation.

## Headless Claude Code: the cage, the clock, and the false alarms

Applies when the engine is Option A run as `claude -p` from your own runtime. Read this before the agent path stage below builds its first run. Written against Claude Code 2.1.240; on any other version, re-read `claude --help` before trusting a flag, and re-run the proof in rule 4 after every upgrade. If you use the Agent SDK instead, map each rule to its current documentation and keep rule 4 either way.

1. **The tool gate is `--tools`.** `--allowedTools` only pre-approves tools; it does not unload the rest, so `--allowedTools Read` still loads a shell and tools that can start sub-agents or schedule jobs. On 2.1.240, `claude --help` says it: `--tools ""` disables all tools. Zero tools (Pattern B): `--tools ""`. Files only (Pattern A): `--tools Read,Edit,Write,Glob,Grep`. Treat `--disallowedTools` and a settings `deny` list as a second layer, never as the gate.
2. **Put `--permission-mode` on the command line of every run.** On 2.1.240 the values `claude --help` lists are `acceptEdits`, `auto`, `bypassPermissions`, `manual`, `dontAsk` and `plan`. Zero-tool bot: `manual`. Files-only bot: `acceptEdits`. Note that with `manual` the init event (rule 4) reports `permissionMode: "default"`: the cage check compares against the value the init event reports (the table in rule 4), not against the word you typed. Without the flag the run inherits the machine's global default, which on a developer's own machine is often bypass. Never `bypassPermissions`, never `--dangerously-skip-permissions`.
3. **Add `--strict-mcp-config` and pass no `--mcp-config`.** The run then loads zero MCP servers, so the bot cannot reach the integrations configured for your interactive sessions.
4. **Check the cage from the runtime, every run, never from the model.** Run with `--output-format stream-json --verbose` and parse one JSON event per line. Find the event with `type: "system"` and `subtype: "init"` (it is not always the first line). Its `tools` (sorted) and `permissionMode` must match the expected values for the cage you built, exactly; on any mismatch kill the run, log `CAGE BREACH`, and tell the chat. A result with no init event is a breach too. Expected on 2.1.240: zero-tool cage, `tools` `[]` and `permissionMode` `default` (what `--permission-mode manual` reports); files-only cage, `tools` `Edit,Glob,Grep,Read,Write` and `permissionMode` `acceptEdits`. Verify these once on your installed version before you hard-code them. The learner runs each check in their own terminal, not Claude Code from its shell tool (rule 6 says why), and Claude Code reads the output the learner pastes or saves to a file: the chat-bridge repo's `scripts/probe-claude.sh` checks the files-only pair only (its expected tools and mode are fixed in the script); for the zero-tool pair, the learner runs the same `claude -p` command with `--tools "" --permission-mode manual`, and Claude Code reads the init event in that output. Also read the init event's `memory_paths` (rule 5): with `CLAUDE_CODE_DISABLE_AUTO_MEMORY` set, no `auto` directory should appear in it. Log one line per run, `cage ok: tools=<sorted list> mode=<mode>`, and one line per entry in the result's `permission_denials`, `denied: <tool> <input>`. Do not ask the model what tools it has: a zero-tool model asked to run a command will write a fake tool call in prose. The proof depends on which cage you built, and you never widen `--tools` to make a proof pass:
   - **Zero-tool cage** (`--tools ""`): the init event's `tools` is `[]`, and a successful result has `num_turns` equal to 1 and `permission_denials` equal to `[]`. Breach condition: `num_turns` greater than 1, or `permission_denials` not empty; either means the model tried to act, log it loudly. A result with `is_error` true and `num_turns` 0 is not a breach: it is a run that never got going (a dead `--resume`, rule 9, or a login problem, rule 6), handle those first. There is no `denied:` line to look for here: a run with no tools has nothing to deny.
   - **Files-only cage**: ask the bot to read `/etc/hosts`; the log must show `denied: Read /etc/hosts` and the reply no file contents. A refusal with no `denied:` line is not a pass, the model never tried; ask again more directly. Also expect a write outside the working directory, and a write to `.claude/settings.local.json` inside it, to be denied.
5. **Spawn it right.** Absolute path to `claude` (`which -a claude`, the line starting with `/`); the message as one argv element, never a shell string; `cwd` pinned to the project folder; `detached: true` so a stop can kill the whole process group; a scrubbed environment built by hand, carrying at least `HOME PATH USER SHELL TERM LANG` plus the two switches below, and nothing inherited from the parent. `USER` and `SHELL` are not optional: without them, on macOS, `claude -p` cannot find your login in the keychain and every answer becomes `Failed to authenticate: OAuth session expired and could not be refreshed`, while your login is fine and `claude login` changes nothing. **Keep your own instruction files out of the bot's runs.** A headless run loads the same instruction files your interactive sessions do: your user-level `CLAUDE.md` and your Claude Code auto-memory. Whatever is in them shapes every reply, and anyone who can message the bot can ask it to repeat them. Set `CLAUDE_CODE_DISABLE_CLAUDE_MDS=1` and `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` in the child's environment (both names are present in the 2.1.240 binary; prove the switches are on the live child with `ps eww -p <pid>`, which must show both variables; with the auto-memory switch set, the init event's `memory_paths` should show no `auto` directory). If you followed the chat-bridge approval-card chapter, which tells you to write the draft format into the working directory's `CLAUDE.md`, put that format into `--append-system-prompt` instead, and put the bot's own instructions in the prompt or an `--append-system-prompt` instead. `--setting-sources` (2.1.240 lists `user`, `project`, `local`) is a second lever: `--setting-sources user` keeps the working directory's project settings and `.mcp.json` out of the run, but it also drops any project-level hooks and permission rules you meant to keep; it decides which `CLAUDE.md` files load, but not auto-memory; the two switches above remain the way to keep both out.
6. **Four false alarms while testing, each one looks like a broken bot.** (a) A process started from an SSH session cannot reach the login keychain and reports "Not logged in". (b) Running `claude -p` from inside an AI agent's shell tool with its sandbox on, Claude Code's own Bash tool included, gives the same false "OAuth session expired". (c) A "quick load check" that does `import()` of the bot file runs the bot: a second consumer on the same bot app, competing for the same events. Check that a file loads with `node --check`, never with `import()`. (d) The foreground test is therefore the learner's job: the learner starts the bot in their own terminal window; Claude Code reads the log file, asks the learner what appeared in the chat (it cannot read the chat itself), and does not start the bot from its own shell tool. One probe settles login questions: run `claude -p` once with a clean env that includes `USER` and `SHELL`, from a normal terminal, not over SSH, not from an agent shell. `is_error: false` means your runtime's env was the problem; an error means log in again.
7. **Your global `~/.claude/settings.json` applies to headless runs too, hooks included**, and a `--settings` file merges with it rather than replacing it. A hook that never returns under a background service (one that plays a sound or waits for a prompt) holds the run forever: the answer is written within seconds and no `result` event ever arrives, so the bot looks silent. Read the global file line by line before creating the service; when a run hangs, `pgrep -P <claude pid>` shows the child that never exited. Fix it in the global file; `--bare` is not an escape, it also skips your login.
8. **Time limits: a silence watchdog plus a hard cap, never one fixed timeout.** Reset the watchdog on every stream event, pause it while a tool call is open, and kill when nothing has happened for the idle limit; keep a hard cap behind it for a tool that never returns. A fixed timeout is wrong in both directions: it kills a healthy long job and makes you wait the full time on a hung one. Kill the whole process group (`process.kill(-pid)`), then force the pipes shut: killing only `claude` leaves its hooks and shells holding the pipeline. Tell the chat plainly when a run was stopped and why. Reference defaults in the chat-bridge repo: 5 minutes idle, 45 minutes cap.
9. **Sessions.** If you keep per-sender memory with `--resume`, store a session id only from a run whose result has `is_error: false`. When a stored session is gone, `--resume` prints `No conversation found with session ID` and returns an error with `num_turns` 0: retry that message once without `--resume`, drop the dead id, and never store it again. Otherwise that one sender is stuck on an error for every message until the file is cleared by hand. Give the owner a `/new` command that resets the thread.
10. **Busy is not silent.** If a message arrives while a run is in progress, acknowledge it at once ("Got it, 1 task ahead of yours"). Bound the queue, and when a message is refused, say which limit it hit. Every limit (idle, cap, queue size, message length, send timeout, retries) is a named constant in one place.

Reference for these rules, with a runnable probe for the files-only cage (`scripts/probe-claude.sh`), the proofs per cage (`docs/proof.md`), the full list of failures that only show up under a background service (`docs/gotchas.md`), and a reference run (`bridge/run-claude.mjs`): https://github.com/breakthrough-edu/claude-code-chat-bridge. Read it for shape; build the stages in this runbook.

## Stage 7: Connect one bounded agent path

Build the run exactly as the section "Headless Claude Code" above says: the tool gate, the permission mode, zero MCP servers, and the cage check on every run are not optional.

The agent core needs:

- A short system prompt that names the job and finish line.
- The minimum approved context.
- One skill, SOP, Method, or Playbook reference.
- A tool set declared with `--tools` (empty for Pattern B), checked from the init event on every run.
- No turn limit to set: `claude --help` on 2.1.240 lists no `--max-turns`. Bound each run with the silence watchdog and hard cap of rule 8 in the section above, and use `--max-budget-usd` (print mode only) as an extra layer, not as the gate.
- A time or cost limit appropriate to the engine.
- Structured output with a result, evidence, status, and proposed next action.

Send replies with `--markdown`, not `--text`: the model writes markdown, and as plain text every `**bold**` and backtick arrives as a literal symbol on the phone. Before the send, neutralise image links in the reply (inline images, reference-style images and `<img>` tags become plain text): the markdown send resolves image URLs, which is a fetch from your machine to an address that came out of the model, and in a group anyone can steer the model into writing one.

First test:

1. Owner sends one approved request.
2. Chat, sender, and mention filters pass.
3. Agent receives only approved context.
4. Agent produces a draft.
5. Bot replies with the draft.
6. No company system changes.

Status after proof: Agent path tested.

## Stage 8: Add the approval gate

Classify every possible result:

- Answer only: may return immediately.
- Draft only: may return immediately and remain unsent.
- Internal reversible write: requires the boundary defined in Stage 0.
- External, financial, sensitive, or irreversible action: requires explicit human approval.

An interactive Lark card can present the exact proposed action with Approve and Reject controls. Approval state must be tied to the requesting owner, exact action, and expiry time.

For card callbacks, Claude Code must account for content that may arrive as a JSON string and must prevent repeated execution. Use a take-once approval record. Restore it only when a failed action is safe to retry.

Claude Code must test:

- Reject performs no action.
- Approve performs only the previewed action.
- Repeated clicks do not repeat the action.
- Expired approval cannot execute.
- Failure returns a clear signal.

Status after proof: Approval tested.

## Stage 9: Optional Lark Base access

Skip this stage unless the job truly requires Base data.

For every table involved, name its role:

- Source: Lark owns the official record.
- Mirror: Lark reads a record owned elsewhere.
- Intake: Lark collects a request, not the master record.
- Snapshot: a dated copy, not live truth.

Rules:

- Default to read-only access.
- Do not write to a Mirror.
- Fetch the Base schema before coding field names.
- Resolve records by stable IDs, not display text alone.
- After every create or update, read the record back and compare intended fields.
- Prevent duplicate writes with an idempotency key or equivalent guard.
- Keep personal and sensitive fields outside the agent unless the job requires them and the owner approves.

No write counts as successful until read-back verification passes.

## Stage 10: Add operational controls

Before background operation, implement:

- A health signal for the event listener and agent path.
- Rate limits and abuse protection.
- Timeouts and bounded retries.
- Duplicate-event protection keyed on `message_id`, not `event_id` (the same message can be delivered again under a new `event_id`); card taps have no message of their own and are keyed on their event id. Persist the handled ids to disk, bounded, written before you act: an in-memory set is empty after every restart, which is when a redelivery is most likely.
- An append-only audit trail without secrets or unnecessary message bodies.
- A visible disable switch.
- A clean stop path.
- A failure notification to the owner.
- Secret rotation instructions.

The owner must be able to stop the service without asking the agent itself.

## Stage 11: Create the background service

Only after foreground tests pass, Claude Code may propose a persistent service:

- macOS: a user-level launch service.
- Linux or VPS: a restricted system service.
- Another managed runtime: only if the learner chooses it and understands cost, secrets, and logs.

Use absolute Node, Lark CLI, and project paths. Explicitly set the runtime environment. Headless services may not inherit the terminal PATH or interactive input. Create the bot profile before creating the service.

On macOS: keep everything the service itself opens (its working directory, its log paths, the file it executes) outside the protected folders: `~/Documents`, `~/Desktop`, `~/Downloads` and cloud-synced folders. A service that points into them works every time you start it by hand and refuses to start after the first cold reboot, with exit code 78 and an empty log. A folder such as `~/Scripts/<bot>/` is the usual choice. The program the service starts can still read protected folders, on one condition: Full Disk Access is granted to that program's binary (the `node` you point the service at) on that machine. The grant is per binary and per machine, it does not sync, and after granting or changing it the job must be unloaded and loaded again (`bootout`, then `bootstrap`); a `kickstart` does not re-evaluate it.

Before this stage, answer the eight questions every unattended worker answers (Reads, Writes, Identity, Limits, Stop, Proof, Heartbeat, Rollback); a question you cannot answer is a hole to name, not a blank. The worksheet is `EIGHT-CELLS.md` in the chat-bridge repo; the Builder Portal's Explore page has the Resident Workers Playbook that explains each one.

Do not enable endless restart loops. Add a retry ceiling and visible failure signal.

Human gate: The learner approves the service location, permissions, start behavior, stop method, and logs.

## Stage 12: Restart and recovery proof

Prove the runtime can restart from saved files:

1. Stop the listener through its documented control.
2. Start it through the intended service path.
3. Wait for the ready signal.
4. Send a fresh owner message.
5. Confirm all filters and approval rules still apply.
6. Confirm old pending approvals cannot execute after restart.
7. Confirm the audit trail shows the new run.

Status after proof: Restart proven.

## Stage 13: Decide whether to broaden access

Do not add a broad team audience unless all earlier stages pass.

If access is broadened:

- Use explicit user and chat allowlists.
- Require mentions in groups.
- Keep sensitive actions owner-only.
- Test an unapproved user, unapproved chat, and missing mention.
- Document who owns access changes.
- Prefer a zero-tool retrieval agent for a broad reader audience.

Only repeated real use with a current owner justifies Running.

## Optional extensions after the core path works

These are not part of the first completion:

- Voice input with explicit transcription controls.
- Images and files with type and size limits.
- Scheduled pushes with owner-controlled subscriptions.
- Lark Base writes with read-back verification.
- Rich interactive cards.
- Multiple bot identities through separate apps and profiles.
- Read-only access to part of your Second Brain, as a second build after Restart proven, and only once the exclusions are enforced by the runtime, not just written down. Shape: working directory set to a folder of the vault the bot may read (a bot-specific subfolder if that is all the job needs, the vault itself only if the job needs it), `--tools Read,Glob` (no `Grep`: a `Read` deny rule is enforced on `Read` and only best-effort on the search tools, so leave `Grep` out, or prove every excluded folder against `Grep` as well), `--permission-mode manual`, owner-only, the cage logged on every run, and a `permissions.deny` list in the bot's own `--settings` file with one rule per excluded folder, written as a path pattern such as `Read(./<private-folder>/**)` relative to the working directory (or `Read(~/path/**)`, `Read(//absolute/**)`), proved by a `denied: Read <path>` line when you ask the bot to read a file in each excluded folder, and by a `Glob` request on the same folder returning nothing. Accept the consequences before you build it: with the rule 5 switches on, neither the vault's `CLAUDE.md` nor a parent folder's `CLAUDE.md` loads as instructions; if the bot needs the vault's own guidance, have it read those files with `Read`. The vault's project settings and hooks still load from that working directory, with the global settings file merged on top; if the vault sits under a protected folder, the service's binary needs Full Disk Access (macOS); and everything not denied is readable by whoever can message the bot, which is why it stays owner-only. A bot that can also write to the vault is a third build, through the approval gate.

Add one extension at a time and repeat the permission, failure, restart, and stop tests.

## Final verification checklist

- [ ] One job, owner, pattern, and test chat are written down.
- [ ] App Secret and model credentials never entered chat, source, logs, screenshots, or Git.
- [ ] The listener proves ready before the test message is sent.
- [ ] Chat, sender, and mention filters run before the model.
- [ ] Bot and user identities are used deliberately.
- [ ] The agent sees only approved context.
- [ ] Tools and Lark permissions are narrow.
- [ ] `--tools` and `--permission-mode` are on the command line of every headless run; `--strict-mcp-config` with no `--mcp-config`.
- [ ] Every run logs `cage ok: tools=... mode=...` from the init event, and `--tools` was never widened to make a proof pass.
- [ ] Cage proof for the cage built: zero-tool, every successful result `num_turns` 1 and `permission_denials` `[]`; files-only, a request to read `/etc/hosts` logged `denied: Read /etc/hosts`.
- [ ] The child's live environment (`ps eww -p <pid>`) carries `USER` and `SHELL` and the two `CLAUDE_CODE_DISABLE_*` switches (proved on the live process, not in the plist); with the auto-memory switch set, the init event's `memory_paths` shows no `auto` directory; the global settings file was read for hooks that can wait forever.
- [ ] Handled message ids are persisted on disk, keyed on `message_id`.
- [ ] External consequences stop for approval.
- [ ] Every Lark write is read back.
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
Lark app and bot identity:
Allowed users and chats:
Mention requirement:
Bot pattern:
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
