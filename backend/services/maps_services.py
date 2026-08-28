import httpx
from math import radians, sin, cos, sqrt, atan2


# ── Geocoding via OpenStreetMap Nominatim (no API key needed) ──────────────
async def geocode_address(address: str, city: str, state: str) -> dict:
    """Convert a text address into lat/lng coordinates."""
    query = f"{address}, {city}, {state}, India"
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": query,
        "format": "json",
        "limit": 1,
        "countrycodes": "in",
    }
    headers = {"User-Agent": "LegalMind/1.0 (legalmind@example.com)"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=headers, timeout=10)
        results = response.json()

    if not results:
        return {"latitude": None, "longitude": None, "display_name": None}

    result = results[0]
    return {
        "latitude": float(result["lat"]),
        "longitude": float(result["lon"]),
        "display_name": result.get("display_name"),
    }


# ── Reverse geocoding: coordinates → address ───────────────────────────────
async def reverse_geocode(latitude: float, longitude: float) -> str:
    """Convert lat/lng back to a human-readable address."""
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {"lat": latitude, "lon": longitude, "format": "json"}
    headers = {"User-Agent": "LegalMind/1.0 (legalmind@example.com)"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=headers, timeout=10)
        result = response.json()

    return result.get("display_name", "Unknown location")


# ── Haversine distance formula ─────────────────────────────────────────────
def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance in km between two lat/lng points."""
    R = 6371  # Earth radius in km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))


# ── Filter lawyers within a radius ────────────────────────────────────────
def filter_lawyers_by_radius(lawyers: list, user_lat: float, user_lon: float, radius_km: float) -> list:
    """Return lawyers within radius_km of the user, sorted by distance."""
    nearby = []
    for lawyer in lawyers:
        loc = lawyer.get("location", {})
        lat = loc.get("latitude")
        lon = loc.get("longitude")
        if lat is None or lon is None:
            continue
        distance = haversine_distance(user_lat, user_lon, lat, lon)
        if distance <= radius_km:
            lawyer["distance_km"] = round(distance, 2)
            nearby.append(lawyer)
    return sorted(nearby, key=lambda x: x["distance_km"])


# ── NOTE: Switching to Google Maps later ──────────────────────────────────
# When you get a Google Maps API key, replace geocode_address with:
#
# import googlemaps
# gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))
#
# result = gmaps.geocode(f"{address}, {city}, {state}, India")
# lat = result[0]["geometry"]["location"]["lat"]
# lng = result[0]["geometry"]["location"]["lng"]
