# Python Async Worker Sample

This repository contains a simplified example of a common bug encountered in asynchronous programming, specifically related to state management and resource handling during error conditions. It serves as a demonstration of how such a bug might manifest and how it can be documented and fixed, similar to a real-world workflow using GitHub Issues and Pull Requests.

**Disclaimer:** This code is a minimal, illustrative example and not intended for production use. The simulated external service and task processing are simplified to highlight the specific bug.

## Repository
https://github.com/Bruce-Moe/build-demo-2025

## Purpose

The goal of this project is to demonstrate:

1.  A potential logical bug in an asynchronous Python application involving state inconsistency after an error.
2.  How this bug can lead to unexpected behavior (a worker becoming unresponsive).
3.  How such an issue might be reported in a platform like GitHub Issues.
4.  How the fix addresses the root cause of the bug.

## Files

* `worker.py`: Contains the initial code with the bug.
* `worker_fixed.py`: Contains the corrected code with the bug resolved.

## Setup

This project requires Python 3.7 or higher for the `asyncio.run()` function. No external libraries are needed.

1.  Clone this repository (or copy the files):
    ```bash
    git clone <repository_url>
    cd python-async-worker-bug-example # Replace with the actual directory name
    ```

## Running the Buggy Code (Observing the Bug)

The buggy code in `worker.py` demonstrates the worker becoming unresponsive after a task failure.

1.  Run the buggy script:
    ```bash
    python worker.py
    ```

2.  Observe the output:
    * You will see tasks starting and potentially some simulating failure (`Simulating failure...`).
    * After the initial batch of tasks completes, the script attempts to run one more task (`task_F`).
    * Due to the bug, the worker is stuck in an `_is_processing = True` state.
    * The output for `task_F` will likely show: `Worker: Warning: Worker is already processing task ... Skipping task task_F.`
    * The final worker state will show `_is_processing=True`, even though all initial tasks are done and the connection is released.

This demonstrates the worker becoming unresponsive to new tasks after an error.

## Running the Fixed Code (Verifying the Fix)

The fixed code in `worker_fixed.py` resolves the state inconsistency bug.

1.  Run the fixed script:
    ```bash
    python worker_fixed.py
    ```

2.  Observe the output:
    * Similar to the buggy version, tasks will run, and some might fail.
    * However, after the initial batch completes, the script attempts to run `task_F`.
    * The fixed worker correctly resets its state after each task (in the `finally` block).
    * `task_F` will now be processed as expected, acquiring the service connection again.
    * The final worker state will show `_is_processing=False`, indicating it's ready for more tasks.

## The Bug Explained

*(This section summarizes the bug as you would see it documented, potentially in a GitHub Issue).*

**Summary:** The asynchronous worker fails to reset its internal `_is_processing` and `_active_task` state flags when a task encounters an error during processing by the simulated `ExternalService`.

**Details:** The `process_task` method sets `_is_processing` to `True` at the start. If an exception occurs within the `try` block (e.g., the simulated `RuntimeError` from the service), the `except` block catches it, and the `finally` block executes to release the service connection. However, the crucial step of resetting `_is_processing` and `_active_task` back to their idle states (`False` and `None`) was missing in the error path. This left the worker in a perpetually "busy" state, preventing it from accepting any subsequent tasks, even though no processing was actively occurring.

**Corresponding GitHub Issue (Conceptual):**

This bug could be reported in a GitHub issue like this one:
