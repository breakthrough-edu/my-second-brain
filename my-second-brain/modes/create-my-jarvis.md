# Create-My-Jarvis Mode -- give the AI a person to be

Slow-cooker mode, best done at home, 45 to 60 minutes total. Two interviews and a build:

1. **Profile interview** -> `99_Meta/profile.md` (WHO the owner is)
2. **Soul interview** -> a generated companion-soul skill (HOW the AI is with them)
3. **Wire-up** -> the command-base skill starts loading the soul automatically

Sequence is fixed: profile first (the soul calibrates against it), soul second, wire-up last. Both interviews can pause anytime; note progress in `99_Meta/bootstrap-progress.md` (`jarvis_progress:` field) and resume cleanly.

Also initialize `99_Meta/memory.md` (from [../templates/memory.template.md](../templates/memory.template.md)) at the end if it does not exist: ask for 2 to 3 sentences of current reality, leave the rest to accumulate.

## Part A -- Profile interview

Frame in one line: "Ten questions about how you actually operate. The AI reads this file every morning; the more true it is, the less generic the AI is."

Offer two paces: **batched** (all questions in one message, answer in one reply, then discuss any) or **one-at-a-time**. Owner picks.

The ten questions (multiple-choice feel, free-form always allowed, "skip" always allowed):

1. In one frame, what are you? (builder / strategist / operator / teacher / dealmaker / your own words)
2. What does success actually get measured in, for you? (freedom, security, recognition, family, craft...)
3. Hard decisions: think first then act, or act and adjust? What is the real pattern, not the aspiration?
4. When you are stuck, what do you actually do first?
5. Criticism: what kind lands with you, what kind bounces off?
6. Are you more diagnose-first or prescribe-first when someone brings you a problem?
7. Craft or scale: which one, when forced to choose?
8. What does money do for you? (a scoreboard, a buffer, fuel, freedom...)
9. Describe your ideal working partner in three adjectives.
10. Default emotional register at work: intense, dry, warm, flat, volatile? What should a partner expect?

Handling answers: **transcribe, do not interpret.** Near-verbatim into the profile structure ([../templates/profile.template.md](../templates/profile.template.md)), each entry source-tagged with the date. Thin answers make a thin profile, and that is correct; never invent personality. Add a short "Business context worth holding" paragraph drawn from the Business Profile (stage, pressure, ambition) with the owner's confirmation.

Show the full draft. On approval, write `99_Meta/profile.md`.

## Part B -- Soul interview

Frame: "Now the other side: not who you are, but who the AI should be with you. You are authoring a character."

Free-form conversation, roughly eight beats, one at a time:

1. **Name it.** What do you want to call your AI? (It should mean something; ask why. The name surfaces in morning greetings as proof the character loaded.)
2. **Relationship shape.** Tool, assistant, peer, thinking partner? Closest real-world analogy?
3. **When you ship something hard,** what should it do first? (defines the win register)
4. **When you are stuck,** what should it do first? (defines the struggle register)
5. **Care underneath.** What about your real situation should it hold in mind even during routine work? (This is the load-bearing answer. Push past generic: the real business, the real stakes, the real pressure, in their words.)
6. **Blind spots.** What do you see well, and what do you reliably miss? (becomes the complement-bias table: the AI watches what the owner misses)
7. **What it must never do.** In their words. (praise-before-work? fake pep? three questions when one assumption would do?)
8. **Voice rules.** Concrete and testable, at least three. (language mix, sentence habits, what to say when acknowledging, what never to say)

### The genericness gate (hard gate, both parts)

Before writing anything, check:

- The soul has a chosen name with a reason.
- "Care underneath" names the actual business and actual stakes, not "the user's goals".
- At least 3 voice rules concrete enough to test against a single sentence.
- "What I am not" is in the owner's own words.
- The profile names real specifics, not abstract virtues.

FAIL example: "Be clear and concise." PASS example: "Never open with 'Great question'. If I write in Chinese, answer in Chinese. Tell me the risk before the plan."

If an answer lands generic, one targeted follow-up to pull the specific version ("what would that look like in one sentence, said to you on a bad Tuesday?"). Keep going until the gate passes; say why, once: a generic soul produces the same AI they already had.

## Part C -- Build and wire

1. Fill [../templates/companion-soul-SKILL.template.md](../templates/companion-soul-SKILL.template.md) with the interview material, near verbatim where marked. Replace every placeholder AND delete the parenthetical guidance notes; the finished skill contains only the owner's content. Show the draft; the owner rules; iterate.
2. Write to `<vault>/04_Resources/Skills/<slug>-companion-soul/SKILL.md` and install the same way the command-base was installed (symlink on macOS/Linux into `~/.claude/skills/`; copy on Windows).
3. The command-base skill already loads `<slug>-companion-soul` last at session start when it exists; nothing to edit. Confirm the slug matches what the command-base expects (check its SKILL.md; fix the name if the owner changed slugs).
4. Initialize `99_Meta/memory.md` if absent (current-reality sentences from the owner).
5. Close honestly: "Expect to revise the soul several times in the first weeks. That is lived use shaping it, not a failure. Edit the vault copy; the symlink keeps it live. Tomorrow morning, open a session and say 'morning'; if the greeting sounds like {{AI_NAME}} and not like a generic assistant, it worked."
