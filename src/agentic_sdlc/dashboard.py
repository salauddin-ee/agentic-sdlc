import os
import re
import yaml
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

# ── Model pricing (USD per 1M tokens) ────────────────────────────────────────
MODEL_PRICING = {
    "claude-sonnet":    {"input": 3.00,  "output": 15.00},
    "claude-haiku":     {"input": 0.25,  "output": 1.25},
    "claude-opus":      {"input": 15.00, "output": 75.00},
    "gpt-4o":           {"input": 5.00,  "output": 15.00},
    "gpt-4o-mini":      {"input": 0.15,  "output": 0.60},
    "gemini-1.5-pro":   {"input": 3.50,  "output": 10.50},
    "gemini-flash":     {"input": 0.075, "output": 0.30},
    "default":          {"input": 3.00,  "output": 15.00},
}

STATUS_COLORS = {
    "TO_DO":       "#6b7280",
    "IN_PROGRESS": "#3b82f6",
    "BLOCKED":     "#ef4444",
    "DONE":        "#10b981",
    "ARCHIVED":    "#9ca3af",
}

STATUS_EMOJI = {
    "TO_DO":       "📋",
    "IN_PROGRESS": "🔄",
    "BLOCKED":     "🚫",
    "DONE":        "✅",
}

def parse_markdown_file(filepath):
    """Extract YAML frontmatter and title from a markdown file."""
    data = {}
    try:
        content = Path(filepath).read_text(encoding="utf-8")
        # Extract YAML frontmatter
        match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
        if match:
            yaml_content = match.group(1)
            data = yaml.safe_load(yaml_content) or {}
        
        # Extract title (H1)
        title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if title_match:
            data["_title"] = title_match.group(1)
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
    return data

def estimate_cost(model, tokens_input, tokens_output):
    """Estimate USD cost for given token counts."""
    pricing = MODEL_PRICING.get("default")
    for key, price in MODEL_PRICING.items():
        if key in (model or "").lower():
            pricing = price
            break
    
    cost = (tokens_input / 1_000_000) * pricing["input"] + \
           (tokens_output / 1_000_000) * pricing["output"]
    return round(cost, 4)

def collect_data(project_root):
    """Parse all story and workspace files, return structured data."""
    root = Path(project_root)
    stories = []
    workspaces = []

    stories_dir = root / "docs" / "sdlc" / "stories"
    workspaces_dir = root / "docs" / "sdlc" / "workspaces"

    if stories_dir.exists():
        for f in sorted(stories_dir.glob("STORY-*.md")):
            d = parse_markdown_file(f)
            d["_file"] = str(f.name)
            stories.append(d)

    if workspaces_dir.exists():
        for f in sorted(workspaces_dir.glob("workspace-*.md")):
            d = parse_markdown_file(f)
            d["_file"] = str(f.name)
            workspaces.append(d)

    return stories, workspaces

def compute_metrics(stories, workspaces):
    status_counts = {"TO_DO": 0, "IN_PROGRESS": 0, "BLOCKED": 0, "DONE": 0}
    blockers = []
    in_progress = []
    done_list = []

    for s in stories:
        status = s.get("status", "TO_DO")
        status_counts[status] = status_counts.get(status, 0) + 1
        if status == "BLOCKED":
            blockers.append(s)
        elif status == "IN_PROGRESS":
            in_progress.append(s)
        elif status == "DONE":
            done_list.append(s)

    total_stories = sum(status_counts.values())
    done_pct = round((status_counts["DONE"] / total_stories * 100) if total_stories > 0 else 0)

    total_input = sum(int(w.get("tokens_input", 0)) for w in workspaces)
    total_output = sum(int(w.get("tokens_output", 0)) for w in workspaces)
    total_hitl = sum(int(w.get("hitl_count", 0)) for w in workspaces)
    total_elapsed = sum(int(w.get("elapsed_minutes", 0)) for w in workspaces)

    model_breakdown = {}
    for w in workspaces:
        model = w.get("model", "unknown")
        if model not in model_breakdown:
            model_breakdown[model] = {"input": 0, "output": 0}
        model_breakdown[model]["input"] += int(w.get("tokens_input", 0))
        model_breakdown[model]["output"] += int(w.get("tokens_output", 0))

    model_costs = {
        m: estimate_cost(m, v["input"], v["output"])
        for m, v in model_breakdown.items()
    }
    total_cost = sum(model_costs.values())

    return {
        "status_counts": status_counts,
        "total_stories": total_stories,
        "done_pct": done_pct,
        "blockers": blockers,
        "in_progress": in_progress,
        "done_list": done_list[-5:],
        "total_input": total_input,
        "total_output": total_output,
        "total_tokens": total_input + total_output,
        "total_hitl": total_hitl,
        "total_elapsed": total_elapsed,
        "model_breakdown": model_breakdown,
        "model_costs": model_costs,
        "total_cost": total_cost,
        "workspace_count": len(workspaces),
    }

def render_html(metrics, project_root, generated_at):
    sc = metrics["status_counts"]

    def story_rows(story_list):
        rows = []
        for s in story_list:
            sid = s.get("story_id", s.get("_file", "?"))
            title = s.get("_title", s.get("story_id", "Untitled"))
            status = s.get("status", "TO_DO")
            owner = s.get("owner", "—")
            branch = s.get("branch", "—")
            priority = s.get("priority", "medium")
            color = STATUS_COLORS.get(status, "#6b7280")
            emoji = STATUS_EMOJI.get(status, "")
            blocked_reason = s.get("blocked_reason", "")
            rows.append(f"""
            <tr>
              <td><code>{sid}</code></td>
              <td>{title}</td>
              <td><span class="badge" style="background:{color}">{emoji} {status}</span></td>
              <td>{priority}</td>
              <td>{owner}</td>
              <td><code>{branch}</code></td>
              {'<td class="blocker-reason">⚠️ ' + blocked_reason + '</td>' if blocked_reason else '<td>—</td>'}
            </tr>""")
        return "\n".join(rows) if rows else '<tr><td colspan="7" class="empty">None</td></tr>'

    def model_rows():
        rows = []
        for model, counts in metrics["model_breakdown"].items():
            cost = metrics["model_costs"].get(model, 0)
            rows.append(f"""
            <tr>
              <td>{model}</td>
              <td>{counts['input']:,}</td>
              <td>{counts['output']:,}</td>
              <td>${cost:.4f}</td>
            </tr>""")
        return "\n".join(rows) if rows else '<tr><td colspan="4" class="empty">No workspace data yet.</td></tr>'

    done_pct = metrics["done_pct"]
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="refresh" content="30">
  <title>Agentic SDLC Dashboard — {project_root}</title>
  <style>
    :root {{
      --bg: #0f1117; --surface: #1a1d27; --border: #2a2d3a;
      --text: #e2e8f0; --muted: #94a3b8; --accent: #6366f1;
      --green: #10b981; --red: #ef4444; --blue: #3b82f6; --yellow: #f59e0b;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: 'Inter', system-ui, sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; }}
    .header {{ background: var(--surface); border-bottom: 1px solid var(--border); padding: 1.5rem 2rem; display: flex; align-items: center; justify-content: space-between; }}
    .header h1 {{ font-size: 1.25rem; font-weight: 700; }}
    .meta {{ color: var(--muted); font-size: 0.8rem; }}
    .main {{ max-width: 1400px; margin: 0 auto; padding: 2rem; display: grid; gap: 1.5rem; }}
    .grid-4 {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; }}
    .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }}
    .card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 1.5rem; }}
    .card h2 {{ font-size: 0.75rem; font-weight: 600; text-transform: uppercase; color: var(--muted); margin-bottom: 1rem; }}
    .stat-card .value {{ font-size: 2.5rem; font-weight: 800; line-height: 1; }}
    .stat-card .label {{ font-size: 0.8rem; color: var(--muted); }}
    .progress-bar {{ height: 8px; background: var(--border); border-radius: 99px; overflow: hidden; margin-top: 10px; }}
    .progress-fill {{ height: 100%; background: linear-gradient(90deg, var(--accent), var(--green)); }}
    table {{ width: 100%; border-collapse: collapse; font-size: 0.875rem; }}
    th {{ text-align: left; padding: 0.6rem; color: var(--muted); border-bottom: 1px solid var(--border); }}
    td {{ padding: 0.75rem; border-bottom: 1px solid var(--border); }}
    code {{ background: rgba(255,255,255,0.06); padding: 0.1rem 0.4rem; border-radius: 4px; }}
    .badge {{ padding: 0.2rem 0.6rem; border-radius: 99px; font-size: 0.7rem; color: #fff; }}
    .token-highlight {{ background: linear-gradient(135deg, rgba(99,102,241,0.1), rgba(16,185,129,0.05)); border: 1px solid var(--border); border-radius: 12px; padding: 1.5rem; }}
    .tk-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }}
    .tk-val {{ font-size: 1.5rem; font-weight: 700; color: var(--accent); }}
    .tk-label {{ font-size: 0.75rem; color: var(--muted); }}
  </style>
</head>
<body>
<header class="header">
  <div>
    <h1>🤖 Agentic SDLC Dashboard</h1>
    <div class="meta">Project: {project_root} · Generated: {generated_at}</div>
  </div>
</header>
<main class="main">
  <div class="grid-4">
    <div class="card stat-card" style="border-top: 3px solid var(--green)">
      <div class="value" style="color:var(--green)">{sc.get('DONE', 0)}</div>
      <div class="label">Stories Done</div>
      <div class="progress-bar"><div class="progress-fill" style="width:{done_pct}%"></div></div>
    </div>
    <div class="card stat-card" style="border-top: 3px solid var(--blue)">
      <div class="value" style="color:var(--blue)">{sc.get('IN_PROGRESS', 0)}</div>
      <div class="label">In Progress</div>
    </div>
    <div class="card stat-card" style="border-top: 3px solid var(--red)">
      <div class="value" style="color:var(--red)">{sc.get('BLOCKED', 0)}</div>
      <div class="label">Blocked</div>
    </div>
    <div class="card stat-card" style="border-top: 3px solid var(--yellow)">
      <div class="value" style="color:var(--yellow)">${metrics['total_cost']:.3f}</div>
      <div class="label">Est. Cost (USD)</div>
    </div>
  </div>
  <div class="token-highlight">
    <h2>🤖 AI Token Usage</h2>
    <div class="tk-grid">
      <div><div class="tk-val">{metrics['total_tokens']:,}</div><div class="tk-label">Total Tokens</div></div>
      <div><div class="tk-val">{metrics['total_input']:,}</div><div class="tk-label">Input</div></div>
      <div><div class="tk-val">{metrics['total_output']:,}</div><div class="tk-label">Output</div></div>
      <div><div class="tk-val">{metrics['total_hitl']}</div><div class="tk-label">HITL</div></div>
      <div><div class="tk-val">{metrics['total_elapsed']}m</div><div class="tk-label">Time</div></div>
      <div><div class="tk-val">{metrics['workspace_count']}</div><div class="tk-label">Workspaces</div></div>
    </div>
  </div>
  <div class="grid-2">
    <div class="card">
      <h2>🔄 In Progress</h2>
      <table>
        <thead><tr><th>ID</th><th>Title</th><th>Status</th><th>Owner</th></tr></thead>
        <tbody>{story_rows(metrics['in_progress'])}</tbody>
      </table>
    </div>
    <div class="card">
      <h2>🚫 Blocked</h2>
      <table>
        <thead><tr><th>ID</th><th>Title</th><th>Status</th><th>Reason</th></tr></thead>
        <tbody>{story_rows(metrics['blockers'])}</tbody>
      </table>
    </div>
  </div>
</main>
</body></html>"""

class DashboardHandler(BaseHTTPRequestHandler):
    project_root = "."

    def do_GET(self):
        if self.path not in ("/", "/index.html"):
            self.send_response(404); self.end_headers(); return
        stories, workspaces = collect_data(self.project_root)
        metrics = compute_metrics(stories, workspaces)
        html = render_html(metrics, self.project_root, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

def serve(project_root, port):
    DashboardHandler.project_root = os.path.abspath(project_root)
    server = HTTPServer(("", port), DashboardHandler)
    print(f"🚀 Dashboard running at http://localhost:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
