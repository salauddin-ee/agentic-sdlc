# Agentic SDLC for Amp (ampcode.com)

Amp natively supports lazy-loading "skills". This means Amp will automatically read and understand the Agentic SDLC methodology if the skills are placed in a location it recognizes!

### Installation for Amp

Amp looks for skills natively in the `.agents/skills/` directory.

Since the Agentic SDLC framework keeps its skills in the `/skills/` directory by default, you can easily support Amp by creating a symlink in your project root:

```bash
mkdir -p .agents
ln -s ../skills .agents/skills
```

By doing this, Amp will automatically discover all Agentic SDLC skills.

### Starting a Session

When you chat with Amp, you can invoke the lifecycle directly:
> "Start a new project. Run the `using-agentic-sdlc` skill."

Amp's native skill system will fetch the correct `.agents/skills/using-agentic-sdlc/SKILL.md` file and begin the lifecycle!
