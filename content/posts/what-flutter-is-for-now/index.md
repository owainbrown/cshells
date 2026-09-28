---
title: "What Flutter is for now"
date: 2026-09-26T21:00:00+01:00
draft: false
wip: true          # published, with the draft note at the top
unlisted: true     # reachable by its address only: not in lists, tags, RSS or the sitemap
slug: "what-flutter-is-for-now"
summary: "AI takes away much of the cost of writing an app twice. That leaves Flutter two narrower jobs: the app a client wants to own cheaply, and a single executable statement of what an app does."
tags: []           # no tags: a tag would show up in Topics
build:
  list: never
---

Earlier this month Shopify announced that native is now the future of mobile at Shopify. That's the company whose 2020 post made React Native feel like a safe bet for everyone else. Its reason wasn't a flaw in React Native. It was that "LLMs changed one of the core assumptions behind our 2020 decision". Building two native apps still costs more than one, but agents now do enough of the implementation, translation, testing and review that the cost is "no longer the deciding factor it was in 2020".

I run a team that builds a lot of Flutter, and I think that sentence matters as much for Flutter as for React Native. The case for cross-platform has always rested on the cost of writing everything twice. If AI takes a large part of that cost away, cross-platform stops being the sensible default, and Flutter goes into that argument from an already uncertain position at Google.

I don't think that leaves Flutter without a job, though. I think it leaves it with two narrower, clearer ones: the app a client wants to own cheaply for years, and the single, executable statement of what an app does, at a time when we don't yet have a better way to write that down.

## An uncertain position already

To be clear, Flutter isn't dying. It shipped eight stable releases in 2025. Google said at I/O 2025 that nearly 30% of new free iOS apps were built with it, and it has put real work into AI tooling: the GenUI SDK, a Dart and Flutter MCP server, and an AI toolkit. By usage, it's in rude health.

Its position inside Google is another matter, and the signals over the last two years have been mixed at best:

- **The 2024 layoffs.** In April 2024, weeks before I/O, Google cut staff from the Flutter and Dart teams as part of a wider restructure. Google's line was that they "weren't affected any more or less than other teams", which was reassuring, if not exactly a statement of priority.
- **The Flock fork.** In October 2024 a former Flutter team member forked the framework, citing slow pull request reviews and stalled platform work. Non-Google contributors now reportedly outnumber Google's own on the project.
- **Macros cancelled.** In January 2025, after more than two years of work, the Dart team abandoned macros, the feature that would have removed most of Flutter's code generation.
- **Google's other answer.** In May 2024 Android announced official support for Kotlin Multiplatform for sharing business logic across Android, iOS and web, and Google Docs was the flagship example. So Google now has two cross-platform stories, and only one of them sits inside Android.
- **Chasing Apple's design language.** Flutter draws its own pixels, so every new Apple design language has to be rebuilt. iOS 26 and Liquid Glass shipped last September. Flutter's answer, this September, is to move Material and Cupertino into separate packages that can release weekly, and "work is already underway" on an official Liquid Glass implementation. It's a sensible fix, but it arrived a year behind the platform.

None of that is fatal. What it adds up to is a framework whose future depends on Google continuing to fund something Google itself doesn't strictly need. That's a weaker position from which to absorb a change in the economics that justify it.

## What Shopify actually showed

The headline is the decision, but the detail in Shopify's write-up of migrating the Shop app is more useful.

- **It was fast.** Twelve weeks from proof of concept to a rebuilt native app in both stores. A core team of six built the foundations and main journeys, with feature teams joining partway through. The proof of concept was one engineer spending a week with coding agents, porting as much of the React Native app to SwiftUI as they could.
- **Agents were best at translation.** They were "particularly effective when they had an existing implementation to work from". They could build a feature on Android using the iOS version as a reference, and the other way round, which is exactly the work that makes two codebases expensive.
- **The result was better.** Startup was 23% faster on iOS and 50% faster on Android, crashing sessions fell tenfold, and the Android app shrank by 37%.
- **Expertise still mattered.** "Native expertise remained essential. Generated code could satisfy feature requirements while still introducing duplication, architectural drift, or performance problems."

That last point is the honest one, and I'll come back to it. But the shape of the argument doesn't depend on React Native. It applies to any framework whose main selling point is avoiding a second codebase.

## What AI changes

I think there are four ways AI changes the maths, and none of them is good news for a framework sold on avoiding a second codebase.

**The saving shrinks, but the costs don't.** Cross-platform has always been a trade: one codebase in exchange for drawing a step away from the platform. Agents cut the cost of the second codebase, which is the thing Flutter saves you, while its costs stay where they were. It still renders its own widgets, so it still chases Apple's and Google's design changes. Platform features still arrive through plugins. It's still a third ecosystem to hire for alongside Swift and Kotlin.

**Native pairs translate well.** Shopify's agents did best when porting from an existing implementation, and SwiftUI and Jetpack Compose are close cousins: both declarative, with similar ideas about state and composition. An agent turning a SwiftUI screen into Compose is working between two well-documented, closely related models. Flutter has no native twin to translate from or to.

**Training data follows popularity.** Models learn from public code, and there's a great deal more public Swift, Kotlin and TypeScript than Dart. I'd expect that to show up as models being better at the first three, but I want to be careful here: I haven't found a benchmark that splits model performance by Dart against Swift or Kotlin, and my own team's impression isn't evidence. It's a hypothesis worth testing, and it's the kind of characteristic I argued [in an earlier post]({{< relref "/posts/models-are-dependencies" >}}) we should be measuring rather than assuming. React Native has an edge over Flutter on this one, because it sits on the largest code corpus there is.

**The one-language team matters less.** Part of Flutter's appeal for a small team is that everyone works in one language across both platforms. Shopify found agents helped developers "ramp up and contribute effectively outside their primary stack". If a Kotlin developer can work competently in a SwiftUI codebase with an agent alongside, one of Flutter's organisational advantages fades too.

## Role one: the app a client wants to own cheaply

Agents cut the cost of writing an app. They do much less for the cost of owning one, and for a lot of our clients owning is most of the bill.

Think of the client whose app does its job and mostly sits there: a booking flow, a loyalty scheme, a companion to a physical product. They don't want a roadmap, they want it to keep working. Even so, it faces a yearly treadmill. There's a new iOS and a new Android, then store deadlines to build against the new SDKs, then dependency updates, security fixes and the odd policy change that means a release nobody asked for. Shopify was clear that the cost of two platforms "has not disappeared". For this client, that remaining cost is the whole relationship, and doing the treadmill once is cheaper than doing it twice, however the code was written.

And the treadmill is speeding up. Both stores are asking more of apps that nobody is actively developing:

- **Apple's SDK floor.** Since 28 April 2026, uploads must be built with Xcode 26 against the iOS 26 SDK. The floor moves every year, and each move brings its own deprecations.
- **Liquid Glass.** Apps built with Xcode 26 pick up the new design automatically, and the opt-out Apple offered is temporary. Apple's developer support has said it "will be removed in Xcode 27, so it can only be delayed for a maximum of one year". For an app with any custom UI, that's rework whether or not the client wanted a redesign.
- **Play's target API level.** From 31 August 2026, updates must target Android 16 (API level 36), with the behaviour changes that come with it.
- **Memory page size.** Apps targeting Android 15 or later must support 16 KB memory pages. From February 2027, updates that don't won't be released. Anything with native code, or depending on a library that has it, needs rebuilding and testing.
- **Sign-in.** Google has deprecated the legacy Google Sign-In for Android and will remove it from the Play services SDK in a future release. Apps need to move to Credential Manager.

None of that adds a feature. It's the cost of staying in the store, and it lands on every app every year, whether or not the client has budget for it.

The interesting part is that these requirements don't all fall the same way. Toolchain and policy changes, such as the SDK floor, target API level, page size and sign-in APIs, are paid once in a Flutter app, largely through framework and plugin upgrades. In a native pair they're paid twice. Design-language changes cut the other way, and more subtly. A native app gets Liquid Glass largely for free by rebuilding, but any custom UI breaks. A Flutter app draws its own widgets, so removing the opt-out changes nothing about how it looks. For a client who wants the app to keep working rather than keep up, that insulation is a feature. The flip side is that the app gradually looks dated next to its neighbours on the home screen, and catching up means waiting for Flutter's own implementation.

There's also a cost that doesn't show up in any store announcement. In a Flutter app every platform change arrives through plugins: camera, payments, sign-in, notifications, storage. Each one tracks two platforms on its maintainer's timetable, which means a steady trickle of minor versions, the odd breaking API change and the occasional plugin that stalls and has to be replaced. None of it is large on its own, but it never stops, and it lands on apps nobody is actively developing. So in a Flutter app you pay the compliance cost once, but on the timetable of the Flutter team and your plugin authors, plus a small continuous tax for going through them. A plugin whose maintainer is slow to ship 16 KB support becomes your deadline problem. For low-maintenance apps, that argues for keeping the plugin list short, preferring first-party and well-maintained plugins, and budgeting for the trickle rather than pretending it isn't there.

It isn't quite one against two, and I'd rather be honest about that. A Flutter app has one codebase, but it still tracks three toolchains: Flutter and Dart, Xcode and iOS, and Gradle and Android. Plugins lag behind the platforms, as Liquid Glass showed. My expectation is that for small, stable apps Flutter still comes out clearly ahead, but that's an expectation rather than a finding.

It's also one we can check. We have years of maintenance history across Flutter and native apps, so hours per app per year, split by stack, would answer it for our clients far better than anyone's opinion, mine included. **\[Add the numbers here once pulled.\]**

## Role two: a single statement of what the app does

This is the argument I find more interesting, because it looks forward rather than defending the present.

If more of our code ends up generated, the valuable artefact stops being the code and becomes the precise description of what the app should do. We don't have a good format for that yet. Natural-language specs are ambiguous, which is exactly where agents go wrong. Two native codebases are two descriptions of the same app that drift apart a little with every release. Designs describe how it looks, not how it behaves.

A Flutter codebase is one description, it's executable, and it's testable. It says what happens when the network drops halfway through checkout in a way no document does. It also fits what Shopify found: agents did their best work when "they had an existing implementation to work from". A Flutter app is that reference implementation, waiting. If a client later needs native, for performance, platform features or a new owner's preference, a well-built Flutter app is the best possible starting point for generating it. Choosing Flutter keeps that option open rather than closing it off.

The caveat is that code describes an implementation, not an intention. A Flutter app carries Flutter-specific workarounds and incidental decisions you wouldn't want to carry across. The parts that really work as a platform-neutral statement are the ones that don't depend on Flutter: the domain layer, the data contracts and the behavioural tests. That makes this argument conditional on how the app is built. A Flutter app with a clean domain layer written against interfaces and a good set of acceptance tests is a strong single statement. One with its business logic tangled into widgets isn't, and it's only a single codebase, not a single source of truth.

It's also not the only candidate. Kotlin Multiplatform makes the same claim for business logic, with Android's backing. Its answer is to share the statement of behaviour and write each UI natively, which agents now make cheaper. I think that's the approach to watch most closely, and I'd expect some of our future projects to look like it.

## What I'd do with a Flutter team today

Panicking would be the wrong response, and so would carrying on as if nothing had happened. What I'd do:

- **Leave existing apps alone.** Nothing here justifies a rewrite on its own. Flutter apps in production should stay Flutter until something about the product, not the framework, makes the case.
- **Choose Flutter for a reason, not by default.** On new work, ask which client this is. For an app the client wants to own cheaply for years, Flutter is still my first answer. For a brief that leans on platform look and feel, deep platform integration or heavy ongoing development, native with agents deserves a proper costing alongside it, and so does shared Kotlin logic with native UI.
- **Build Flutter apps as if they'll be translated.** Keep the domain layer clean and behind interfaces, keep business logic out of widgets, and invest in behavioural tests. It's good practice anyway, and it's what turns a Flutter codebase into a portable statement of the app rather than just a single codebase.
- **Measure both claims.** Pull maintenance hours per app per year by stack, and build one real feature with agents in Dart and in Swift and Kotlin to compare effort, quality and review burden.
- **Keep the team bilingual.** Flutter developers who can read and review Swift and Kotlin are worth more whichever way this goes.
- **Watch the signals.** Whether an official Liquid Glass implementation lands soon, where Google puts Flutter headcount, and whether the talk of a Flutter Foundation becomes governance that doesn't depend on one company's priorities.

For a decade, Flutter's job was to save you from writing an app twice. AI is taking a lot of that job away. What's left is narrower and, I think, more durable: keeping an app cheap to own, and being the clearest statement of what it does until we've learnt to write that down some better way.

## Sources

- [Native is now the future of mobile at Shopify, Shopify Engineering, 10 Sep 2026](https://shopify.engineering/back-to-native)
- [Migrating Shop app from React Native to native, Shopify Engineering](https://shopify.engineering/shop-app-migration)
- [Simon Willison on Shopify's move](https://simonwillison.net/2026/Sep/10/shopify-react-native/)
- [Google lays off staff from Flutter, Dart and Python teams, TechCrunch, May 2024](https://techcrunch.com/2024/05/01/google-lays-off-staff-from-flutter-dart-python-weeks-before-its-developer-conference/)
- [Developer forks Flutter, citing issues at Google, Techzine](https://www.techzine.eu/news/devops/125753/developer-forks-flutter-citing-issues-at-google/)
- [State of Flutter 2026, Dev Newsletter](https://devnewsletter.com/p/state-of-flutter-2026/)
- [Android support for Kotlin Multiplatform, Android Developers Blog, May 2024](https://android-developers.googleblog.com/2024/05/android-support-for-kotlin-multiplatform-to-share-business-logic-across-mobile-web-server-desktop.html)
- [Material and Cupertino decoupling are here, Flutter Blog](https://flutter.dev/blog/decoupling-material-cupertino)
- [MobileDev-Bench, arXiv](https://arxiv.org/html/2603.24946v1)

Store requirements:

- [SDK minimum requirements, Apple Developer](https://developer.apple.com/news/upcoming-requirements/)
- [UIDesignRequiresCompatibility usage period, Apple Developer Forums](https://developer.apple.com/forums/thread/801712)
- [Target API level requirements for Google Play apps, Play Console Help](https://support.google.com/googleplay/android-developer/answer/11926878?hl=en)
- [Support 16 KB page sizes, Android Developers](https://developer.android.com/guide/practices/page-sizes)
- [About the migration from legacy Google Sign-In, Android Developers](https://developer.android.com/identity/sign-in/legacy-gsi-migration)
