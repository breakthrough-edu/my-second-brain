# Lane Guide: `02_Work`, the activity layer

`01_Assets` is what the business is made of. `02_Work` is what is **moving**: every live piece of work is one project, and every project sits in exactly one of four lanes. This file is the capture-side companion to the filing ladder in doctrine §1: how to ask for in-flight work, how to place it, and what to notice about it.

⚠️ **Lanes are not departments.** The ladder classifies by facts the work observably has (a name, an audience, recurrence), never by which department would own it in a big company. This vault has no departments, which is exactly why the old function rooms are gone.

---

## The ladder (ask in order, first yes wins)

1. **Deliver** · is this work for a specific NAMED customer or hot prospect?
2. **Grow** · else, is it aimed at people who have not bought yet, addressed as an audience?
3. **Run** · else, would this work still exist if the business never grew?
4. **Build** · else, by elimination: finite internal work that leaves the business different when it is done.

Three things the ladder settles that people ask about every time:

- **A client job is ONE project from pursuit to handover.** Its `stage:` tracks the lifecycle (`pursuing` → `executing` → `closed`); the project never moves and never splits. There is no separate pipeline room, because a deal you are chasing and the job you deliver are the same relationship at two moments.
- **Recurring service for a named customer stays in Deliver**, indefinitely, at `stage: executing`. Run is internal-only.
- **A Grow or Build project that turns into routine** archives as a finite project, and the recurring residue re-homes to `Run/`. Deliver is deliberately excluded from that rule.

**Materials, not projects.** Lanes hold projects, never loose files. The files inside a project (transcripts, drafts, exports) are project materials: they live with the project and need no frontmatter family. Standing material that is not tied to one project belongs in `01_Assets`, in the entity room that naturally owns it.

**Every project gets `_<Project>-Brief.md`**, and briefs are linked bare (project names are unique vault-wide). Lane guides are linked path-qualified. Tasks live in `<Project>/Tasks/` and carry no project, lane or domain keys: the path already says all three.

---

## The four doors (`guide_family: lane`)

⭐ **Scaffold copies these onto the four lane guides verbatim, and capture reads the same lines when it walks someone into a lane.** They are here rather than invented at install time for one reason: a door file is read every time anyone works in that folder, so two installs that improvise two sets of door signs are two different products. ⛔ Do not reword them per vault; translate them on a `中文` install and leave the file names English.

### Deliver

**Door sign:** work you are doing for a named customer or hot prospect. One engagement, one project, from first pursuit through handover.
**Filing test:** if the work has a specific customer's name on it, it belongs here (whether or not they have paid yet); WHO that customer is lives in `01_Assets/Clients/`; HOW you win or serve them is an SOP in `03_SOP/`. A recurring service for a named customer stays here indefinitely at `stage: executing`, and never re-homes to `Run/`.

### Grow

**Door sign:** work aimed at people who have not bought yet, addressed as an audience: content, campaigns, channels, offer design.
**Filing test:** the campaign or launch lives here while it is running; the reusable output it leaves behind (the post that worked, the photo set) graduates to `01_Assets/Marketing-Assets/` when the project closes; the platform it runs on and who holds that login lives in `01_Assets/IT-Systems/`. If it turns into routine, the finite project archives and the recurring residue re-homes to `Run/`.

### Run

**Door sign:** recurring internal upkeep: the work that would still exist if the business never grew, and never finishes.
**Filing test:** work that repeats with no end date and no customer's name on it belongs here; a recurring service for a named customer is `Deliver/`, not this; the written steps for the routine are an SOP in `03_SOP/`, and this lane is where doing it lives.

### Build

**Door sign:** finite internal work that leaves the business different when it is done: a new capability, a tool, a system, a training, an expansion.
**Filing test:** internal, has an end, and changes what the business can do → here; what it produces files in the `01_Assets` room that owns it once it exists (a new POS becomes an IT-Systems note); attending a course as an undertaking is a project here, while the notes from it live in `02_Command-Base/Resources/`.

---

## Capturing in-flight work (the question set)

This is usually the most valuable ten minutes of a first capture, because the live work is what the owner is carrying in their head right now, and it is the material an empty vault most obviously cannot help with.

**Questions:**
1. Right now, what are you actively working on or chasing? Name the top three. (do not sort them yet; just get the names out)
2. For the biggest one: how did it come in, what stage is it at, what is the next step, and **whose move is it?**
3. Is there anything you are doing for a named customer right now? (that is Deliver, whether or not they have paid yet)
4. Anything you are building or fixing internally that has an end? (that is Build; "we are moving to a new POS" counts)
5. What has to happen every week whether or not anyone sells anything? (that is Run)
6. When something goes quiet, what happens? (honest answer: usually nothing; that is a capture, not a confession)

Place each one with the ladder, out loud, in one clause: "That is a named customer, so Deliver." Then create the folder and `_<Project>-Brief.md`, filling `status`, `stage`, next step and whose move directly from what was just said. Whatever material they already have for that job moves in with it.

⛔ **Do not open a project for every passing thought.** Three to five live pieces of work is a full first capture, same ceiling as any room. And a task with no project does not get parked: propose the project first, however small, or leave the task unwritten (§0).

---

## Insight angles

- **The silent-deal graveyard.** No follow-up mechanism for stalled work: things die of silence, not of rejection, and nothing anywhere records the death. A written next step with a name against it turns a graveyard into a call somebody made, on a date.
- **Whose-move blindness.** For N of the pieces of work just named, the next move is actually waiting on the owner themselves. That number is usually a surprise, and it is visible tonight because the question was asked per project rather than in general.
- **Lane imbalance.** Everything landed in one lane. All Deliver means the business only moves when a customer pulls it; all Build means a lot is being built and little is being sold. Say what the shape is, do not prescribe.
- **The invisible Run lane.** The owner names zero recurring work, then describes five recurring things while answering something else. Recurring upkeep is the work least likely to be volunteered and most likely to be the thing eating the week.
- **Close-rate folklore.** Any conversion number the owner gives is a feeling. Marked as a guess it is still worth capturing: a month of briefs turns it into a number.

⛔ Name what you see, do not fix it in the same breath.
