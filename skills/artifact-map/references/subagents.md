# Subagents

How skills in this pack hand work to other agents. Use the harness's own mechanism for starting one; this file says when and how, not which tool.

## Two reasons to dispatch

- **Parallelism:** independent pieces run faster side by side, such as searches across separate areas. If the harness cannot start subagents, do the pieces in sequence; the result is the same.
- **Separation:** the work is only valid if done without the requester's context, such as an independent review. If the harness cannot start a fresh context, do not quietly do it yourself: tell the user to run the skill in a new session, or do it and label the result **not independent** at the top.

## Rules

- **One owner per source.** Each file, log, page, or probe is read by one agent, which passes on the facts with their `file:line` or source. No other agent fetches it again.
- **Brief like a peer.** A subagent knows only its prompt: give it the goal, the inputs, what is already ruled out, and the exact output shape you need back.
- **Separated agents get inputs, not reasoning.** An independent reviewer or checker receives the diff, the intent (plan or request), and the standards. Never the builder's transcript, notes, or explanation of why the code is right.
- **Bulk stays in files.** A subagent that gathers more than a page writes it to a scratch file outside the repository and returns a short summary with the path.
- **Choose the model by role.** Extraction and search: the fastest model. Building: the session's default. Independent review and hard judgment: the strongest available. Name the role in the brief; map it to a model with whatever the harness offers.
- **Verify before relaying.** A subagent's claim enters a report only after you have checked the cited line or reproduced the result.
