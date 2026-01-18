import os
import sys
from src.config_loader import ConfigLoader
from src.test_runner import TestRunner


def main():
    # Path to config file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, 'config', 'settings.yaml')

    print(f"Starting Python Test Automation Framework")
    print(f"Loading configuration from: {config_path}")

    try:
        config = ConfigLoader(config_path)
    except Exception as e:
        print(f"Failed to load configuration: {e}")
        sys.exit(1)

    runner = TestRunner(config)

    try:
        runner.setup()
        runner.run()
    except KeyboardInterrupt:
        print("\nTest execution interrupted.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
