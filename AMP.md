# Agentic SDLC for Amp (ampcode.com)

Amp natively supports lazy-loading "skills". This means Amp will automatically read and understand the Agentic SDLC methodology if the skills are placed in a location it recognizes!

### Installation for Amp

1. Clone the framework into your project:
   ```bash
   git submodule add https://github.com/salauddin-ee/agentic-sdlc.git .agentic-sdlc-framework
   ```
2. Link skills to where Amp expects them:
   ```bash
   mkdir -p .agents
   ln -s ../.agentic-sdlc-framework/skills .agents/skills
   ```
3. Initialize the context directory:
   ```bash
   bash .agentic-sdlc-framework/scripts/init-context.sh .
   ```

### Starting a Session

When you chat with Amp, you can invoke the lifecycle directly:
> "Start a new project. Run the `using-agentic-sdlc` skill."

Amp's native skill system will fetch the correct `.agents/skills/using-agentic-sdlc/SKILL.md` file and begin the lifecycle!
