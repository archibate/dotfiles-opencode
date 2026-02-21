Insight: instruction in impretive mood

---

Good:

- edit ... to make it ...
- fix ... in ...
- write a test for ...
- search web for ...
- investigate ...
- explain ...

LLMs follow instructions best when they are unambiguous and ordered. A strict task list outperforms lengthy philosophical advice.

---

Insight: asking wrongly - question drift

Sometimes you might be asking question in a wrong way - causing irrevertible information loss, that even Einstein won't be able to recover your original problem. Here's an example:

You want to achieve X.

The industral standard solution for X is Y. But you don't know that.

You become hysteria, stuck your hard brain into X, your poor brain think that Z is a solution to X.

But Z is actually a low-effcient, brainfucking, terriable approach.

Now you start to ask people:

how can I achieve Z?

people would be confused by your bizzare requirement Z, why would anyone need this?

A smart questioner should ask like this:

how can I achieve X?

Or optionally provide your bizzare Z idea (despite it can be uselsss, but as long as you convey X, that's enough):

how can I achieve X? I plan to use Z to achieve X, but get stucked again.

This way, people will know that you are actually mean to solve X, but your purposed method Z is not applicable. they will then tell you to use Y, which is the industral standard soltuion to X.

This rule also applies to asking question to LLMs.

if you only pop-up with a bizzare requirement Z - well, LLMs are trained to obey human instruction! they would really comply to your Z approach, run bizzare commands in your computer.

instead, reveal your real question, agents don't have telepathy, you must convey all your thinking into prompts. otherwise they would have to solve problem by randomly guessing your intent.

- providing Z only: Bad, you just assumed X can only be solved by Z
- providing only X: Usually good, LLMs have way more knowledge than you, if the LLM also says Z without your hinting, then at least you can confirm your are on the right track of choosing Z
- providing both XZ: Moderate, will introduce bias - since LLMs is trained to follow human intent, if human insists Z, even if LLM knows the standard way is using Y, it will try to not resist your intent - use this unless you have confidence you are more knowledgable than LLM in this specific domain

---

Insight: no taking preset answers into question

---

talk to the XYZ problem, let's also criticize some prompt simply include bias in asking question.

Your mind: I want to do xxx classification, I want to validate if LightGBM is a good choice.

Good:
- You: I am doing a classification task for xxx, please search web, investigate what are the best models suitable for this?
- GLM: Based on my investigation, the best candidates are: LightGBM, XGBoost, LogisticRegression, ...
- You: (great! GLM also concluded to LightGBM as top-1 candidate independently, without my bias hint! that means LightGBM is indeed a correct choice)

Bad:
- You: I want to do classification task for xxx, is LightGBM a good choice?
- GLM: You are absolutely right! LightGBM is an excellant solution to xxx classification because... (GLM drawing the target before archery)
- You: GLM agreed with me! but is this a industral consensus, or due to the fact that I'm mentioning LightGBM? not sure.

if you already know LightGBM is the best choice, why would you still ask? -> use the 'impretive mood' to ask agent execute it directly.

if you don't know what is the best choice, why not be humble when ask? -> investigate, ask agent do web search for state-of-art solution.

LLMs are autoregressive, they are purely predicting next words based on previous words. If LLM happens to decide start with affirmation (the stupid "You are absolutely right!" pharse of claude), then the following words would have to follow the positive tone, otherwise the total paragraph would be not high confidence to be a human-like text, excluded in its top-K probability selection.

You may ask GLM to first show the reasoning step before jump to conclusion. REASONING -> CONCLUSION. this gives the prediction of CONCLUSION more previous reasoning context, making conclusion less random. actually that's why recent model introduced CoT (thinking mode).

I constantly see GLM responsing like:

I offer these options:
- option A: xxx (not a good choice)
- option B: xxx (not a good choice)
- option C: xxx (good choice)
- option D: xxx (not a good choice)
I would recommend option C, because xxx. (GLM finally realized that C is the only good choice after listing all possbilities)

If CoT did make GLM listed all A, B, C, D explicitly in thinking text, then why not it output the C option in the top, rather than in the middle? this is a clear clue of the autoregressive, non-rollback nature of LLMs.

---

Insight: man-made 'plan' mode, postfix to append to your prompt prevents GLM hullucination.

---

opencode has a built-in PLAN mode, switching to it the agent will be prevented from editing files. a typical usage is: switch to PLAN mode -> say what you want -> agent response with a detailed plan ask you to review -> switch to BUILD mode -> ask agent to execute the previous plan.

Now I'm saying:

Just keep in BUILD mode of opencode, no need to switch to PLAN. we ask for plan manually by adding these postfix to your prompt:

Postfix: show your plan before edit.

For example, edit function X to make it faster, show your plan before edit.

Effect:

GLM will first show a its plan in text, then it will proceed to edit without user interference.

The plan is not for the user, but for GLM itself. 

Tech detail: LLM have no hidden states except previous context! by outputing a detailed text plan before outputing code, it literally 'locks' what to do for the future code generation.

here, the plan chunk act as a 'thinking' context, making the 'edit' more concentrated, less likely to hullucinate.

The built-in thinking is oftenly too rush, not enough context for GLM to making a detailed plan. However, when user explicit asking 'output a plan before edit'. GLM would use the 'thinking' tokens to think for a plan, and try its best to present a high-quality text plan, try to make it suitable for human reading. while thinking tokens are oftenly not. this plan provides a more clear guidence to following code generation, preventing code generation from shifting in-the-middle-way.

---

Postfix: show your plan, no edit.

For example, I want to wrap this web app into an electron app, show your plan.

Effect:

GLM will show a detailed plan to you, then stop, asking your agreement.

You say "proceed" or raise issues, ask for changing the plan. and GLM continue to edit.

This is to confirm GLM is fully aligned with your mind. I constantly finding I have said ambiguity words, or GLM being extending my plan way too much, into purely flaw.

also times am I realized my idea was actually not even feasible after GLM shows plan, so I can cancel the plan after realized that.

By PAUSE, let me confirming, correcting dynamically in conversation, before plan execute: I prevented unmature ideas being overinterpreted by GLM, avoids wasting time producing tons of code not matching my will.

---

Bad: I want X function in Y module. (no 'plan' postfix in prompt)

GLM could:

1. execute edit directly, but the edit can be off from your intent.
2. first show you a plan, findings. get into this good branch purely by chance.

You totally have no control over it. You don't even know if GLM will execute the edit in this round.

---

Insight: when requesting changes:

1. provide context, e.g. I'm making frontend design / doing prompt engineering. 'workflow' can have different meaning in prompt engineering and frontend.
2. what you've already done in the codebase (manually or by vibe coding).

This prevents GLM from misunderstanding your intent.

Good: I'm doing prompt engineering, I created a brainstorm agent system prompt: @agent/brainstorm.md . I notice that the brainstorm agent tends to not executing read-only commands exploring my local environment to gather information, instead it tends to ask me about information (e.g. are you using linux or windows? ubuntu or archlinux?), which is bad. I need to inform it that I permit it to run read-only bash commands to understand existing project codebase and computer environment, as long as not modifying them. how can I write concise prompt to convey these intents

GLM understand my intent: my role is act as a prompt engineer, the user ask me to edit the system prompt of a 'brainstorm' agent..

Bad: @agent/brainstorm.md make it not asking me OS information, discover OS information automatically.

GLM could think: do you want me to roleplay the brainstorm agent? Ok, I won't asking you about OS information in this conversation! let me run uname -a to get your OS information now..

---

Insight: Use a list of 'impretive' verbs.

a clear step by step guide makes GLM easy to follow, no ambiguity, no overinterpretation.

only speak of related context in prompt, no additionally adding anything could confusing GLM.

Bad: the X function is reluctant since it is no longer used in Y and Z module, we can use X2 instead in W module freely I think.

Good: remove the X function in Y module. check for references of symbol X.

An extensive example of 'a list of impretive verbs' is defining a workflow, as I done in agent/executor.md and skills/tdd-workflow/SKILL.md. a strict steps to follow, is way better than tons technical preach.

'superpowers' and 'oh-my-opencode' (totally hype, I uninstalled it in 1 day) are great bad examples in my view of prompt engineering - see https://github.com/obra/superpowers/blob/main/skills/test-driven-development/SKILL.md, it write tons of 'iron raw', 'ALL CAPITCAL', fancy memraids, but never define a clear steps for LLM to follow - totally self perceived preaching, as if a talkative stupid professor is preaching a human fellow, tons of shits wasting your tokens.

If your only got a blurry idea, cannot form a clear list of steps in your mind:

first talk with GLM to brainstorm, prompt it to discuss possbility and feasibility only, not execute.

when idea is clearified, ask GLM to create a list of steps in impretive mood (with 'show the list of steps, no execute' postfix). then you confirm these steps, and say 'execute.'

This would be way more effcient than directly tell GLM the idea to execute without discussing to produce a concrete list of steps.

---

Insight: Do not explain why to LLMs

a common mistake is keep explaining 'why I need this change' to LLMs, which turns out to be wasting your time typing. actually LLMs have no memory beyond each conversation - you have just hallucinated to view LLMs as your human workmates, you try teaching them as if they would remember your skill - no, each conversation is a fresh clone of existing GLM model, it will never remember your previous dedicated tech course you taught.

Bad: edit the X class to a singleton, because archibate's programming course said that singleton is very suitable for my universe simulator scenario, right?

Good: edit the X class to a singleton.

Good: as a design pattern expert, decide whether singleton is suitable for the UniverseSimulator class in @src/universe_simulator.cpp, show your reasoning, no edit

---

Insight: Write down docs

LLMs have no long-term memory, it only see things in previous conversation. that's why agentic become a heat - it allows LLM to respond tool calling requests, e.g.:
- execute bash command ls
- read content of xxx.py
The agentic client opencode will then execute these commands, and append the command output as 'user message', each different project would result in different command output, which contains valuable context local to your own project, thus prevents hallucination

to make LLMs actually 'memorize' your skills, knowledges, preferences, write down as documents. and mention them like this: @docs/architecture-overfiew.md refactor the architecture of X module to adapt singleton design pattern, update document afterwards to reflect the change. show your plan before edit.

notice that its important to make the agent to synchronize docs after code change, otherwise out-of-date document would fool later agents who discovered this document.

---

Insight: Mention (@) any relevant documents as context explicitly, instead of 'praying' agent to discover this document itself

If a document or code file is obviously required to correctly accomplish your task, you'd better mention them explicitly using the @ symbol.
otherwise you would have to 'pray' the agent is able to discover this document itself, purely by chance.

---

Insight: No bloating AGENTS.md

AGENTS.md is a standard path for all agentic programming tools (opencode, crush, ...). they always read AGENTS.md in your project root folder, and attach the full content of it prior to EVERY conversation.

> some agentic tools have different naming convention, e.g. claude code uses CLAUDE.md.

so make sure your AGENTS.md is clear and concise, follow prompt engineering best pratices, otherwise your agent will eat these shit before EVERY conversation, reducing conversation quality.

huge fixed prompts - either due to huge AGENTS.md or tons-of-silly-prompt plugins like oh-my-opencode - will make GLM more likely to respond like retard.

adding too much MCPs would also bloat fixed tokens: from my experiement, each MCP function occupies 100~1k of tokens (they have fixed prompts on introducing how to use these functions), these shits stick with your agent EVERY conversation. if you rarely or never use them, just do not install them by 'hobby', they're not free.

For architecture overview, big-pictures, anything that is less likely to change in future, is okay put into AGENTS.md.

do not put everything in AGENTS.md - that would be a great distraction, a flood of knowledge from ABCDE context, making them unable to focus on the most relevant context for your current E question, also a waste of tokens.

use a docs/ folder, refer docs/ in AGENTS.md, or ask agent to explore docs/ on need, or mention explicitly if you already know the agent must read this document before work.

content of AGENTS.md for project is having high-trust to agents, they would likely not running tool calls to confirm what you claimed in AGENTS.md, so make sure not to have false sentences in AGENTS.md, and always keep it up to date when architecture change - that's also a reason why I don't recommend to add too much detail in AGENTS.md - details are likely to change over time.

Bad AGENTS.md (act as a mono-document try to cover all, not feasible for big projects):

A: A is xxx...
B: B is xxx...
C: C is xxx...

Good AGENTS.md (act as a catalog, agent navigates into docs/c.md automatically when you asking C):

A: A is xxx, see docs/a.md.
B: B is xxx, see docs/b.md.
C: C is xxx, see docs/c.md.

Alternatively, you can use code as document too! since code never lies, but document can (if not synchronized correctly on code change).

A: A is xxx, see docs/a.md.
B: B is xxx, see src/b.py.
C: C is xxx, see tests/c.py.

let the code explain itself! LLMs can understand your code intent quickly, no need for bloat comments and md documents):

---

Insight: feasibility study before hand

Bad: optimize this function to <1s
- You have no clue that this function is actually possible to <1s at all. GLM would have to fool you, or making this function not working correctly to get your hard-coded goal.

Good: investigate optimization opptunities in this function
- Not setting a hard target, instead, you ask GLM to study feasibility first. whatever finally found feasible or not, this gives GLM more time to investigate, prevents GLM from rush into bizzare revamp to this function

Good: this function is slow (~20s) in XXX condition, but fast (<1s) in YYY condition, please investigate why
- Provide a reproduction guide, both Red and Green are provided, allowing GLM to reproduce these results itself, make a good starting point for investigation

Good: what is the major blocker for this function performing slow: algorithmic complicity or constant overhead?
- Offering two good starting point of analyzing performance issues, set GLM a clear starting point.

Good: write a test case (if not have yet) for this function, cover all edge cases, then run test to make sure it pass. then begin optimize this function, make sure function pass test after optimization, without editing test. give up optimization approaches that make the function regress in test.
- Use a test to ensure function is not regressed after bizzare optimization, if you haven't one yet.

---

Insight: why not try: human write code, AI reviews

actually I find LLM preforms code review very well. it always catch my bugs that I didn't even notice, points out undefinied behaviors in C++, English grammar issues and typos.

as a contrast, asking LLM writing code with domain-specific knowledge is constantly filled with hullucinatation, need taken very carefully.

actually some statistics shows that programers take 80% of their time in testing and debugging loop, not in writing code. writing code is strightforward (at least for most ACM winners), validation is the bottleneck, while code review and testing are the two main steps for validating code quality.

no 'shame' to insist write code manually in the age of 'AI hype', especially for code requiring highly skilled domain knowledge. by writing code yourself, verifying with AI, you are actually speeding up the '80%' of work time with AI power!

after all, writing code is small (user request) -> big (full code), suffering from dimension diaster, can easily get hallucinated; code review is big (full code) -> small (classify good or not), which has long been a solid industral scenario for NLPs to act as classifiers, before autoregressive LLMs have been invented. classification has always been the most robust AI model target all the ways.

---

Insight: create a fresh conversation for each request, no "Middle Ages Auntie's Foot Wrap".

...
