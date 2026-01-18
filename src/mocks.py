import time

class MockSSH:
    def connect(self, host):
        print(f"MOCK_SSH: Connecting to host {host}...")
        time.sleep(0.5)
        print("MOCK_SSH: Connection established.")
        return True

    def execute_command(self, command):
        print(f"MOCK_SSH: Executing command: {command}")
        return "Command executed successfully"

class MockRDP:
    def connect(self, host):
        print(f"MOCK_RDP: Validating remote connection to {host}...")
        time.sleep(0.5)
        print("MOCK_RDP: Connection validated.")
        return True
