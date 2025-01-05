from config import db, app
from routes.trails import Trail

# Define the new trail
new_trail = Trail(
    name="Test Trail",
    summary="A test summary.",
    description="A detailed description.",
    difficulty="Moderate",
    location="Test Location",
    length=5.0,
    elevation_gain=100,
    route_type="Loop",
    owner_id=1,
    pt1_lat=40.5678,
    pt1_long=-74.9876,
    pt1_desc="Start Point",
    pt2_lat=40.6789,
    pt2_long=-74.5432,
    pt2_desc="End Point"
)

# Use the application context
with app.app_context():
    db.session.add(new_trail)
    db.session.commit()
    print("Trail added successfully.")
