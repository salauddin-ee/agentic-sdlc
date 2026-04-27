import sys
from pathlib import Path

from click.testing import CliRunner

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from agentic_sdlc.cli import main

REPO_ROOT = Path(__file__).resolve().parents[1]
UNSUPPORTED_ENTRYPOINTS = ("CLAUDE.md", "GEMINI.md", "AMP.md", "ANTIGRAVITY.md")
PLATFORM_DOCS = (
    "docs/platforms/codex.md",
    "docs/platforms/claude.md",
    "docs/platforms/opencode.md",
    "docs/platforms/cursor.md",
    "docs/platforms/gemini.md",
    "docs/platforms/antigravity.md",
    "docs/platforms/amp.md",
)

# Canonical set of stubs created by `asdlc init` — must stay in sync with cli.py
EXPECTED_STUBS = (
    "docs/architecture/domain-model.md",
    "docs/product/features/brd.md",
    "docs/product/design-system.md",
    "docs/product/mockups.md",
    "docs/product/accessibility.md",
    "docs/architecture/tech-architecture.md",
    "docs/architecture/coding-standards.md",
    "docs/sdlc/epics/implementation-plan.md",
    "docs/architecture/data-domain.md",
    "docs/architecture/existing-system.md",
)

# Canonical set of directories created by `asdlc init`
EXPECTED_DIRS = (
    "docs/architecture/adrs",
    "docs/product/features",
    "docs/product/mockups",
    "docs/sdlc/epics",
    "docs/sdlc/stories",
    "docs/sdlc/workspaces",
    "docs/sdlc/test-plans",
    "docs/sdlc/retrospectives",
)

# Paths that were previously scaffolded but removed — regression guard to
# prevent them being re-introduced accidentally.
ORPHAN_PATHS = (
    "docs/architecture/rfcs",
    "docs/investigations",
    "docs/product/personas.md",
)


# ── Original entrypoint tests ──────────────────────────────────────────────

def test_init_creates_missing_target_directory(tmp_path):
    runner = CliRunner()
    target = tmp_path / "new-project"

    result = runner.invoke(main, ["init", str(target)])

    assert result.exit_code == 0, result.output
    assert target.is_dir()
    assert (target / "AGENTS.md").exists()
    assert (target / "docs" / "architecture" / "domain-model.md").exists()
    assert (target / ".agents" / "skills").is_dir()


def test_init_installs_agents_md_as_only_entry_point(tmp_path):
    runner = CliRunner()
    target = tmp_path / "new-project"

    result = runner.invoke(main, ["init", str(target)])

    assert result.exit_code == 0, result.output
    assert (target / "AGENTS.md").exists()
    for entrypoint in UNSUPPORTED_ENTRYPOINTS:
        assert not (target / entrypoint).exists()


def test_repo_root_does_not_ship_unsupported_platform_entrypoints():
    for entrypoint in UNSUPPORTED_ENTRYPOINTS:
        assert not (REPO_ROOT / entrypoint).exists()


def test_platform_docs_describe_agents_md_as_supported_entry_point():
    for rel_path in PLATFORM_DOCS:
        content = (REPO_ROOT / rel_path).read_text()
        assert "`AGENTS.md`" in content, rel_path
        for entrypoint in UNSUPPORTED_ENTRYPOINTS:
            assert f"`{entrypoint}`" not in content, rel_path


# ── Init scaffold contract tests ───────────────────────────────────────────

def test_init_creates_all_expected_stubs(tmp_path):
    runner = CliRunner()
    target = tmp_path / "new-project"

    result = runner.invoke(main, ["init", str(target)])

    assert result.exit_code == 0, result.output
    for rel in EXPECTED_STUBS:
        assert (target / rel).exists(), f"Missing stub: {rel}"


def test_init_creates_all_expected_dirs(tmp_path):
    runner = CliRunner()
    target = tmp_path / "new-project"

    result = runner.invoke(main, ["init", str(target)])

    assert result.exit_code == 0, result.output
    for rel in EXPECTED_DIRS:
        assert (target / rel).is_dir(), f"Missing dir: {rel}"


def test_init_does_not_create_orphan_paths(tmp_path):
    """Regression guard: ensure previously-removed scaffold paths are not re-added."""
    runner = CliRunner()
    target = tmp_path / "new-project"

    result = runner.invoke(main, ["init", str(target)])

    assert result.exit_code == 0, result.output
    for rel in ORPHAN_PATHS:
        assert not (target / rel).exists(), f"Orphan path should not exist: {rel}"


# ── update-agents tests ────────────────────────────────────────────────────

def test_update_agents_appends_context_block(tmp_path):
    runner = CliRunner()
    target = tmp_path / "new-project"

    # init first so AGENTS.md and docs structure exist
    runner.invoke(main, ["init", str(target)])

    # write a tech-architecture file so update-agents detects it
    tech_arch = target / "docs" / "architecture" / "tech-architecture.md"
    tech_arch.write_text("# Technical Architecture\n")

    result = runner.invoke(main, ["update-agents", str(target)])

    assert result.exit_code == 0, result.output
    agents_content = (target / "AGENTS.md").read_text()
    assert "## Project Context" in agents_content
    assert "tech-architecture.md" in agents_content


def test_update_agents_fails_gracefully_without_init(tmp_path):
    """update-agents should print an error, not crash, when AGENTS.md is missing."""
    runner = CliRunner()
    target = tmp_path / "uninitialised-project"
    target.mkdir()

    result = runner.invoke(main, ["update-agents", str(target)])

    assert result.exit_code == 0
    assert "not found" in result.output.lower()
