"""
Lightweight smoke tests for domain agents.
Ensures agents execute locally without external calls and return a non-empty string.
"""

import unittest

from agents.ui_agent import run_agent as ui_run
from agents.core_agent import run_agent as core_run
from agents.fusion_agent import run_agent as fusion_run
from agents.cam_agent import run_agent as cam_run


class AgentSmokeTests(unittest.TestCase):
    def test_ui_agent_summary(self):
        output = ui_run({"query": ""})
        self.assertIsInstance(output, str)
        self.assertIn("UI/GUI", output)

    def test_core_agent_search(self):
        output = core_run({"query": "Application"})
        self.assertIn("Core", output)

    def test_fusion_agent_search(self):
        output = fusion_run({"query": "Extrude"})
        self.assertIn("Fusion", output)

    def test_cam_agent_search(self):
        output = cam_run({"query": "Operation"})
        self.assertIn("CAM", output)


if __name__ == "__main__":
    unittest.main()
