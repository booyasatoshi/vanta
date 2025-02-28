import requests
from ratelimiter import RateLimiter

class VantaAPI:
    """
    A Python wrapper for the Vanta API, providing access to core endpoints for
    managing organizations, users, controls, evidence, and audits.

    Uses OAuth 2.0 client credentials for authentication.
    """

    def __init__(self, client_id, client_secret, base_url="https://api.vanta.com/v1"):
        """
        Initialize the VantaAPI client.

        :param client_id: Your Vanta API client ID
        :param client_secret: Your Vanta API client secret
        :param base_url: Base URL for the Vanta API (default: https://api.vanta.com/v1)
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = base_url
        self.rate_limiter = RateLimiter(max_calls=50, period=60)  # 50 requests/minute
        self.api_key = self._get_access_token()
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _get_access_token(self):
        """
        Retrieve an OAuth 2.0 access token using client credentials.

        :return: Access token string
        :raises requests.exceptions.HTTPError: If token retrieval fails
        """
        url = "https://api.vanta.com/oauth/token"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
            "scope": "vanta-api.all:read vanta-api.all:write"  # Adjust scope as needed
        }
        response = requests.post(url, json=data, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        return response.json()["access_token"]

    def _make_request(self, method, endpoint, data=None, params=None):
        """
        Internal method to make an HTTP request to the Vanta API.

        :param method: HTTP method (GET, POST, PUT, DELETE)
        :param endpoint: API endpoint (e.g., 'organizations')
        :param data: JSON data for POST or PUT requests (default: None)
        :param params: Query parameters for GET requests (default: None)
        :return: JSON response from the API or None for no-content responses
        :raises requests.exceptions.HTTPError: If the request fails
        """
        url = f"{self.base_url}/{endpoint}"
        with self.rate_limiter:
            try:
                response = requests.request(method, url, headers=self.headers, json=data, params=params)
                response.raise_for_status()
                return response.json() if response.content else None
            except requests.exceptions.HTTPError as e:
                if response.status_code == 401:  # Token expired
                    self.api_key = self._get_access_token()
                    self.headers["Authorization"] = f"Bearer {self.api_key}"
                    return self._make_request(method, endpoint, data, params)  # Retry
                elif response.status_code == 429:  # Rate limit exceeded
                    raise Exception("Rate limit exceeded. Please wait and retry.")
                else:
                    raise

    # Organizations
    def get_organizations(self, params=None):
        """
        List all organizations.

        :param params: Optional dictionary of query parameters, e.g., {"pageSize": 50, "pageCursor": "some_id"}
        :return: JSON response containing the list of organizations
        """
        return self._make_request("GET", "organizations", params=params)

    def get_all_organizations(self, page_size=100):
        """
        Fetch all organizations across all pages.

        :param page_size: Number of items per page (default: 100)
        :return: List of all organization data
        """
        params = {"pageSize": page_size}
        results = []
        while True:
            response = self._make_request("GET", "organizations", params=params)
            if not response or "data" not in response:
                break
            results.extend(response["data"])
            if "pageInfo" not in response or not response["pageInfo"].get("hasNextPage"):
                break
            params["pageCursor"] = response["pageInfo"]["endCursor"]
        return results

    def get_organization(self, org_id):
        """
        Get a specific organization by ID.

        :param org_id: The ID of the organization
        :return: JSON response containing the organization details
        """
        return self._make_request("GET", f"organizations/{org_id}")

    def create_organization(self, data):
        """
        Create a new organization.

        :param data: Dictionary containing organization data (e.g., {"name": "New Org"})
        :return: JSON response containing the created organization
        """
        return self._make_request("POST", "organizations", data=data)

    def update_organization(self, org_id, data):
        """
        Update an existing organization.

        :param org_id: The ID of the organization
        :param data: Dictionary containing updated organization data
        :return: JSON response containing the updated organization
        """
        return self._make_request("PUT", f"organizations/{org_id}", data=data)

    def delete_organization(self, org_id):
        """
        Delete an organization by ID.

        :param org_id: The ID of the organization
        :return: JSON response (if any) or None
        """
        return self._make_request("DELETE", f"organizations/{org_id}")

    # Users
    def get_users(self, params=None):
        """
        List all users.

        :param params: Optional dictionary of query parameters, e.g., {"pageSize": 50}
        :return: JSON response containing the list of users
        """
        return self._make_request("GET", "users", params=params)

    def get_all_users(self, page_size=100):
        """
        Fetch all users across all pages.

        :param page_size: Number of items per page (default: 100)
        :return: List of all user data
        """
        params = {"pageSize": page_size}
        results = []
        while True:
            response = self._make_request("GET", "users", params=params)
            if not response or "data" not in response:
                break
            results.extend(response["data"])
            if "pageInfo" not in response or not response["pageInfo"].get("hasNextPage"):
                break
            params["pageCursor"] = response["pageInfo"]["endCursor"]
        return results

    def get_user(self, user_id):
        """
        Get a specific user by ID.

        :param user_id: The ID of the user
        :return: JSON response containing the user details
        """
        return self._make_request("GET", f"users/{user_id}")

    def create_user(self, data):
        """
        Create a new user.

        :param data: Dictionary containing user data (e.g., {"email": "user@example.com"})
        :return: JSON response containing the created user
        """
        return self._make_request("POST", "users", data=data)

    def update_user(self, user_id, data):
        """
        Update an existing user.

        :param user_id: The ID of the user
        :param data: Dictionary containing updated user data
        :return: JSON response containing the updated user
        """
        return self._make_request("PUT", f"users/{user_id}", data=data)

    def delete_user(self, user_id):
        """
        Delete a user by ID.

        :param user_id: The ID of the user
        :return: JSON response (if any) or None
        """
        return self._make_request("DELETE", f"users/{user_id}")

    # Controls
    def get_controls(self, params=None):
        """
        List all controls.

        :param params: Optional dictionary of query parameters, e.g., {"pageSize": 50}
        :return: JSON response containing the list of controls
        """
        return self._make_request("GET", "controls", params=params)

    def get_all_controls(self, page_size=100):
        """
        Fetch all controls across all pages.

        :param page_size: Number of items per page (default: 100)
        :return: List of all control data
        """
        params = {"pageSize": page_size}
        results = []
        while True:
            response = self._make_request("GET", "controls", params=params)
            if not response or "data" not in response:
                break
            results.extend(response["data"])
            if "pageInfo" not in response or not response["pageInfo"].get("hasNextPage"):
                break
            params["pageCursor"] = response["pageInfo"]["endCursor"]
        return results

    def get_control(self, control_id):
        """
        Get a specific control by ID.

        :param control_id: The ID of the control
        :return: JSON response containing the control details
        """
        return self._make_request("GET", f"controls/{control_id}")

    def create_control(self, data):
        """
        Create a new control.

        :param data: Dictionary containing control data
        :return: JSON response containing the created control
        """
        return self._make_request("POST", "controls", data=data)

    def update_control(self, control_id, data):
        """
        Update an existing control.

        :param control_id: The ID of the control
        :param data: Dictionary containing updated control data
        :return: JSON response containing the updated control
        """
        return self._make_request("PUT", f"controls/{control_id}", data=data)

    def delete_control(self, control_id):
        """
        Delete a control by ID.

        :param control_id: The ID of the control
        :return: JSON response (if any) or None
        """
        return self._make_request("DELETE", f"controls/{control_id}")

    # Evidence
    def get_evidence(self, params=None):
        """
        List all evidence.

        :param params: Optional dictionary of query parameters, e.g., {"pageSize": 50}
        :return: JSON response containing the list of evidence
        """
        return self._make_request("GET", "evidence", params=params)

    def get_all_evidence(self, page_size=100):
        """
        Fetch all evidence across all pages.

        :param page_size: Number of items per page (default: 100)
        :return: List of all evidence data
        """
        params = {"pageSize": page_size}
        results = []
        while True:
            response = self._make_request("GET", "evidence", params=params)
            if not response or "data" not in response:
                break
            results.extend(response["data"])
            if "pageInfo" not in response or not response["pageInfo"].get("hasNextPage"):
                break
            params["pageCursor"] = response["pageInfo"]["endCursor"]
        return results

    def get_evidence_item(self, evidence_id):
        """
        Get a specific evidence item by ID.

        :param evidence_id: The ID of the evidence
        :return: JSON response containing the evidence details
        """
        return self._make_request("GET", f"evidence/{evidence_id}")

    def create_evidence(self, data):
        """
        Create new evidence.

        :param data: Dictionary containing evidence data
        :return: JSON response containing the created evidence
        """
        return self._make_request("POST", "evidence", data=data)

    def update_evidence(self, evidence_id, data):
        """
        Update existing evidence.

        :param evidence_id: The ID of the evidence
        :param data: Dictionary containing updated evidence data
        :return: JSON response containing the updated evidence
        """
        return self._make_request("PUT", f"evidence/{evidence_id}", data=data)

    def delete_evidence(self, evidence_id):
        """
        Delete evidence by ID.

        :param evidence_id: The ID of the evidence
        :return: JSON response (if any) or None
        """
        return self._make_request("DELETE", f"evidence/{evidence_id}")

    # Audits
    def get_audits(self, params=None):
        """
        List all audits.

        :param params: Optional dictionary of query parameters, e.g., {"pageSize": 50}
        :return: JSON response containing the list of audits
        """
        return self._make_request("GET", "audits", params=params)

    def get_all_audits(self, page_size=100):
        """
        Fetch all audits across all pages.

        :param page_size: Number of items per page (default: 100)
        :return: List of all audit data
        """
        params = {"pageSize": page_size}
        results = []
        while True:
            response = self._make_request("GET", "audits", params=params)
            if not response or "data" not in response:
                break
            results.extend(response["data"])
            if "pageInfo" not in response or not response["pageInfo"].get("hasNextPage"):
                break
            params["pageCursor"] = response["pageInfo"]["endCursor"]
        return results

    def get_audit(self, audit_id):
        """
        Get a specific audit by ID.

        :param audit_id: The ID of the audit
        :return: JSON response containing the audit details
        """
        return self._make_request("GET", f"audits/{audit_id}")

    def create_audit(self, data):
        """
        Create a new audit.

        :param data: Dictionary containing audit data
        :return: JSON response containing the created audit
        """
        return self._make_request("POST", "audits", data=data)

    def update_audit(self, audit_id, data):
        """
        Update an existing audit.

        :param audit_id: The ID of the audit
        :param data: Dictionary containing updated audit data
        :return: JSON response containing the updated audit
        """
        return self._make_request("PUT", f"audits/{audit_id}", data=data)

    def delete_audit(self, audit_id):
        """
        Delete an audit by ID.

        :param audit_id: The ID of the audit
        :return: JSON response (if any) or None
        """
        return self._make_request("DELETE", f"audits/{audit_id}")
