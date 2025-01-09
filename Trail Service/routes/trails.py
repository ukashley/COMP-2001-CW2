from flask import Blueprint, jsonify, request
from config import db
from models.trail import Trail, User, trail_schema, trails_schema
from sqlalchemy.exc import SQLAlchemyError

trail_bp = Blueprint("trail_bp", __name__)

@trail_bp.route('/trails', methods=['POST'])
def create_trail():
    """
    Create a new trail. For Admins Only
    """
    try:
        user_email = request.headers.get("user_email")
        if not user_email:
            return jsonify({"error": "Missing user_email in headers"}), 400

        # Fetching users and verifying their roles
        user = User.query.filter_by(Email_Address=user_email).first()
        if not user or user.Role != "Admin":
            return jsonify({"error": "Disallowed: Only admins can create"}), 403

        data = request.json

        # Validation of required fields
        required_fields = ['trail_name', 'location', 'owner_id']
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

        # Create a new trail
        new_trail = Trail(
            name=data.get('trail_name'),
            location=data.get('location'),
            owner_id=data.get('owner_id'),
            summary=data.get('summary', ""),
            description=data.get('description', ""),
            difficulty=data.get('difficulty'),
            length=data.get('length'),
            elevation_gain=data.get('elevation_gain'),
            route_type=data.get('route_type'),
            pt1_lat=data.get('pt1_lat'),
            pt1_long=data.get('pt1_long'),
            pt1_desc=data.get('pt1_desc'),
            pt2_lat=data.get('pt2_lat'),
            pt2_long=data.get('pt2_long'),
            pt2_desc=data.get('pt2_desc')
        )

        db.session.add(new_trail)
        db.session.commit()

        return jsonify(trail_schema.dump(new_trail)), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@trail_bp.route('/trails', methods=['GET'])
def get_trails():
    """
    Retrieve all trails. For Admins only.
    """
    try:
        user_email = request.headers.get("user_email")
        if not user_email:
            return jsonify({"error": "Missing user_email in headers"}), 400

        user = User.query.filter_by(Email_Address=user_email).first()
        if not user:
            return jsonify({"error": "Invalid user_email"}), 403

        if user.Role == "Admin":
            trails = Trail.query.all()
            return jsonify(trails_schema.dump(trails)), 200
        else:
            trails = Trail.query.with_entities(
                Trail.id, Trail.name, Trail.summary, Trail.location, Trail.length
            ).all()
            return jsonify(
                [{"id": t.id, "name": t.name, "summary": t.summary, "location": t.location, "length": t.length} for t in trails]
            ), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch trails: {e}"}), 500

@trail_bp.route('/trails/<int:trail_id>', methods=['GET'])
def get_trail(trail_id):
    """
    Retrieve a single trail by ID. 
    """
    try:
        # Get user_email from headers
        user_email = request.headers.get('user_email')
        if not user_email:
            return jsonify({"error": "Missing user_email in headers"}), 400

        # Verify the user
        user = User.query.filter_by(Email_Address=user_email).first()
        if not user:
            return jsonify({"error": "Invalid user_email"}), 403

        # Fetch the trail
        trail = Trail.query.get(trail_id)
        if not trail:
            return jsonify({"error": "Trail not found"}), 404

        # Check the user's role
        if user.Role == "Admin":
            # Admin can view all trail details
            return jsonify(trail_schema.dump(trail)), 200
        else:
            # Regular users can view limited trail details
            limited_trail = {
                "name": trail.name,
                "summary": trail.summary,
                "location": trail.location,
                "length": trail.length
            }
            return jsonify(limited_trail), 200

    except SQLAlchemyError as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@trail_bp.route('/trails/<int:trail_id>', methods=['PUT'])
def update_trail(trail_id):
    """
    Update an existing trail. For Admins only.
    """
    try:
        user_email = request.headers.get("user_email")
        if not user_email:
            return jsonify({"error": "Missing user_email in headers"}), 400

        user = User.query.filter_by(Email_Address=user_email).first()
        if not user or user.Role != "Admin":
            return jsonify({"error": "Disallowed: Only admins can update trails"}), 403

        data = request.json
        trail = Trail.query.get(trail_id)
        if not trail:
            return jsonify({"error": "Trail not found"}), 404
          # Update the trail fields
        trail.name = data.get("name", trail.name)
        trail.summary = data.get("summary", trail.summary)
        trail.description = data.get("description", trail.description)
        trail.location = data.get("location", trail.location)
        trail.owner_id = data.get("owner_id", trail.owner_id)
        db.session.commit()
        return jsonify(trail_schema.dump(trail)), 200

    except Exception as e:
        return jsonify({"error": f"Failed to update trail: {e}"}), 500

@trail_bp.route('/trails/<int:trail_id>', methods=['DELETE'])
def delete_trail(trail_id):
    """
    Delete a trail. For Admins Only
    """
    try:
        user_email = request.headers.get("user_email")
        if not user_email:
            return jsonify({"error": "Missing user_email in headers"}), 400

        user = User.query.filter_by(Email_Address=user_email).first()
        if not user or user.Role != "Admin":
            return jsonify({"error": "Disallowed: Only admins can delete trails"}), 403

        trail = Trail.query.get(trail_id)
        if not trail:
            return jsonify({"error": "Trail not found"}), 404

        db.session.delete(trail)
        db.session.commit()
        return jsonify({"message": "Trail deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": f"Failed to delete trail: {e}"}), 500
