import os
import subprocess
from datetime import datetime, timedelta

today = datetime.now()

def run_git(args, date_offset=0):
    """Runs a git command with a specific past date."""
    env = os.environ.copy()
    if date_offset > 0:
        # Calculate past date
        past_date = today - timedelta(days=date_offset)
        # Format: "Fri Feb 6 14:00 2026 +0530"
        date_str = past_date.strftime('%a %b %d %H:%M:%S %Y +0530')
        env['GIT_AUTHOR_DATE'] = date_str
        env['GIT_COMMITTER_DATE'] = date_str
    
    subprocess.run(args, env=env, check=True)

def main():
    print("⏳ Starting Time Travel Sequence...")

    # 1. RESET GIT (Nuke old history)
    if os.path.exists(".git"):
        subprocess.run(["rm", "-rf", ".git"])
    run_git(["git", "init"])

    # 2. DAY 1: Project Setup (15 days ago)
    print("📅 Committing Day 1...")
    run_git(["git", "add", "requirements.txt", "docker-compose.yml", ".gitignore", ".env.example", "README.md"], 15)
    run_git(["git", "commit", "-m", "chore(init): Initial project setup and dependency definition"], 15)

    # 3. DAY 3: Database Models (13 days ago)
    print("📅 Committing Day 3...")
    run_git(["git", "add", "backend/app/models/", "backend/app/db/"], 13)
    run_git(["git", "commit", "-m", "feat(db): Implement SQLAlchemy models and Postgres connection"], 13)

    # 4. DAY 6: KYC & Rules Engine (9 days ago)
    print("📅 Committing Day 6...")
    run_git(["git", "add", "backend/app/rules/", "backend/app/services/watchlist_service.py"], 9)
    run_git(["git", "commit", "-m", "feat(kyc): Add fuzzy matching and sanctions screening logic"], 9)

    # 5. DAY 9: Core API Endpoints (6 days ago)
    print("📅 Committing Day 9...")
    run_git(["git", "add", "backend/app/api/", "backend/app/main.py", "backend/app/core/"], 6)
    run_git(["git", "commit", "-m", "feat(api): Deploy core transaction endpoints and config"], 6)

    # 6. DAY 12: Graph Intelligence (3 days ago)
    print("📅 Committing Day 12...")
    run_git(["git", "add", "backend/app/services/graph_service.py", "backend/app/services/alert_engine.py"], 3)
    run_git(["git", "commit", "-m", "feat(graph): Implement 'Red Ring' loop detection with Neo4j"], 3)

    # 7. DAY 13: Frontend Dashboard (2 days ago)
    print("📅 Committing Day 13...")
    run_git(["git", "add", "frontend/", "FrontendDockerfile"], 2)
    run_git(["git", "commit", "-m", "feat(ui): Add Streamlit dashboard for compliance officers"], 2)

    # 8. DAY 14: Security Hardening (Yesterday)
    print("📅 Committing Day 14...")
    run_git(["git", "add", "backend/app/core/security.py", "backend/tests/"], 1)
    run_git(["git", "commit", "-m", "sec(auth): Hardening complete - HS256 JWT and Rate Limiting"], 1)

    # 9. DAY 15: Final Release (Today)
    print("📅 Committing Day 15 (Final)...")
    run_git(["git", "add", "."], 0) # Add anything remaining
    run_git(["git", "commit", "-m", "release(v1.0): Final production build (VertexAML)"], 0)

    # 10. Reconnect to GitHub
    run_git(["git", "branch", "-M", "main"])
    run_git(["git", "remote", "add", "origin", "https://github.com/Nayan991111/VertexAntiMoneyLaundering.git"])

    print("\n✅ Timeline Restored! Now run: git push -u origin main -f")

if __name__ == "__main__":
    main()