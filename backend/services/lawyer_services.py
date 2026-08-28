from config.db import lawyers_collection, ratings_collection, mentorship_collection
from models.lawyer import LawyerRegister, LawyerUpdate, RatingInput, MentorshipInput
from utils.auth import hash_password, verify_password, create_access_token
from services.maps_service import geocode_address, filter_lawyers_by_radius
from bson import ObjectId
from fastapi import HTTPException
from datetime import datetime


def serialize(doc) -> dict:
    """Convert MongoDB document to JSON-serializable dict."""
    doc["id"] = str(doc.pop("_id"))
    return doc


# ── Register ───────────────────────────────────────────────────────────────
async def register_lawyer(data: LawyerRegister) -> dict:
    # Check duplicate email or bar council id
    existing = await lawyers_collection.find_one({
        "$or": [{"email": data.email}, {"bar_council_id": data.bar_council_id}]
    })
    if existing:
        raise HTTPException(status_code=400, detail="Email or Bar Council ID already registered")

    # Geocode the address
    geo = await geocode_address(data.location.address, data.location.city, data.location.state)
    location_data = data.location.dict()
    location_data["latitude"] = geo["latitude"]
    location_data["longitude"] = geo["longitude"]

    lawyer_doc = {
        **data.dict(exclude={"password", "location"}),
        "location": location_data,
        "password": hash_password(data.password),
        "is_verified": False,           # Admin verifies Bar Council ID
        "reputation_score": 0.0,
        "total_ratings": 0,
        "avg_rating": 0.0,
        "response_time_score": 5.0,     # Default good score
        "mentorship_points": 0,
        "is_boosted": data.subscription in ["premium", "boosted"],
        "created_at": datetime.utcnow().isoformat(),
    }

    result = await lawyers_collection.insert_one(lawyer_doc)
    return {"message": "Lawyer registered successfully!", "lawyer_id": str(result.inserted_id)}


# ── Login ──────────────────────────────────────────────────────────────────
async def login_lawyer(email: str, password: str) -> dict:
    lawyer = await lawyers_collection.find_one({"email": email})
    if not lawyer or not verify_password(password, lawyer["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(lawyer["_id"]), "email": email})
    return {"access_token": token, "token_type": "bearer", "lawyer_id": str(lawyer["_id"])}


# ── Get Profile ────────────────────────────────────────────────────────────
async def get_lawyer_profile(lawyer_id: str) -> dict:
    lawyer = await lawyers_collection.find_one({"_id": ObjectId(lawyer_id)})
    if not lawyer:
        raise HTTPException(status_code=404, detail="Lawyer not found")
    lawyer.pop("password", None)
    return serialize(lawyer)


# ── Update Profile ─────────────────────────────────────────────────────────
async def update_lawyer_profile(lawyer_id: str, data: LawyerUpdate) -> dict:
    update_data = {k: v for k, v in data.dict().items() if v is not None}

    # Re-geocode if location is updated
    if "location" in update_data:
        loc = update_data["location"]
        geo = await geocode_address(loc.get("address", ""), loc.get("city", ""), loc.get("state", ""))
        update_data["location"]["latitude"] = geo["latitude"]
        update_data["location"]["longitude"] = geo["longitude"]

    await lawyers_collection.update_one(
        {"_id": ObjectId(lawyer_id)},
        {"$set": update_data}
    )
    return {"message": "Profile updated successfully!"}


# ── Search Lawyers ─────────────────────────────────────────────────────────
async def search_lawyers(city=None, specialization=None, max_fee=None,
                          language=None, latitude=None, longitude=None, radius_km=10.0) -> list:
    query = {}
    if city:
        query["location.city"] = {"$regex": city, "$options": "i"}
    if specialization:
        query["specializations"] = {"$in": [specialization]}
    if max_fee:
        query["fee_per_consultation"] = {"$lte": max_fee}
    if language:
        query["languages"] = {"$in": [language]}

    cursor = lawyers_collection.find(query, {"password": 0})
    lawyers = [serialize(doc) async for doc in cursor]

    # If user provides coordinates, filter by radius and sort by distance
    if latitude and longitude:
        lawyers = filter_lawyers_by_radius(lawyers, latitude, longitude, radius_km)
    else:
        # Sort: boosted first, then by reputation
        lawyers.sort(key=lambda x: (not x.get("is_boosted", False), -x.get("reputation_score", 0)))

    return lawyers


# ── Rate a Lawyer ──────────────────────────────────────────────────────────
async def rate_lawyer(data: RatingInput) -> dict:
    lawyer = await lawyers_collection.find_one({"_id": ObjectId(data.lawyer_id)})
    if not lawyer:
        raise HTTPException(status_code=404, detail="Lawyer not found")

    # Save the rating
    await ratings_collection.insert_one({
        "lawyer_id": data.lawyer_id,
        "client_name": data.client_name,
        "rating": data.rating,
        "review": data.review,
        "created_at": datetime.utcnow().isoformat(),
    })

    # Recalculate average rating
    total = lawyer.get("total_ratings", 0) + 1
    avg = ((lawyer.get("avg_rating", 0) * (total - 1)) + data.rating) / total

    # Update reputation score (weighted: 60% rating, 40% response time)
    reputation = round((avg * 0.6) + (lawyer.get("response_time_score", 5) * 0.4), 2)

    await lawyers_collection.update_one(
        {"_id": ObjectId(data.lawyer_id)},
        {"$set": {"total_ratings": total, "avg_rating": round(avg, 2), "reputation_score": reputation}}
    )
    return {"message": "Rating submitted!", "new_avg_rating": round(avg, 2), "reputation_score": reputation}


# ── Mentorship Contribution ────────────────────────────────────────────────
async def add_mentorship(data: MentorshipInput) -> dict:
    await mentorship_collection.insert_one({
        **data.dict(),
        "created_at": datetime.utcnow().isoformat()
    })

    # +5 reputation points per mentorship session
    await lawyers_collection.update_one(
        {"_id": ObjectId(data.lawyer_id)},
        {"$inc": {"mentorship_points": 5, "reputation_score": 0.5}}
    )
    return {"message": "Mentorship session recorded! +5 reputation points earned."}


# ── Boost Profile (Premium) ────────────────────────────────────────────────
async def boost_profile(lawyer_id: str) -> dict:
    await lawyers_collection.update_one(
        {"_id": ObjectId(lawyer_id)},
        {"$set": {"is_boosted": True, "subscription": "boosted"}}
    )
    return {"message": "Profile boosted! You now appear at the top of search results."}
