from config import db, ma
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

# User Table
class User(db.Model):
    __tablename__ = "USER"
    __table_args__ = {"schema": "CW2"}
    user_id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(255), nullable=False, unique=True)
    role = db.Column(db.String(50))

# Trail Table
class Trail(db.Model):
    __tablename__ = "TRAIL"
    __table_args__ = {"schema": "CW2"}

    trail_id = db.Column("TrailID", db.Integer, primary_key=True)
    name = db.Column("TrailName", db.String(255), nullable=False)
    summary = db.Column("TrailSummary", db.Text)
    description = db.Column("TrailDescription", db.Text)
    difficulty = db.Column("Difficulty", db.String(50))
    location = db.Column("Location", db.String(255))
    length = db.Column("Length", db.Float)
    elevation_gain = db.Column("ElevationGain", db.Float)
    route_type = db.Column("RouteType", db.String(100))
    owner_id = db.Column("OwnerID", db.Integer, db.ForeignKey("CW2.USER.UserID"))
    pt1_lat = db.Column("Pt1_Lat", db.Float)
    pt1_long = db.Column("Pt1_Long", db.Float)
    pt1_desc = db.Column("Pt1_Desc", db.Text)
    pt2_lat = db.Column("Pt2_Lat", db.Float)
    pt2_long = db.Column("Pt2_Long", db.Float)
    pt2_desc = db.Column("Pt2_Desc", db.Text)  

# Feature Table
class Feature(db.Model):
    __tablename__ = "FEATURE"
    __table_args__ = {"schema": "CW2"}
    trail_feature_id = db.Column(db.Integer, primary_key=True)
    trail_feature = db.Column(db.String(255), nullable=False)

# Trail Feature Table 
class TrailFeature(db.Model):
    __tablename__ = "TRAIL_FEATURE"
    __table_args__ = {"schema": "CW2"}
    trail_id = db.Column(db.Integer, db.ForeignKey("CW2.TRAIL.trail_id"), primary_key=True)
    trail_feature_id = db.Column(db.Integer, db.ForeignKey("CW2.FEATURE.trail_feature_id"), primary_key=True)

# Marshmallow Schemas
class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

class TrailSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Trail
        load_instance = True

class FeatureSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Feature
        load_instance = True

class TrailFeatureSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TrailFeature
        load_instance = True

# Instantiate schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)
trail_schema = TrailSchema()
trails_schema = TrailSchema(many=True)
feature_schema = FeatureSchema()
features_schema = FeatureSchema(many=True)
trail_feature_schema = TrailFeatureSchema()
trail_features_schema = TrailFeatureSchema(many=True)
