from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "update_docs.yml"
CI_WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "main.yml"


class UpdateDocsWorkflowTests(unittest.TestCase):
    def test_workflow_deploys_to_openmlsys_github_io(self) -> None:
        workflow = WORKFLOW_PATH.read_text(encoding="utf-8")

        self.assertIn("DEPLOY_TOKEN", workflow)
        self.assertIn("openmlsys.github.io", workflow)
        self.assertIn("git push", workflow)

    def test_workflows_use_peaceiris_mdbook_action(self) -> None:
        for workflow_path in (WORKFLOW_PATH, CI_WORKFLOW_PATH):
            workflow = workflow_path.read_text(encoding="utf-8")
            self.assertIn("uses: peaceiris/actions-mdbook@v2", workflow, workflow_path.as_posix())
            self.assertIn("mdbook-version: 'latest'", workflow, workflow_path.as_posix())
            self.assertNotIn("cargo install mdbook --locked", workflow, workflow_path.as_posix())


if __name__ == "__main__":
    unittest.main()
