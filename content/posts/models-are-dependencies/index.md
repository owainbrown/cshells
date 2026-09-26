---
title: "We don't know our most important dependency"
date: 2026-09-26
draft: true
slug: "models-are-dependencies"
summary: "We pin every package in the repo, then hand a large share of our work to a model we know only by reputation. What it would take to know it properly."
tags: ["ai", "dependencies"]
---

Every mobile project we run has a lockfile. `Package.resolved`, `pubspec.lock`, a `Gemfile.lock` for fastlane: every transitive dependency is pinned to a version, most of them to a hash, and nothing moves until someone raises a pull request and CI goes green. We know most of those dependencies well: what they cost at runtime, how they fail, which versions to avoid. Then, somewhere in the same repo or in the tools around it, there's a string like `opus` or `gpt-5`. It was picked because it was what everyone was using that month, and it now decides more about what our code does than any of the packages we so carefully pinned.

A large share of our work runs through models now: planning, implementation, review, analysis and a fair amount of the prose around it. My problem isn't that we use them, or even that we don't pin them. It's that we take a remarkably casual approach to understanding what they're actually like. We know our most important dependency by reputation.

## What we know about a library, and what we know about a model

Take a networking library we've used for years. We know how it behaves under a poor connection, what its retry logic does, which calls are safe off the main thread, and the two or three bugs that bite if you use it the wrong way. Some of that came from the docs, more from reading the source, and most from watching it in production. None of it came from what people said about it online.

Now take the model doing a large share of our implementation work. Ask the team which model is best at our Swift, and you'll get an answer based on reputation. Ask how it fails on our codebases, and you'll get a couple of good stories. Ask how much its output varies if you give it the same task twice, and I doubt anyone has looked. Ask whether it has changed in the last month, and we'd find out when someone says it "feels worse this week".

Often we don't even know which model it is. Claude Code's `opus` and `sonnet` are aliases that "update over time", and Copilot's Auto setting picks a model per task based on complexity and load. On individual plans it may also serve "evaluation models" unless you opt out. We characterise a thing we can't reliably name.

## Characterising a model is hard, even for experts

Two stories suggest how easy this is to get wrong, even for people who do it for a living.

In 2023, researchers at Stanford and Berkeley reported that GPT-4's accuracy at identifying prime numbers had fallen from 84% to 51% between its March and June versions. It went viral as proof the model was getting worse. Then Arvind Narayanan and Sayash Kapoor pointed out that every number in the test set was prime. The March model mostly answered "prime" and the June model mostly answered "composite". Once composite numbers were added, all the versions were roughly as poor as each other. What had changed was the model's bias, not its ability. The behaviour really had shifted (which would break anything relying on it), but the headline characterisation was wrong, because the test was one-sided.

In August and early September 2025, Claude's output quality dropped intermittently for several weeks. Anthropic's postmortem traced it to three infrastructure bugs: a routing error, output corruption and a compiler bug. The model weights never changed. Its own evaluations, in its words, "simply didn't capture the degradation users were reporting". The people who noticed first were users with a sense of what normal looked like, but without a baseline their reports were "confusing and contradictory" and hard to act on.

If the researchers and the vendor can get this wrong, a team going on feel certainly can. The second story also shows that a pinned, unchanged model can still behave differently, so knowing its characteristics once isn't enough.

## The characteristics that matter

So what would it mean to know a model the way we know that networking library? For each place a model does work for us, I think these are the questions worth being able to answer.

- **Capability on our work.** How well does it do our tasks, not a benchmark's: Swift and Kotlin in client codebases with their own conventions, ageing CI and a decade of decisions baked in? A leaderboard average says very little about that.
- **Failure modes.** When it's wrong, how is it wrong? Confidently and plausibly, by editing more than it was asked to, by quietly ignoring a project convention, or by stopping short and calling it done? A library's failure modes are in its docs and issue tracker; a model's we have to find ourselves.
- **Variance.** Give it the same task twice and how different are the results? This decides how far any single output can be trusted, and it's the characteristic I think we've looked at least.
- **Sensitivity.** How much does behaviour move when the prompt, the harness version or the amount of context changes? A model that's excellent with a tight prompt and poor with a sprawling one is a different dependency depending on who drives it.
- **Cost and speed per task.** Measured on a finished piece of work, not per token. Tokenisers and reasoning settings differ enough that the price list is a poor guide.
- **Drift.** Is any of the above changing, and would we know if it were?

Most teams, us included, could answer the first loosely and none of the others.

## Getting to know it without a platform

None of this needs an evaluation product. It needs a few habits, and the discipline to keep them when a new model arrives and everyone wants to try it.

**Hold it still while you look.** You can't characterise a moving target, so while measuring, pin the model ID, the prompt and the harness version together. In agent tools the harness matters as much as the model, because a new release can change the system prompt, the tools the agent has, how context is managed or the default reasoning effort. Pinning `claude-opus-5-5` pins none of that.

**Use our own cases.** For each use, take a few dozen real tasks from our own history: tickets, pull requests, the migration that went wrong. Where you can, check results with plain assertions, and otherwise with a short rubric. Building those cases is real work, probably a couple of days for the first use case, and it's the part most likely to be skipped.

**Run each case more than once.** A single run tells you about one sample, not the model. Five runs per case is enough to see the spread, and the spread is often the most useful thing you learn. Without it, a small dip in a score is indistinguishable from noise.

**Write the failure modes down.** Keep a short, living list per use: what it gets wrong, how it looks when it does, and what reviewers should check for. This is the part that makes human review effective, because a reviewer who knows how a model fails catches far more than one who doesn't.

**Keep it proportionate.** Where a person reviews every output closely, floating on the newest model is reasonable, and the characterisation's job is to tell reviewers what to look for. Where output ships at scale or without close review (pipelines, automated review, anything that touches a client's code on its own), pin, measure and re-measure before changing anything.

I'd record all of this next to the code, in something as plain as this:

```yaml
# models.yaml: what we depend on, and what we know about it
review-agent:
  model: claude-opus-5-5
  harness: claude-code@2.1.280
  prompt: prompts/review@v7
  cases: evals/review            # 40 cases from our own PR history
  last-measured: 2026-09-24
  score: 0.86 (range 0.81-0.90 over 5 runs)
  failure-modes: docs/models/review-agent.md
  retires: none announced
```

## Treat it like the yearly SDK

For a mobile team, the nearest thing we already manage well is Apple's platform. Every September a new Xcode and SDK arrive, the App Store sets a date after which we have to build with them, and we plan for it: betas early, a spike on each project, a list of what broke last time. Nobody thinks of it as optional, and nobody relies on reputation to know whether their app still works.

Models now run on a similar clock, just faster and with less warning. Anthropic commits to at least 60 days' notice before retiring a public model; OpenAI gives six months for its generally available models, and is switching off a set of 2025 snapshots this December. So pinning doesn't buy stability, it buys time. The habit I'd borrow from the SDK cycle is to re-characterise at every change, forced or chosen, and on a schedule in between, because the 2025 postmortem shows a model can drift while its ID stays the same.

The obvious objection is that models improve so quickly that careful characterisation is out of date before it's finished, so why bother? I think that gets it backwards. The expensive part of characterising a model is building the cases, and they don't belong to any model. They're a description of good work on our codebases, and they outlive every model we run through them. The failure modes carry over too: overreaching edits, drifting conventions, confident invention and stopping early turn up across models, even when how often they happen changes. What goes stale is the numbers, and refreshing them is the cheap part.

The objection also assumes that newer means better at our work, which is exactly what we haven't measured. Without the cases, adopting every release isn't keeping up, it's just changing models, and we can't tell a better model from a different one. With them, a new model costs an afternoon's re-run and a decision rather than weeks of finding out by feel. So the faster things move, the more the measurement is worth. And we don't have to keep up with the frontier anyway, only know what we're running. We don't put every iOS beta on client apps; we adopt when we've checked. Models deserve the same deliberate lag.

## What I found when I looked

{{< callout warn >}}Result pending. Replace this section once the experiment has run.{{< /callout >}}

*The experiment:* one real code review from our own history, on a pull request where we know what a good review should catch. Run it 20 times with the model, prompt and harness we use today, all pinned. Record what each run flagged, what it missed, what it got wrong, how long it took and what it cost.

*What to report:* how many of the known issues were caught every time, sometimes or never; the spread of findings across runs; and any failure mode that showed up more than once. A short paragraph on what surprised me.

*The demo sits here:* a grid of the 20 runs, one tile per run, coloured by which known issues each caught. The reader can sort the tiles, pick any two runs to compare side by side, and switch to a view of which issues were caught how often. Real data from the experiment, not illustrative numbers.

## Where I'm starting

None of this is sophisticated. It's the curiosity we already apply to a networking library, pointed at the component that now writes a good share of our code. I think we haven't done it because models arrived as tools rather than dependencies, and we judge tools by how they feel to use. That was fine when they finished our lines; it isn't now they write our pull requests.

So here's what I'm going to do on our side over the next month. First, a `models.yaml` for each active project and pipeline, including the tools people use day to day. Second, the review experiment above expanded into a proper set of cases, run five times each, with the model, prompt and harness pinned. Third, a written list of failure modes for that use, shared with everyone who reviews its output. I'll write up what the inventory turns up and what a month of measurement teaches us in a follow-up post.

## Sources

- [How is ChatGPT's behavior changing over time? Chen, Zaharia and Zou, 2023](https://arxiv.org/abs/2307.09009)
- [Is GPT-4 getting worse over time? Narayanan and Kapoor](https://www.normaltech.ai/p/is-gpt-4-getting-worse-over-time)
- [A postmortem of three recent issues, Anthropic](https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues)
- [Model deprecations, Claude Platform Docs](https://platform.claude.com/docs/en/about-claude/model-deprecations)
- [Deprecations, OpenAI API](https://developers.openai.com/api/docs/deprecations)
- [OpenAI retiring GPT-5 and o3 snapshots in December 2026, privatedevops.com](https://privatedevops.com/news/openai-retires-gpt-5-o3-snapshots-december-2026)
- [Model configuration, Claude Code docs](https://code.claude.com/docs/en/model-config)
- [About Copilot auto model selection, GitHub Docs](https://docs.github.com/en/copilot/concepts/models/auto-model-selection)
