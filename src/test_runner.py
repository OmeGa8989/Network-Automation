from .api_client import ApiClient
from .mocks import MockSSH, MockRDP
import sys
import json

class TestRunner:
    def __init__(self, config):
        self.config = config
        self.api = ApiClient(config.get('api.base_url'), config.get('api.timeout'))
        self.ssh = MockSSH()
        self.rdp = MockRDP()
        self.context = {} # Store data between steps

    def setup(self):
        username = self.config.get('auth.username')
        password = self.config.get('auth.password')
        register_endpoint = self.config.get('api.endpoints.register')
        login_endpoint = self.config.get('api.endpoints.login')

        print("--- Setup Phase ---")
        # Try to register first (ignore error if already exists, or handle it)
        # In a real framework, we might check if user exists or use a flag
        self.api.register(register_endpoint, username, password)
        
        if not self.api.login(login_endpoint, username, password):
            print("Critical: Failed to login. Aborting tests.")
            sys.exit(1)
        
        # Initialize mocks
        self.ssh.connect("mock-host-ssh")
        self.rdp.connect("mock-host-rdp")
        print("Setup complete.\n")

    def run(self):
        workflow = self.config.get('workflow')
        for stage in workflow:
            print(f"=== Executing Stage: {stage['stage']} ===")
            print(f"Description: {stage['description']}")
            
            for step in stage['steps']:
                self._execute_step(step)
            print("Stage complete.\n")

    def _execute_step(self, step):
        action = step['action']
        
        if action == "fetch_all":
            self._fetch_all(step)
        elif action == "validate_attribute":
            self._validate_attribute(step)
        elif action == "update_resource":
            self._update_resource(step)
        else:
            print(f"Unknown action: {action}")

    def _fetch_all(self, step):
        resource = step['resource']
        endpoint = self.config.get(f'api.endpoints.{resource}')
        print(f"Fetching all {resource}s...")
        
        data = self.api.get(endpoint)
        if data is not None:
            # Handle list or dict with results
            items_list = data
            if isinstance(data, dict):
                # Common patterns: results, items, data
                for key in ['results', 'items', 'data']:
                    if key in data and isinstance(data[key], list):
                        items_list = data[key]
                        break
            
            # The API returns a list of objects.
            # Task: "Log the counts or names of each"
            count = len(items_list) if isinstance(items_list, list) else 0
            print(f"Fetched {count} items.")
            self.context[f"{resource}_list"] = items_list
            
            # Print names for visibility
            if isinstance(items_list, list):
                names = [item.get('name', 'Unknown') for item in items_list]
                print(f"Names: {', '.join(names[:5])}..." if len(names) > 5 else f"Names: {', '.join(names)}")

    def _validate_attribute(self, step):
        resource = step['resource']
        identifier_key = step['identifier_key']
        identifier_value = step['identifier_value']
        attribute = step['attribute']
        expected_value = step['expected_value']

        # Find the UUID from the context or fetch again
        item = self._find_item(resource, identifier_key, identifier_value)
        if not item:
            print(f"Error: Could not find {resource} with {identifier_key}={identifier_value}")
            return

        # Use uuid or id
        uuid = item.get('uuid', item.get('id'))
        if not uuid:
             print(f"Error: Item found but has no uuid/id")
             return

        endpoint = f"{self.config.get(f'api.endpoints.{resource}')}/{uuid}"
        
        # Fetch fresh data
        data = self.api.get(endpoint)
        if data:
            actual_value = data.get(attribute)
            if actual_value == expected_value:
                print(f"Validation SUCCESS: {attribute} is {actual_value}")
            else:
                print(f"Validation FAILED: Expected {attribute} to be {expected_value}, got {actual_value}")

    def _update_resource(self, step):
        resource = step['resource']
        identifier_key = step['identifier_key']
        identifier_value = step['identifier_value']
        payload = step['payload']

        item = self._find_item(resource, identifier_key, identifier_value)
        if not item:
            print(f"Error: Could not find {resource} with {identifier_key}={identifier_value}")
            return

        uuid = item.get('uuid', item.get('id'))
        if not uuid:
             print(f"Error: Item found but has no uuid/id")
             return

        endpoint = f"{self.config.get(f'api.endpoints.{resource}')}/{uuid}"
        
        print(f"Updating {resource} {uuid} with payload: {payload}")
        data = self.api.put(endpoint, payload)
        if data:
            print("Update request successful.")
            # Verify update in response if possible
            if all(data.get(k) == v for k, v in payload.items()):
                 print("Update verified in response.")

    def _find_item(self, resource, key, value):
        # Look in context first
        items = self.context.get(f"{resource}_list")
        if not items:
            # Try to fetch if not in context
            endpoint = self.config.get(f'api.endpoints.{resource}')
            items = self.api.get(endpoint)
            self.context[f"{resource}_list"] = items
        
        if items and isinstance(items, list):
            for item in items:
                if item.get(key) == value:
                    return item
        return None
