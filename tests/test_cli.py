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
