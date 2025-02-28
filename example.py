from vanta import VantaAPI
import requests

# Initialize the API with client credentials
api = VantaAPI(client_id="YOUR_CLIENT_ID", client_secret="YOUR_CLIENT_SECRET")

try:
    # Get the first page of organizations (up to 50 items)
    params = {"pageSize": 50}
    organizations = api.get_organizations(params=params)
    print("Organizations (first page):", organizations)

    # Check if there are more pages and fetch the next page
    if organizations and "pageInfo" in organizations and organizations["pageInfo"].get("hasNextPage"):
        next_params = {"pageSize": 50, "pageCursor": organizations["pageInfo"]["endCursor"]}
        next_organizations = api.get_organizations(params=next_params)
        print("Next page of organizations:", next_organizations)

    # Alternatively, fetch all organizations at once using the new method
    all_organizations = api.get_all_organizations(page_size=50)
    print("All organizations:", all_organizations)

except requests.exceptions.HTTPError as e:
    print(f"API error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
