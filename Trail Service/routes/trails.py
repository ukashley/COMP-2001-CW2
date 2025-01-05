from flask import jsonify, request
from config import db
from models.trail import Trail, trail_schema, trails_schema
from routes.auth import verify_user, require_role
from models.trail import User  

@require_role("Admin")
def create_trail():
    data = request.json
    new_trail = Trail(
        name=data["name"],
        summary=data.get("summary", ""),
        description=data.get("description", ""),
        location=data["location"],
        owner_id=data["owner_id"],
    )
    db.session.add(new_trail)
    db.session.commit()
    return trail_schema.jsonify(new_trail), 201


def get_trails():
    try:
        # Fetch all trails from the database
        trails = Trail.query.all()
        serialized_trails = trails_schema.dump(trails)

        return jsonify(serialized_trails)
    except Exception as e:
        return jsonify({"error": f"Failed to fetch trails: {e}"}), 500

def get_trail(trail_id):
    """Retrieve a single trail by ID."""
    try:
        trail = Trail.query.get(trail_id)
        if not trail:
            return jsonify({"error": "Trail not found"}), 404
        return trail_schema.jsonify(trail), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch trail: {e}"}), 500

def create_trail():
    """Create a new trail."""
    try:
        data = request.json

        # Validate required fields
        if not data.get("name") or not data.get("location") or not data.get("owner_id"):
            return jsonify({"error": "Missing required fields: name, location, owner_id"}), 400

        # Verify the owner_id with the Authenticator API
        user = verify_user(data["owner_id"])
        if not user:
            return jsonify({"error": "Invalid owner ID"}), 400

        # Create the trail
        new_trail = Trail(
            name=data["name"],
            summary=data.get("summary", ""),
            description=data.get("description", ""),
            location=data["location"],
            owner_id=data["owner_id"]
        )
        db.session.add(new_trail)
        db.session.commit()
        return trail_schema.jsonify(new_trail), 201
    except Exception as e:
        return jsonify({"error": f"Failed to create trail: {e}"}), 500

def update_trail(trail_id):
    """Update an existing trail."""
    try:
        data = request.json

        # Find the trail
        trail = Trail.query.get(trail_id)
        if not trail:
            return jsonify({"error": "Trail not found"}), 404

        def verify_user(owner_id):
            return db.session.query(User).filter_by(user_id=owner_id).first()

        # Update the trail
        trail.name = data.get("name", trail.name)
        trail.summary = data.get("summary", trail.summary)
        trail.description = data.get("description", trail.description)
        trail.location = data.get("location", trail.location)
        trail.owner_id = data.get("owner_id", trail.owner_id)

        db.session.commit()
        return trail_schema.jsonify(trail), 200
    except Exception as e:
        return jsonify({"error": f"Failed to update trail: {e}"}), 500

def delete_trail(trail_id):
    """Delete a trail."""
    try:
        # Find the trail
        trail = Trail.query.get(trail_id)
        if not trail:
            return jsonify({"error": "Trail not found"}), 404

        # Delete the trail
        db.session.delete(trail)
        db.session.commit()
        return jsonify({"message": "Trail deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to delete trail: {e}"}), 500
