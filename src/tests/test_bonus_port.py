"""Test verifying bonus port to Inspect AI and DeepEval."""
import pytest
from eval.bonus_graders_port import verify_equivalence

def test_bonus_port_equivalence():
    verify_equivalence()
