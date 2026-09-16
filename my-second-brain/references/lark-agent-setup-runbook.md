# Lark AI Agent Setup Runbook

Version: 1.0  
Audience: Business owners building their first bounded AI agent  
Outcome: An owner-only Lark bot can receive one bounded request, return a draft or approval request, survive a restart, and stop safely.

## Start here

Open a fresh Claude Code session inside a new, dedicated project folder. Use the guided prompt from the Student Portal. It directs Claude Code to the public copy of this runbook.

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
- Existing Lark CLI profiles without exposing their secrets.
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
2. Start the event listener and wait until it reports ready or connected.
3. Only then ask the learner to send a test message.
4. Parse the event envelope and message content safely.
5. Reject messages outside the approved chat and sender allowlists.
6. In a group, require a bot mention before continuing.
7. Return a static reply as the bot.

The long connection does not replay messages sent while the listener was offline. A test message sent before the ready signal is not a valid test.

Proof required:

- A real owner message reached the listener after it was ready.
- One static reply returned as the bot.
- An unapproved sender or chat did not call the agent.
- A group message without a mention did not call the agent.
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

Human gate: The learner approves dependencies and file changes before installation.

## Stage 7: Connect one bounded agent path

The agent core needs:

- A short system prompt that names the job and finish line.
- The minimum approved context.
- One skill, SOP, Method, or Playbook reference.
- A narrow tool allowlist.
- A maximum turn limit.
- A time or cost limit appropriate to the engine.
- Structured output with a result, evidence, status, and proposed next action.

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
- Duplicate-event protection.
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

Add one extension at a time and repeat the permission, failure, restart, and stop tests.

## Final verification checklist

- [ ] One job, owner, pattern, and test chat are written down.
- [ ] App Secret and model credentials never entered chat, source, logs, screenshots, or Git.
- [ ] The listener proves ready before the test message is sent.
- [ ] Chat, sender, and mention filters run before the model.
- [ ] Bot and user identities are used deliberately.
- [ ] The agent sees only approved context.
- [ ] Tools and Lark permissions are narrow.
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
Approval boundary:
Proof completed:
Known limits:
How to disable:
How to stop:
Next safest expansion:
```
