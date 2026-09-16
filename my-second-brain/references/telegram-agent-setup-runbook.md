# Telegram AI Agent Setup Runbook

Version: 1.0  
Audience: Business owners building their first bounded AI agent  
Outcome: An owner-only Telegram bot can receive one bounded request, return a draft or approval request, survive a restart, and stop safely.

## Start here

Open a fresh Claude Code session inside a new, dedicated project folder. Use the guided prompt from the Student Portal. It directs Claude Code to the public copy of this runbook.

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
3. The update offset advances so the same message is not handled twice.
4. The sender user ID and chat ID are captured for allowlisting without publishing them.
5. The bot returns a static reply.
6. An unapproved sender is rejected before any model call.

Telegram keeps pending updates for a limited period. Long polling and webhooks are mutually exclusive. Do not configure a webhook during this first build.

Proof required:

- A real owner message reached the local runtime.
- One static reply returned to the same chat.
- A rejected sender test did not call the agent.
- The audit log records time, event type, result, and correlation ID without secrets.

Status after proof: Channel connected.

## Stage 5: Connect one bounded agent path

The agent core needs:

- A short system prompt that names the job and finish line.
- The minimum context required for the job.
- One skill, SOP, Method, or Playbook reference.
- A narrow tool allowlist.
- A maximum turn limit.
- A time or cost limit appropriate to the chosen engine.
- Structured output with a result, evidence, status, and proposed next action.

If Claude Code is used non-interactively, review current support for controls such as `--allowedTools`, `--max-turns`, `--max-budget-usd`, structured output, and permission callbacks. Do not copy old flags without checking the installed version.

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

Human gate: The learner approves creation of the service after reviewing its location, permissions, start behavior, stop method, and logs.

## Stage 9: Restart and recovery proof

Prove the runtime can restart from saved files:

1. Stop the process through its documented control.
2. Start it through the intended service path.
3. Send a fresh owner message.
4. Confirm the sender filter, agent path, and approval state still behave correctly.
5. Confirm old pending approvals do not execute after restart.
6. Confirm the audit trail shows the new run.

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

## Final verification checklist

- [ ] One job and one owner are written down.
- [ ] The bot token never entered chat, source, logs, screenshots, or Git.
- [ ] Sender and chat filters run before the model.
- [ ] The agent sees only the minimum context.
- [ ] Tools are narrow and explicit.
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
Approval boundary:
Proof completed:
Known limits:
How to disable:
How to stop:
Next safest expansion:
```
