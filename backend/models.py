from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(120), unique=False, nullable=False)

class Influencer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    instagram_handle = db.Column(db.String(50))
    instagram_follower_count = db.Column(db.Integer, default=0)  # Default to 0
    twitter_handle = db.Column(db.String(50))
    twitter_follower_count = db.Column(db.Integer, default=0)  # Default to 0
    youtube_channel_link = db.Column(db.String(100))
    youtube_subscriber_count = db.Column(db.Integer, default=0)  # Default to 0
    primary_content_categories = db.Column(db.String(255))
    description_of_content = db.Column(db.Text)
    links_to_portfolio_or_website = db.Column(db.String(255))
    profile_picture = db.Column(db.String(255), nullable=True)  # Path to profile picture
    isflagged = db.Column(db.Boolean, default=False)
    posts = db.relationship('InfluencerPosts', backref='influencer', lazy=True)
    ad_requests = db.relationship('AdRequest', backref='influencer', lazy=True)
    negotiations = db.relationship('Negotiation', backref='influencer', lazy=True)

class InfluencerPosts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.id'), nullable=False)
    post = db.Column(db.Text)
    media = db.Column(db.String(255), nullable=True)  # Path to media (image or video)
    created_at = db.Column(db.DateTime, default=db.func.now())

class Sponsor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    contact_number = db.Column(db.String(20))
    company_name = db.Column(db.String(100))
    company_website = db.Column(db.String(255))
    company_description = db.Column(db.Text)
    company_logo = db.Column(db.String(255), nullable=True) 
    contact_person = db.Column(db.String(255),nullable=True) 
    industry = db.Column(db.String(255))
    isflagged = db.Column(db.Boolean, default=False)

  

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    details = db.Column(db.Text, nullable=False)
    age_group = db.Column(db.String(50))
    gender = db.Column(db.String(50))
    budget = db.Column(db.Float, nullable=False)
    platform_youtube = db.Column(db.Boolean, default=False)
    platform_instagram = db.Column(db.Boolean, default=False)
    platform_twitter = db.Column(db.Boolean, default=False)
    visibility = db.Column(db.Boolean, default=True)  # Assuming visibility is a boolean
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.id'), nullable=False)  
    status = db.Column(db.String(50), default='pending')  # Default status to 'pending'
    # Relationship (if needed to access Company from Campaign)
    sponsor = db.relationship('Sponsor', backref=db.backref('campaigns', lazy=True))
    ad_requests = db.relationship('AdRequest', backref='campaign', lazy=True)
    isflagged = db.Column(db.Boolean, default=False)

class AdRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad_name = db.Column(db.String(255), nullable=False)
    ad_description = db.Column(db.Text, nullable=False)
    ad_terms = db.Column(db.Text, nullable=False)
    ad_payment = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    ad_platform = db.Column(db.String(50), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.id'), nullable=True)
    progress_percent = db.Column(db.String, default='0')  # Default to 0
    remarks = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default='pending')  # Default status to 'pending'
    negotiation = db.relationship('Negotiation', backref='ad_request', lazy=True)

class Negotiation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad_request_id = db.Column(db.Integer, db.ForeignKey('ad_request.id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.id'), nullable=False)
    status = db.Column(db.String(50), default='negotiating')  # Possible values: pending, accepted, rejected, negotiating
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())

    # Relationship
    messages = db.relationship('Message', backref='negotiation', lazy=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    negotiation_id = db.Column(db.Integer, db.ForeignKey('negotiation.id'), nullable=False)
    sender = db.Column(db.String(50), nullable=False)  # Possible values: sponsor, influencer
    content = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=db.func.now())
