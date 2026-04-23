"""
GitHub Pages Deployer — pushes CA prediction reports to a GitHub Pages site.

Maintains a local git repo at C:\\exam_analyzer_data\\gh-pages-site\\
that is synced to a GitHub repository's gh-pages branch.
"""
import json
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

SITE_DIR = Path(r"C:\exam_analyzer_data\gh-pages-site")
DATA_DIR = SITE_DIR / "data"


def init_site_repo(github_repo_url: str) -> str:
    """Initialize or verify the local git repo for GitHub Pages.
    
    Args:
        github_repo_url: Full HTTPS or SSH URL of the GitHub repo.
                         e.g. "https://github.com/user/rbi-ca-predictions.git"
    
    Returns:
        Status message string.
    """
    SITE_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    git_dir = SITE_DIR / ".git"
    if not git_dir.exists():
        # First time setup
        _run_git(["init"], cwd=SITE_DIR)
        _run_git(["checkout", "-b", "gh-pages"], cwd=SITE_DIR)
        _run_git(["remote", "add", "origin", github_repo_url], cwd=SITE_DIR)
        # Create initial .nojekyll to disable Jekyll processing
        (SITE_DIR / ".nojekyll").touch()
        return "Repository initialized. Ready to deploy."
    else:
        # Verify remote
        result = _run_git(["remote", "get-url", "origin"], cwd=SITE_DIR)
        current_remote = result.strip()
        if current_remote != github_repo_url:
            _run_git(["remote", "set-url", "origin", github_repo_url], cwd=SITE_DIR)
            return f"Remote updated from {current_remote} to {github_repo_url}"
        return f"Repository already configured. Remote: {current_remote}"


def deploy_site(analysis: dict, exam_name: str = "RBI Grade B", commit_msg: str = "") -> str:
    """Build the site and deploy to GitHub Pages.
    
    Args:
        analysis: Full analysis dict from ca_predictor.run_predictive_analysis()
        exam_name: Target exam name
        commit_msg: Custom commit message (auto-generated if empty)
    
    Returns:
        Status/result message.
    """
    if not (SITE_DIR / ".git").exists():
        return "Error: Repository not initialized. Call init_site_repo() first."
    
    # Step 1: Save analysis data as JSON
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save current analysis snapshot
    data_path = DATA_DIR / "latest_analysis.json"
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2, default=str)

    # Also save timestamped version for history
    history_path = DATA_DIR / f"analysis_{timestamp}.json"
    with open(history_path, "w", encoding="utf-8") as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2, default=str)
    
    # Step 2: Build the index.html
    from exporters.ca_site_builder import build_github_pages_site
    html_content = build_github_pages_site(analysis, exam_name)
    
    index_path = SITE_DIR / "index.html"
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    # Step 3: Git add, commit, push
    _run_git(["add", "-A"], cwd=SITE_DIR)
    
    if not commit_msg:
        facts = analysis.get("total_facts", 0)
        qs = analysis.get("total_questions", 0)
        commit_msg = f"Update: {facts} facts, {qs} MCQs — {datetime.now().strftime('%b %d, %Y %H:%M')}"
    
    try:
        _run_git(["commit", "-m", commit_msg], cwd=SITE_DIR)
    except RuntimeError as e:
        if "nothing to commit" in str(e):
            return "No changes to deploy. Site is up to date."
        raise
    
    try:
        _run_git(["push", "-u", "origin", "gh-pages", "--force"], cwd=SITE_DIR)
    except RuntimeError as e:
        return f"Committed locally but push failed: {e}\nYou may need to set up authentication (git credential manager or SSH key)."
    
    return f"Successfully deployed! Commit: {commit_msg}"


def get_site_status() -> dict:
    """Get the current status of the GitHub Pages site."""
    result = {
        "initialized": (SITE_DIR / ".git").exists(),
        "site_dir": str(SITE_DIR),
        "has_index": (SITE_DIR / "index.html").exists(),
        "remote_url": "",
        "last_commit": "",
        "pages_url": "",
    }
    
    if result["initialized"]:
        try:
            result["remote_url"] = _run_git(["remote", "get-url", "origin"], cwd=SITE_DIR).strip()
        except RuntimeError:
            result["remote_url"] = "(no remote configured)"
        
        try:
            log = _run_git(["log", "-1", "--format=%h %s (%ar)"], cwd=SITE_DIR).strip()
            result["last_commit"] = log
        except RuntimeError:
            result["last_commit"] = "(no commits yet)"
        
        # Derive GitHub Pages URL from remote
        remote = result["remote_url"]
        if "github.com" in remote:
            # https://github.com/user/repo.git -> https://user.github.io/repo/
            parts = remote.replace("https://github.com/", "").replace("git@github.com:", "").replace(".git", "").strip("/").split("/")
            if len(parts) >= 2:
                result["pages_url"] = f"https://{parts[0]}.github.io/{parts[1]}/"
    
    return result


def _run_git(args: list[str], cwd: Path = SITE_DIR) -> str:
    """Run a git command and return stdout. Raises RuntimeError on failure."""
    try:
        result = subprocess.run(
            ["git"] + args,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode != 0:
            raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
        return result.stdout
    except FileNotFoundError:
        raise RuntimeError("git is not installed or not in PATH")
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"git {' '.join(args)} timed out")
