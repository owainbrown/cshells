---
title: "Questions we couldn't afford to answer"
date: 2026-09-26T20:00:00+01:00
draft: false
wip: true          # published, with the draft note at the top
slug: "questions-we-couldnt-afford"
summary: "Most talk about models is about writing more code, sooner. The bigger change is what happens to the cost of an answer, and in an agency that moves the line on which questions we can afford to answer properly."
tags: ["ai", "agency"]
---

Most of the talk about models at work is about volume: more code, sooner. That's real, but I don't think it's the most interesting change. The bigger one, for me, is what's happening to the cost of an answer.

What we aim for is simple to say: significant decisions should rest on evidence. Where users are struggling, how delivery is tracking against the estimate, whether a data model will hold up, what someone's work shows. Every one of those deserves a proper answer, and good teams give them one.

In an agency, that aim always comes with a compromise. Time is sold by the hour, so analysis either has to be agreed with a client as part of the work or has to come out of time we'd otherwise spend delivering. Specialist tools are harder to justify when each client has their own accounts, data and budget. So we prioritise: the questions with the most riding on them get the deep treatment, and the rest get a proportionate look from experienced people. That's a reasonable trade, and it's how most of the industry works.

What models change is where that line falls. The approach I'd advocate isn't handing a model everything and seeing what comes back; it's asking a targeted question of an appropriate, often early, slice of the data, and checking the answer. Done that way, some analysis that would once have been its own piece of work can happen inside the work we're already doing, and more questions get a proper answer.

## Four questions that deserve a proper answer

**What is the analytics telling us?** Every app we build ships with analytics, and clients rightly ask what it says. A deep answer has traditionally meant dedicated analyst time, which is worth it for some decisions and hard to justify for others. A narrower question, such as where people leave one particular flow in the first weeks after a release, asked of an agreed extract of the events, can give a first read quickly enough to bring to a sprint review. It doesn't replace an analyst; it means more conversations start from the data, and it shows where a deeper analysis would be worth commissioning.

**How are we doing against the estimate?** We track delivery against estimates, and the aspiration is to go further: to see which kinds of work we consistently misjudge and what that means for the rest of the project. Doing that across tickets, worklogs and the original estimate has usually meant either a dedicated platform or careful manual reconciliation. A targeted question early in a project (are the first integration tickets running over, and by how much?) can be answered from the delivery data we already hold, without an integration project, and it's more useful early, while there's still time to adjust the plan.

**What should this database look like?** The ideal is to try several schema designs against realistic data and the queries the product will actually need. On a fixed-price project, that competes with everything else discovery has to cover, so experience and judgement carry a lot of the weight. Using a model to generate realistic synthetic data and exercise each candidate design against the queries we expect makes comparing options a more affordable part of discovery, and none of it needs production data. The analytics can be designed in from the start, too: if we know which funnels and events the client wants to measure, the schema can account for them rather than having them added after launch.

**What does someone's recorded work show?** Good feedback is specific and grounded in examples. Pull request history, review discussions and tests hold a lot of that evidence, but reading months of it by hand is more than most review cycles allow, so feedback naturally leans on conversations and the moments people remember. A model can help find examples for a specific question (how has review feedback on a particular area been taken on board?), within the tools and data the organisation has approved for it. Used carefully, that can make feedback more specific and more balanced. It's also the example that needs the most care, which I come back to below.

## What they have in common

None of these are about producing more. They're about knowing more before deciding.

- **The data was already there.** Event logs, tickets, worklogs and commit history have existed for years. What's changing is the cost of reading them properly.
- **More analysis fits inside the work.** When a first pass is quick, it doesn't always need its own budget line or tool. It can become part of doing the job well.
- **Impressions become claims someone can check.** "The onboarding feels leaky" or "we tend to underestimate integrations" become statements with evidence attached, which someone can challenge.
- **Targeted questions complement experience.** Experience tells you where to look; a well-framed question about a specific slice of data checks whether the instinct holds, and can surface quieter patterns (good work that didn't draw attention, rare failure paths, slow drifts).
- **The skilled part moves.** Producing an answer gets easier. Asking a good question and checking the answer become the work, and that's where experienced people add the most.

## Where it goes wrong

A model-written change goes through review and CI. A model-written analysis tends to be believed, especially when it arrives with numbers and a confident recommendation attached. The failure modes are different from code, and none of them show up on a coding benchmark:

- **Misreading the data.** An event that fires twice, a status that means something different on this project, an estimate field someone reused for something else. The analysis is internally consistent and built on a wrong assumption.
- **Evidence that doesn't exist.** A quoted comment from the wrong pull request, a figure that can't be traced back to a row, or a pattern described with more confidence than the data supports.
- **Answering the question as asked.** Ask where onboarding is failing and you'll get an answer even if it isn't. Ask for evidence of a weakness and you'll get some. The model finds what the framing invites.
- **Confident figures from a thin sample.** A drop-off rate across a week of traffic, or a median across a dozen review threads, reads like a fact.
- **Correlation served as recommendation.** "Users who do X retain better, so push everyone to X" is the classic, and it's easy to accept when it arrives as a tidy action.
- **Agreeing with the person asking.** A drift towards confirming what you already thought, which is the most dangerous when the analysis is about a person.

## Method: the model as researcher, not judge

The pattern I'd recommend in all four cases is to treat the model as the researcher, and keep the judgement with people.

- **Start narrow.** Ask a specific question of the smallest appropriate slice of data, using tools approved for that data, and widen only if the answer justifies it.
- **Check the inputs first.** Before trusting any analysis, have the model explain what each field and event means, and correct it where it's wrong. I'd expect most bad analyses to fail here rather than in the reasoning.
- **Trace every figure back.** A number or quote that can't be traced to a row, a ticket or a commit shouldn't go into anything shared.
- **Ask for the other side.** Ask for the counter-evidence, the alternative explanation and the case against the recommendation as explicitly as the finding itself.
- **Keep the method visible.** A write-up should say what data was used, over what period and how, so someone else can check it or challenge it.
- **Re-run it.** Ask the same question twice, or phrase it differently. If the answer moves a lot, it wasn't much of an answer. That's the variance point from [my last post]({{< relref "/posts/models-are-dependencies" >}}), applied to analysis.

## When the data is about people

The first three examples analyse products and projects. The fourth involves a person, and that deserves its own care. I haven't written this section yet; these are the points it needs to cover.

- Transparency: the person should know what was looked at and how, and be able to challenge it.
- Proportion: the same tooling could run continuously on everyone. Where's the line between supporting feedback and monitoring?
- Measures become targets: publish "time to act on review comments" and people will optimise for it.
- Data protection: this is employee data, and a model vendor may process it. Where it goes and who can see it matters.

## Close

If models only made us faster at writing code, the change would be large but familiar. What I find more significant is that they lower the cost of an answer, and in a business that sells time, that moves the line on which questions get a proper one. The judgement doesn't go away: someone still has to ask the right question, spot the misread field and refuse the confident number that doesn't trace back to anything. That's the same skill it's always been. What changes is how often we can afford to use it.
