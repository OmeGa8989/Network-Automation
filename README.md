# Python Test Automation Framework

## Overview
This is a modular, configuration-driven Python test framework designed to interact with a mock load balancer API. It demonstrates dynamic configuration using YAML, parallel task execution concepts, and modular design.

## Structure
- `config/settings.yaml`: Contains API endpoints, credentials, and the test execution workflow definitions.
- `src/`: Source code directory.
  - `config_loader.py`: Handles YAML parsing.
  - `api_client.py`: Manages API connections, authentication, and requests.
  - `mocks.py`: Contains stubbed methods for SSH and RDP interactions.
  - `test_runner.py`: The core engine that parses the workflow and executes steps.
- `main.py`: Entry point for the framework.
- `requirements.txt`: Python dependencies.

## Prerequisites
- Python 3.x
- `requests` library
- `pyyaml` library

## Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration
1. Open `config/settings.yaml`.
2. Update the `auth` section with your desired username and password. The framework will attempt to register this user first, then login.
   ```yaml
   auth:
     username: "your_username"
     password: "your_password"
   ```
3. Ensure the `workflow` section matches your desired test steps.

## Execution
Run the main script:
```bash
python main.py
```

## Workflow Stages
The framework executes the following stages as defined in the task:
1. **Pre-Fetcher**: Fetches all virtual services and logs them.
2. **Pre-Validation**: Checks if the target Virtual Service (`backend-vs-t1r_1000-1`) is enabled (`enabled: true`).
3. **Task / Trigger**: Disables the Virtual Service (`enabled: false`).
4. **Post-Validation**: Verifies that the Virtual Service is now disabled.

## Logs
Output is printed to the console, showing the progress of each stage, API interactions, and mock SSH/RDP connection logs.
