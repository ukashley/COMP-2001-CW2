from flask import Blueprint, jsonify, request
from config import db
from models.trail import Trail, User, trail_schema, trails_schema
from routes.auth import verify_user
from sqlalchemy.exc import SQLAlchemyError

trail_bp = Blueprint("trail_bp", __name__)

@trail_bp.route('/trails', methods=['POST'])
def create_trail():
    """
    Create a new trail.
    """
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['trail_name', 'location', 'owner_id']
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

        # Verify owner ID using the authenticator API
        user = verify_user(data['owner_id'])
        if not user:
            return jsonify({"error": "Invalid owner ID or authentication failed"}), 400

        # Create a new trail
        new_trail = Trail(
            name=data.get('trail_name'),
            location=data.get('location'),
            owner_id=data.get('owner_id'),
            summary=data.get('summary', ""),
            description=data.get('description', ""),
            difficulty=data.get('difficulty', "Moderate"),
            length=data.get('length', 0.0),
            elevation_gain=data.get('elevation_gain', 0.0),
            route_type=data.get('route_type', "Unknown"),
            pt1_lat=data.get('pt1_lat'),
            pt1_long=data.get('pt1_long'),
            pt1_desc=data.get('pt1_desc'),
            pt2_lat=data.get('pt2_lat'),
            pt2_long=data.get('pt2_long'),
            pt2_desc=data.get('pt2_desc')
        )
        
        # Add to the database
        db.session.add(new_trail)
        db.session.commit()

        return jsonify(trail_schema.dump(new_trail)), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except ValueError as e:
        return jsonify({"error": f"Value error: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


def get_trails():
    try:
        # Fetch all trails from the database
        trails = Trail.query.all()

        # Serialize the trails using Marshmallow
        serialized_trails = trails_schema.dump(trails)

        # Use Flask's jsonify to return the serialized data
        return jsonify(serialized_trails), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch trails: {e}"}), 500


def get_trail(trail_id):
    """Retrieve a single trail by ID."""
    try:
        trail = Trail.query.get(trail_id)
        if not trail:
            return jsonify({"error": "Trail not found"}), 404

        # Serialize the trail using Marshmallow
        serialized_trail = trail_schema.dump(trail)

        # Use Flask's jsonify to return the serialized data
        return jsonify(serialized_trail), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch trail: {e}"}), 500

def update_trail(trail_id):
    """Update an existing trail."""
    try:
        data = request.json

        # Find the trail
        trail = Trail.query.get(trail_id)
        if not trail:
            return jsonify({"error": "Trail not found"}), 404

        # Update the trail fields
        trail.name = data.get("name", trail.name)
        trail.summary = data.get("summary", trail.summary)
        trail.description = data.get("description", trail.description)
        trail.location = data.get("location", trail.location)
        trail.owner_id = data.get("owner_id", trail.owner_id)

        # Commit the updates to the database
        db.session.commit()

        # Serialize the updated trail
        serialized_trail = trail_schema.dump(trail)

        # Use Flask's jsonify to return the serialized data
        return jsonify(serialized_trail), 200
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

        # Return a success message
        return jsonify({"message": "Trail deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to delete trail: {e}"}), 500
