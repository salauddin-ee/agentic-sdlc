import sys
from pathlib import Path

from click.testing import CliRunner

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from agentic_sdlc.cli import main


def test_init_creates_missing_target_directory(tmp_path):
    runner = CliRunner()
    target = tmp_path / "new-project"

    result = runner.invoke(main, ["init", str(target)])

    assert result.exit_code == 0, result.output
    assert target.is_dir()
    assert (target / "AGENTS.md").exists()
    assert (target / "docs" / "architecture" / "domain-model.md").exists()
    assert (target / ".agents" / "skills").is_dir()
