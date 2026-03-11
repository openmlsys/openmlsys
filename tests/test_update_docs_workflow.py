from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "update_docs.yml"


class UpdateDocsWorkflowTests(unittest.TestCase):
    def test_workflow_uses_official_pages_actions_and_page_variables(self) -> None:
        workflow = WORKFLOW_PATH.read_text(encoding="utf-8")

        self.assertIn("uses: actions/configure-pages@v5", workflow)
        self.assertIn("uses: actions/upload-pages-artifact@v4", workflow)
        self.assertIn("uses: actions/deploy-pages@v4", workflow)
        self.assertIn("url: ${{ steps.deployment.outputs.page_url }}", workflow)
        self.assertIn("${{ steps.pages.outputs.base_url }}", workflow)
        self.assertNotIn("git clone https://x-access-token:${DEPLOY_TOKEN}", workflow)


if __name__ == "__main__":
    unittest.main()
