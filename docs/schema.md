# Project Lock In — Schema Documentation

Version: **1.0**

Last Updated: **2026-06-29**

---

# Purpose

This document defines the data architecture of Project Lock In.

It describes:

- Every file
- What it stores
- Who owns the data
- When it is updated
- Relationships between files

This document is the contract for the repository.

---

# Design Philosophy

Project Lock In follows five core principles.

## 1. Single Source of Truth

Every piece of information has exactly one owner.

No duplicated data.

Example:

- Player level belongs in `player.yaml`.
- Curriculum belongs in `curriculum.yaml`.
- Quest definitions belong in `curriculum.yaml`.
- Quest progress belongs in `quests.yaml`.

---

## 2. Static vs Dynamic Data

Static data rarely changes.

Dynamic data changes every Save Game.

### Static

- curriculum.yaml
- world.yaml
- rules.yaml

### Dynamic

- player.yaml
- quests.yaml
- journal.yaml
- review-queue.yaml
- mentor-notes.yaml
- stats.yaml
- projects.yaml
- mistakes.yaml
- achievements.yaml
- boss-battles.yaml
- changelog.yaml

---

## 3. Repository is the Source of Truth

Project Lock In does not rely on ChatGPT memory.

The repository contains the entire game state.

Every session begins by loading the latest repository.

---

## 4. Save Game

Only changed files are updated.

Never regenerate the repository.

Workflow

```text
Load Game

↓

Play

↓

Save Game

↓

Patch Notes

↓

Update Changed Files

↓

Git Commit
```

---

## 5. Schema Stability

Schemas should remain stable.

If a breaking change is needed:

- Increment major version
- Update this document
- Migrate repository

---

# Repository Structure

```text
project-lock-in/

README.md

docs/
    GameDesignDocument.md
    schema.md

protocol/
    mentor.md

data/

    player.yaml

    curriculum.yaml

    quests.yaml

    review-queue.yaml

    mistakes.yaml

    journal.yaml

    mentor-notes.yaml

    stats.yaml

    projects.yaml

    world.yaml

    boss-battles.yaml

    achievements.yaml

    rules.yaml

    changelog.yaml
```

---

# File Responsibilities

---

## player.yaml

Owner

Player

Purpose

Stores the player's current save.

Contains

- Character
- Level
- EXP
- Current Academy
- Current Mission
- Progress
- Reviews
- Statistics
- Learning Profile
- Mentor Assessment

Updated

Every Save Game

---

## curriculum.yaml

Owner

Game

Purpose

Defines every academy, module, mission, skill, concept and mental model.

Contains

- Academies
- Modules
- Skills
- Concepts
- Dependencies
- Mission definitions
- Mental Models

Updated

Only when new content is added.

Never stores player progress.

---

## quests.yaml

Owner

Player

Purpose

Tracks active and completed quests.

Contains

- Main Quest
- Active Quest
- Side Quests
- Completed Missions
- Failed Missions

Updated

Save Game

---

## review-queue.yaml

Owner

Player

Purpose

Controls spaced repetition.

Contains

- Today
- Tomorrow
- This Week
- Next Week
- Overdue
- Review Rules

Updated

Save Game

---

## mistakes.yaml

Owner

Player

Purpose

Tracks misconceptions.

Mistakes are never deleted.

Instead

Active

↓

Resolved

Contains

- Mistake
- Correction
- Session
- Severity
- Status

Updated

Whenever misconceptions are discovered or resolved.

---

## journal.yaml

Owner

Player

Purpose

Engineering logbook.

Not a diary.

Contains

- Mission
- Summary
- Mental Models
- Questions
- Discoveries
- Mentor Feedback

Updated

After every completed mission.

---

## mentor-notes.yaml

Owner

Mentor

Purpose

Long-term teaching observations.

Contains

- Strengths
- Weaknesses
- Learning Style
- Teaching Strategy
- Recommendations

Updated

Whenever meaningful observations occur.

---

## stats.yaml

Owner

System

Purpose

Aggregated statistics.

Contains

- Sessions
- Hours
- Missions
- Reviews
- Boss Battles
- Projects
- Achievements

Updated

Save Game

---

## projects.yaml

Owner

Player

Purpose

Engineering portfolio inside Project Lock In.

Contains

Training Projects

Portfolio Projects

Boss Projects

Each project stores

- Technologies
- Concepts
- Lessons Learned
- Mentor Evaluation

Updated

Whenever project progress changes.

---

## world.yaml

Owner

Game

Purpose

Defines the world.

Contains

- Ranks
- Academies
- Unlock Order
- Story Chapters

Updated

Rarely.

---

## boss-battles.yaml

Owner

Player

Purpose

Tracks boss battle progress.

Contains

- Available
- Active
- Completed
- Failed

Updated

Save Game

---

## achievements.yaml

Owner

Player

Purpose

Permanent accomplishments.

Achievements are never removed.

Updated

When unlocked.

---

## rules.yaml

Owner

Game

Purpose

Defines gameplay rules.

Contains

- EXP philosophy
- Reviews
- Knowledge Decay
- Mentor Responsibilities
- Player Responsibilities

Updated

Rarely.

---

## changelog.yaml

Owner

Repository

Purpose

Historical record.

Never delete entries.

Append only.

Updated

Whenever meaningful repository changes occur.

---

# Data Ownership

| Data                | Owner             |
| ------------------- | ----------------- |
| Player Level        | player.yaml       |
| EXP                 | player.yaml       |
| Current Mission     | player.yaml       |
| Academy Definitions | curriculum.yaml   |
| Mission Definitions | curriculum.yaml   |
| Concepts            | curriculum.yaml   |
| Mental Models       | curriculum.yaml   |
| Quest Progress      | quests.yaml       |
| Reviews             | review-queue.yaml |
| Mistakes            | mistakes.yaml     |
| Journal             | journal.yaml      |
| Mentor Observations | mentor-notes.yaml |
| Statistics          | stats.yaml        |
| Projects            | projects.yaml     |
| World               | world.yaml        |
| Boss Battles        | boss-battles.yaml |
| Achievements        | achievements.yaml |
| Rules               | rules.yaml        |
| Repository History  | changelog.yaml    |

---

# Session Lifecycle

Every learning session follows the same flow.

```text
Load Game

↓

Read Repository

↓

Play

↓

Mission

↓

Exercises

↓

Discussion

↓

Boss Battle (optional)

↓

Save Game

↓

Generate Patch Notes

↓

Update Changed Files

↓

Git Commit
```

---

# Session IDs

Every learning session receives an ID.

Example

```
S-0001

S-0002

S-0003
```

These IDs are referenced by:

- Journal
- Mistakes
- Reviews
- Mentor Notes
- Quest Completion

---

# Versioning

Major

Breaking schema changes.

Example

1.x → 2.0

Minor

New optional fields.

Example

1.0 → 1.1

Patch

Documentation fixes.

Example

1.0.1

---

# Engineering Philosophy

Project Lock In rewards:

- Understanding
- Reasoning
- Curiosity
- Communication
- Independent Problem Solving

It does not reward:

- Memorization
- Blind copying
- Passive learning

---

# Final Rule

If a proposed feature does not improve today's gameplay,
it is postponed.

Project Lock In is built through continuous iteration,
not endless planning.
