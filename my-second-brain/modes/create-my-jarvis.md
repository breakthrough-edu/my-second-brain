# Create-My-Jarvis Mode: give the AI a person to be

Slow-cooker mode, best done at home. Two interviews and a build:

1. **Profile interview** -> `99_Meta/profile.md` (WHO the owner is)
2. **Soul interview** -> a generated companion-soul skill (HOW the AI is with them)
3. **Wire-up** -> the command-base skill starts loading the soul automatically

Sequence is fixed: profile first (the soul calibrates against it), soul second, wire-up last. Everything can pause anytime; record progress in `99_Meta/bootstrap-progress.md` (`jarvis_progress:`, shape below) and resume cleanly.

`99_Meta/memory.md` is scaffolded at setup, so it normally already exists. At the end of this mode, fill its Current reality section with 2 to 3 sentences from the owner if it is still empty. (Backstop: if the file is missing, create it from [../templates/memory.template.md](../templates/memory.template.md) first.)

## Two tiers: light and deep

Ask once, at the top, and let the owner pick. ⛔ Do not default to deep and do not talk them into it: the deep tier asks about where they came from, who they carry and where their lines are, and an owner who agreed to that because it sounded like the thorough option will answer it carefully and resent it later.

| | **Light** | **Deep** |
|---|---|---|
| What it is | the ten questions in Part A, then the soul interview | light, plus three sittings and a taste module |
| Time | 45 to 60 minutes, one sitting | 2 to 3 hours, and **not in one evening** |
| Profile sections filled | seven | ten (the three deep-only ones fill here and only here) |
| What the soul gets | a calibrated assistant that sounds like it knows them | a character with roots, a line it will not cross, and a voice with taste in it |

Say it in one line and stop: "Light gets you an AI that stops being generic. Deep gets you one that sounds like someone who has known you a while. Deep is three more conversations, best spread over a few days."

⭐ **Light is a complete product, not a trial.** An owner who takes light and never comes back has the thing this mode exists to give. **And light is reversible:** the three deep-only profile sections stay in the file, empty and labelled, so "let's do the deep ones" is a real sentence they can say in six months. ⛔ Never delete an empty deep section to make a light profile look finished.

## The five mechanisms this mode runs on

These are the moving parts. Everything below refers back to them by name.

### 1. Follow-up protocol

**At most two follow-ups on one answer, then take what is there.**

A follow-up is not the same question again in different words. It is a request for **one concrete instance**: a moment, a sentence, a person, a number. "What would that look like in one sentence, said to you on a bad Tuesday?" is a follow-up. "Can you say more about that?" is the same question wearing a hat.

- **First follow-up:** ask for the instance.
- **Second follow-up:** offer a wrong guess and let them correct it. People who cannot produce a description will readily fix one. "So something like: you would rather be told the number is bad than be asked how you feel about it?"
- **Then stop.** Write the thin answer thin. ⛔ A thin profile is correct and honest; an invented one is neither, and the owner cannot tell which they are reading six months later.

⚠️ **Three follow-ups on one question is the signal to change the question, not to push harder.** Something in it is not landing, and pushing turns an interview into an interrogation with an hour still to run.

### 2. Distillation and adjudication

**Transcribe by default; interpret only where a section demands it, and then show the sentence.**

Answers go into the profile near-verbatim, source-tagged with the date. Where a section genuinely needs synthesis (Core identity, Business context worth holding), write the synthesis as **one sentence**, show it back with the raw material beside it, and ask: "Is that yours?"

**Adjudication is the owner's, absolutely.** What they cut stays cut, and ⛔ it does not come back in another section wearing different words. What they correct is used as corrected, even where the raw material seemed to say otherwise; ⛔ do not preserve your reading in a parenthesis. ⭐ **This is the rule that makes the file safe to be honest in**, and an owner who catches one smuggled-back line will never give a real answer again.

### 3. The deep-only gate

The three sittings and the taste module are the only source for the profile's **Worldview**, **Life architecture** and **Relationships** sections and for the deep half of the soul's care-underneath, never-do and voice.

- ⛔ **Never enter a deep sitting without the consent card below having been shown and answered.**
- ⛔ **Never fill a deep-only section from a light run**, and never fill one by inference from the ten questions. A section filled by inference reads exactly like one filled by the owner, and nothing downstream can tell them apart.
- **If the owner stops mid-sitting**, that is a complete answer. Write what exists, mark the sitting `stopped` in `jarvis_progress:`, and do not circle back to it later in the session.

### 4. The consent card

Shown **once**, before the first deep sitting, as its own message. Not folded into a question and not summarized. Five things, plainly:

1. **What gets asked:** where you came from, who is in the room when you decide, and where your lines are.
2. **Where it lands:** `99_Meta/profile.md` in this vault, in your own words, on your own disk.
3. **Who reads it:** every future session, at the start, automatically. That is the point of it, and it is also the whole risk.
4. **What stays out, whatever you say:** health specifics, family intimacy, and anyone else's private business. Those belong in private area notes, not in the file that loads into every conversation. ⛔ This holds even when the owner offers them.
5. **How to undo it:** open the file and delete the line. It is markdown, it is theirs, and nothing re-adds it.

Then one question, and wait for the word: "Want to go ahead?" ⛔ A shrug is not a yes. ⛔ Do not re-ask later in the session if the answer was no; offer it again another day or not at all.

### 5. The red-line pass

**The last thing before anything is written.** Read the full draft back (or hand it over to read), and ask exactly one question:

> "Is there a line in here you would not want read out in a session six months from now, with someone looking over your shoulder?"

Cut whatever they name, immediately, without asking why and without arguing for it. ⛔ Do not say it is useful, do not offer to soften it, do not move it to another section. ⭐ **The point is that the answer costs them nothing**, which is the only reason the question gets a true answer at all.

Run it over the profile before writing `profile.md`, and again over the soul draft before writing the skill.

## Progress and resuming

`jarvis_progress:` in `99_Meta/bootstrap-progress.md` is **one inline mapping with a substate per stage**, not a single value. Setup does not write it; this mode creates it on first run.

```yaml
jarvis_progress: {tier: deep, ten_questions: done, deep_roots: done, deep_relationships: pending, deep_boundaries: pending, taste: pending, profile_written: pending, soul_beats: pending, rehearsal: pending, wired: pending}
```

- `tier:` is `light` or `deep`, set the moment the owner picks. On `light`, the four deep keys are written once as `skipped` and never revisited.
- Every other key is `pending` / `done` / `skipped` / `stopped`. `stopped` is a deep sitting the owner ended early and it is **not** an invitation to resume it; treat it as done unless they raise it.
- ⛔ **Update the key the moment a stage ends, not at the end of the session.** A single value could only ever say "somewhere in the middle", and this mode is designed to be interrupted.
- Resuming: read the mapping, say in one line what is already done, and start at the first `pending`. ⛔ Never re-run a `done` stage to "check it is still right"; the owner answered once.

## Part A: Profile interview

Frame in one line: "Ten questions about how you actually operate. The AI reads this file every morning; the more true it is, the less generic the AI is."

Offer two paces: **batched** (all questions in one message, answer in one reply, then discuss any) or **one-at-a-time**. Owner picks.

### The ten questions (both tiers)

Multiple-choice feel, free-form always allowed, "skip" always allowed:

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

Handling answers: **transcribe, do not interpret** (mechanism 2). Near-verbatim into the profile structure ([../templates/profile.template.md](../templates/profile.template.md)), each entry source-tagged with the date. Thin answers make a thin profile, and that is correct; never invent personality. Add a short "Business context worth holding" paragraph drawn from the Business Profile (stage, pressure, ambition) with the owner's confirmation.

**Light tier stops here.** Run the red-line pass, show the full draft, and on approval fill `99_Meta/profile.md`, leaving the three deep-only sections present and empty. ⛔ **That file already exists, scaffolded empty. Fill its sections; never replace the file.** The weekly distillation lands graduated lines in it, and those were approved once already.

### Deep: three sittings and a taste module

Consent card first (mechanism 4). Then three conversations, best on different days, each 20 to 30 minutes. They are conversations, not questionnaires: the questions below are openings, and the follow-up protocol (mechanism 1) does the rest.

**Sitting 1 · Where you came from** -> profile **Worldview**, and the soul's **care-underneath**.

- What did the people who raised you do for money, and what did you take from watching that?
- What is the thing you decided you would never be?
- What do you believe about how this business works that most people in your trade would argue with?
- When it has gone badly, what has it usually been?

⭐ **This is the load-bearing sitting.** An owner asked directly what the AI should hold in mind produces a mission statement; the same owner talking about the road that got them here produces the actual thing, and it is usually in one sentence they say quickly and move past. Catch that sentence.

**Sitting 2 · Who you carry** -> profile **Relationships**.

- Who is in the room when you make a hard call, even when they are not in the room?
- Whose opinion actually changes your mind, and whose do you hear out and then ignore?
- Who is depending on this working?
- Is there anyone you are trying to prove something to?

⚠️ Roles and their weight, not gossip, and ⛔ nothing about anyone's private business. If an answer starts going somewhere personal about a third party, say so in one line and move on.

**Sitting 3 · Boundaries and dilemmas** -> profile **Life architecture**, and the soul's **never-do**.

- What is the work FOR? What is it not allowed to cost?
- Tell me about a time someone in a position of trust handled you badly. What exactly did they do?
- What trade-off have you already settled and do not want reopened?
- What dilemma have you never settled and still argue with yourself about?

⭐ **The second question is the one that produces the never-do list.** Asked "what should it never do", owners produce etiquette (do not be rude, do not waffle). Asked about the adviser who talked over them or the partner who buried the bad number, they produce the actual line, in the actual words, and that is what goes in the soul.

**The taste module** -> the soul's **voice**.

Not about them at all, which is why it works. Three prompts, and collect the exact wording:

- Show me a piece of writing you think is sharp. What makes it sharp?
- What kind of writing makes you close the tab?
- Is there a word or an opener you cannot stand?

⭐ **Taste is stated as a judgment about someone else, so it comes out unguarded and specific**, and it transfers straight into testable voice rules and into the anti-vocabulary list. This module is short, ten minutes, and it is the highest-yield ten minutes in the deep tier.

**Then:** red-line pass over everything (mechanism 5), show the full draft, and on approval fill `99_Meta/profile.md` (same rule as the light tier: fill it, ⛔ never replace it).

## What the two tiers actually produce

An anonymized composite, so the difference is visible rather than asserted. Same owner, same slot in the soul (`care-underneath`), two tiers.

**Light.** Beat 5 of the soul interview, "what should it hold in mind":

> **Owner:** "That the shop is growing and I do not want it to get sloppy."
>
> **What lands in care-underneath:** "The shop is growing and quality is the thing at risk. Hold that in routine work, not just when quality comes up."

That is a real gain over a generic assistant. It is one layer: a thing at risk.

**Deep.** Same owner, sitting 1, twenty minutes in, talking about their father's shop:

> **Owner:** "He kept it perfect and it closed anyway. Everyone said what a shame, and then they went to the place with the parking. So I do not actually believe good work protects you. I think it is the price of entry and then you still have to be found."
>
> **What lands in care-underneath:** "Quality is the price of entry, not the protection. He watched a perfect shop close because nobody could park, so a conversation that treats craft as the answer will feel naive to him and he will stop bringing you the real question. Hold both: the standard is not negotiable AND it is not sufficient. What he is actually afraid of is doing everything right and being invisible."

Three layers instead of one: the belief, where the belief came from, and what it means for how to talk to him. ⛔ **The difference is not length.** A longer light answer would still be one layer, and no amount of follow-up on beat 5 reaches the second and third, because beat 5 does not ask about the road.

## Part B: Soul interview

Frame: "Now the other side: not who you are, but who the AI should be with you. You are authoring a character."

### First half: the eight beats

Free-form conversation, one at a time:

1. **Name it.** What do you want to call your AI? (It should mean something; ask why. The name surfaces in morning greetings as proof the character loaded.)
2. **Relationship shape.** Tool, assistant, peer, thinking partner? Closest real-world analogy?
3. **When you ship something hard,** what should it do first? (defines the win register)
4. **When you are stuck,** what should it do first? (defines the struggle register)
5. **Care underneath.** What about your real situation should it hold in mind even during routine work? (On a deep run this is already answered by sitting 1: read the Worldview section back and ask whether it is right, rather than asking the question cold.)
6. **Blind spots.** What do you see well, and what do you reliably miss? (becomes the complement-bias table: the AI watches what the owner misses)
7. **What it must never do.** In their words. (On a deep run, sitting 3's incident is the material; bring it back and ask what the rule out of it is.)
8. **Voice rules.** Concrete and testable, at least three. (On a deep run, the taste module is the material.)

### Second half: the rehearsal loop

⛔ **Do not go from the beats to writing the skill.** Everything above is the owner describing a character in the abstract, and a described character and an authored one are not the same thing: the description always sounds right and the first real reply is what shows whether it is. So rehearse, in front of them, on their own material.

**Loop, three or four rounds, and each round is short:**

1. **Propose the archetype.** One named character the owner can picture, drawn from what they have just said: someone they have worked with, a role, a figure from a book or a film. Say what you are taking from it and what you are deliberately not. "Something like a good operations partner: says the number before the sympathy, does not manage your mood. Not the drill-sergeant part."
2. **Play it, on one real thing from their actual day.** Take a live situation from the vault or from the conversation and write **the reply itself**, in character, in full, the way it would arrive tomorrow morning. ⛔ Not a description of how it would respond. The description is what the beats already gave you.
3. **Ask them to pick it apart.** "What is off?" ⭐ Wrong is more useful than right here, so ask for the wrong part first, and if they only say it is fine, push once with the follow-up protocol: "nothing you would change at all?"
4. **Change one thing and play the same situation again.** One change per round, so the owner can tell what moved.
5. **Keep the score, on both sides.** A reply the owner approves goes to the soul's **worked simulation** slot verbatim, awkwardness included. Every phrasing they reject goes to the **anti-vocabulary** slot with a word on what was wrong with it. ⭐ **The rejects are the more valuable half**: "be direct" cannot be checked against a sentence, and "never open with 'Great question'" can.

**Stop when the owner reacts to a reply as if it came from a person rather than a draft.** That is the signal, and it usually arrives in round three. ⛔ If nothing has been rejected across the whole loop, the loop has not run: an owner agreeing with everything is being polite, and the anti-vocabulary slot being empty at the end is the proof of it. Say so, plainly, and run one more round with a deliberately overcooked version to give them something easy to push against.

### The genericness gate (hard gate, both tiers)

Before writing anything, check:

- The soul has a chosen name with a reason.
- **An archetype with something explicitly refused.** An archetype with nothing refused is a licence to drift.
- "Care underneath" names the actual business and actual stakes, not "the user's goals".
- At least 3 voice rules concrete enough to test against a single sentence.
- **At least one worked simulation the owner approved, and at least one anti-vocabulary entry.**
- "What I am not" is in the owner's own words.
- The profile names real specifics, not abstract virtues.

FAIL example: "Be clear and concise." PASS example: "Never open with 'Great question'. Tell me the risk before the plan. If I paste a draft, edit it, do not rewrite it."

If an answer lands generic, use the follow-up protocol (mechanism 1). Keep going until the gate passes; say why, once: a generic soul produces the same AI they already had.

## Part C: Build and wire

1. Fill [../templates/companion-soul-SKILL.template.md](../templates/companion-soul-SKILL.template.md) with the interview material, near verbatim where marked. Replace every placeholder AND delete the parenthetical guidance notes; the finished skill contains only the owner's content.

   **Where the rehearsal material lands, specifically:** `{{ARCHETYPE}}` / `{{ARCHETYPE_TAKEN}}` / `{{ARCHETYPE_REFUSED}}` from loop step 1, `{{WORKED_SIMULATION}}` from the approved reply verbatim, `{{ANTI_VOCABULARY}}` from the rejects. **And on a deep run, the three chains:** Worldview -> `{{CARE_UNDERNEATH}}`, sitting 3's incident -> `{{NEVER_DO}}`, taste module -> `{{VOICE_RULES}}`. ⛔ An empty slot stays empty and gets said out loud; ⛔ never write a fresh example into `{{WORKED_SIMULATION}}` to fill it, because the whole value of that slot is that the owner approved that exact text.

   Then the red-line pass (mechanism 5) over the draft. Show it; the owner rules; iterate.
2. Write it beside the command-base skill, in the same generated-skills folder that one already lives in (`99_Meta/Skills/` in a vault scaffolded by the current version, `04_Resources/Skills/` in an older one; find it rather than assuming, and keep the two together whichever it is). Then install it into `~/.claude/skills/` exactly the way the command-base was installed: read `command_base_install:` from `99_Meta/bootstrap-progress.md` and mirror it (symlink on macOS/Linux, copy on Windows, junction on Windows only if that is what the owner chose for the command-base). ⚠️ Using the flag to **pick an install method** is fine, which is all it is doing here; `SKILL.md`'s retrofit rule that the flag is never proof applies to a different question, whether an edit actually reached the loaded file, and there the answer has to come from reading the file back, following the branch and the verify step in [setup.md](setup.md) step 6. Record the outcome as `companion_soul_install:` with the same three values, so a later edit knows whether it reaches the live skill.
3. The command-base skill already loads `<slug>-companion-soul` last at session start when it exists; nothing to edit. Confirm the slug matches what the command-base expects (check its SKILL.md; fix the name if the owner changed slugs). ⚠️ **The name is load-bearing beyond this session:** the command-base looks for the soul by that exact name and, finding nothing, says the AI is still running generic. Set `jarvis_progress: {..., wired: done}` here, in the same breath as the install, because that is the flag the command-base reads to tell "no soul yet" from "a soul that went missing".
4. Fill `99_Meta/memory.md`'s Current reality with the owner's sentences if still empty (create the file from the template first only on older vaults where setup did not scaffold it).
5. Close honestly: "Expect to revise the soul several times in the first weeks. That is lived use shaping it, not a failure. Edit the vault copy; on a symlink or junction install that is the live skill. On a copy install it is not, so an edit there needs a re-copy into `~/.claude/skills/` before it takes effect. Tomorrow morning, open a session and say 'morning'; if the greeting sounds like {{AI_NAME}} and not like a generic assistant, it worked."

   **On a light run, add one line and then drop it:** "Three sections of your profile are still empty. They are the ones that need a longer conversation, and the file will tell you which. Say 'let's do the deep ones' whenever you feel like it." ⛔ Once, at the close, never again from this mode.
