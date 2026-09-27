"""Compile and run the trusted C++20 algorithm test binary."""
from __future__ import annotations

import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
BUILD = ROOT / "build" / "cpp"
BUILD.mkdir(parents=True, exist_ok=True)
binary = BUILD / ("algorithm_tests.exe" if os.name == "nt" else "algorithm_tests")
command = [
    os.environ.get("CP_LAB_CPP_COMPILER", "g++"), "-std=c++20", "-O2", "-Wall", "-Wextra",
    "-I", "algorithms/cpp/include", "algorithms/cpp/tests/test_algorithms.cpp",
    "-o", "build/cpp/algorithm_tests.exe" if os.name == "nt" else "build/cpp/algorithm_tests",
]
subprocess.run(command, check=True, cwd=ROOT)
completed = subprocess.run([str(binary.relative_to(ROOT))], check=True, text=True, capture_output=True, cwd=ROOT)
sys.stdout.write(completed.stdout)
