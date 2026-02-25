# Complete Workflow Example

## Overview

End-to-end example of setting up a new Python project with UV.

## Setting Up a New Python Project

```bash
# 1. Create project directory
mkdir my-awesome-project
cd my-awesome-project

# 2. Initialize git
git init

# 3. Create .gitignore
cat > .gitignore << EOF
.venv/
__pycache__/
*.pyc
.pytest_cache/
.coverage
EOF

# 4. Create virtual environment
python -m venv .venv

# 5. Activate virtual environment
. .venv/Scripts/activate  # Windows Git Bash
# source .venv/bin/activate  # Linux/Mac

# 6. Install project dependencies
uv pip install requests fastapi uvicorn

# 7. Freeze dependencies
uv pip freeze > requirements.txt

# 8. Install development tools (globally with UV tool)
uv tool install black
uv tool install flake8
uv tool install mypy
uv tool install pytest

# 9. Create project structure
mkdir src tests
touch src/__init__.py
touch tests/__init__.py

# 10. Create main application
cat > src/main.py << EOF
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}
EOF

# 11. Create test
cat > tests/test_main.py << EOF
from src.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
EOF

# 12. Format code
black .

# 13. Lint code
flake8 src/ tests/

# 14. Run tests
pytest tests/

# 15. Create README
cat > README.md << EOF
# My Awesome Project

## Setup

\`\`\`bash
python -m venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
\`\`\`

## Run

\`\`\`bash
uvicorn src.main:app --reload
\`\`\`

## Test

\`\`\`bash
pytest tests/
\`\`\`
EOF

# 16. Commit
git add .
git commit -m "Initial project setup"

echo "Project setup complete!"
```

## What This Workflow Demonstrates

- Complete project initialization from scratch
- Git repository setup with proper .gitignore
- Virtual environment creation and activation
- Dependency management with UV
- Development tool installation
- Project structure creation
- Application and test code creation
- Code formatting and linting
- Test execution
- Documentation creation
- Initial git commit

## Related Documentation

- [Installation and Setup Reference](../references/installation-and-setup.md)
- [Tool Management](../references/tool-management.md)
- [Python Environment Management](../references/python-environment.md)
- [Virtual Environment Workflows](virtual-environments.md)
- [Development Workflows](development-workflows.md)
