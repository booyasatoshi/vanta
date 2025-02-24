from vanta import VantaAPI

api = VantaAPI(api_key="YOUR_API_KEY")

try:
    # Get the first 50 organizations
    params = {"limit": 50}
    organizations = api.get_organizations(params=params)
    print("Organizations:", organizations)

    # If there are more pages, use 'starting_after' with the last ID
    if organizations.get("has_more"):
        last_id = organizations["data"][-1]["id"]
        next_params = {"limit": 50, "starting_after": last_id}
        next_organizations = api.get_organizations(params=next_params)
        print("Next page of organizations:", next_organizations)
except requests.exceptions.HTTPError as e:
    print(f"API error: {e}")