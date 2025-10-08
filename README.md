# Bots with Python

## [Nippan GPT](https://github.com/kurosame/nippan-gpt)

Have daily sales reports responded to in Slack using Azure GPT

## Setup for Claude Code

Execute the following command.

```sh
ln -s ~/ghq/github.com/kurosame/dotfiles/.claude/.mcp.json .

npx cc-sdd@latest --lang ja # generate .claude/commands/kiro

claude # Start Claude Code

/init                    # generate CLAUDE.md
/mcp__serena__onboarding # generate .serena
/kiro:steering           # generate .kiro/steering

codex # Start Codex

/init # generate AGENTS.md
```
