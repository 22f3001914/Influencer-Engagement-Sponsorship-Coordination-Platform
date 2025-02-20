from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
from flask import current_app as app
from .models import * 
import os
import qrcode
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

#App related routes
@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/')
def home():
    return render_template('landing.html')


# Admin Related Routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        flash('Incorrect username or password!', 'error')
        username = request.form.get('username')
        password = request.form.get('password')
        admin = Admin.query.filter_by(username=username).first()
        if not admin:
            print('User does not exit!')
            flash('User does not exit!', 'error')
            return redirect(url_for('admin_login'))
        elif admin.password != password:
            print("Incorrect password!")
            flash('Incorrect username or password!', 'error')
            return redirect(url_for('admin_login'))
        else:
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard', id=admin.id))

    return render_template('login-admin.html')


@app.route('/admin/<int:admin_id>/flag/<int:influencer_id>')
def flag_influencer(admin_id, influencer_id):
    influencer = Influencer.query.get(influencer_id)
    influencer.isflagged = True
    db.session.commit()
    flash('Influencer flagged successfully!', 'success')
    return redirect(url_for('admin_find', id=admin_id, ))


@app.route('/admin/<int:admin_id>/unflag/<int:influencer_id>')
def unflag_influencer(admin_id, influencer_id):
    influencer = Influencer.query.get(influencer_id)
    influencer.isflagged = False
    db.session.commit()
    flash('Influencer unflagged successfully!', 'success')
    return redirect(url_for('admin_dashboard', id=admin_id))

@app.route('/admin/<int:admin_id>/delete/<int:influencer_id>')
def delete_influencer(admin_id, influencer_id):
    posts = InfluencerPosts.query.filter_by(influencer_id=influencer_id).all()
    if posts:
        for post in posts:
            if post.media:
                os.remove(f'./static/uploads/{post.media}')
            db.session.delete(post)
    negotiations = Negotiation.query.filter_by(influencer_id=influencer_id).all()
    if negotiations:
        for negotiation in negotiations:
            messages = Message.query.filter_by(negotiation_id=negotiation.id).all()
            for message in messages:
                db.session.delete(message)
            db.session.delete(negotiation)
   
    ad_requests = AdRequest.query.filter_by(influencer_id=influencer_id).all()
    for ad_request in ad_requests:
        db.session.delete(ad_request)

    influencer = Influencer.query.get(influencer_id)
    db.session.delete(influencer)
    db.session.commit()
    flash('Influencer deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard', id=admin_id))


@app.route('/admin/<int:id>/dashboard')
def admin_dashboard(id):
    admin = Admin.query.get(id)
    campaigns = Campaign.query.all()
    influencers = Influencer.query.all()
    sponsors = Sponsor.query.all()
    ad_requests = AdRequest.query.all()
    return render_template('dashboard-admin.html', admin=admin, campaigns=campaigns, influencers=influencers, sponsors=sponsors, ad_requests=ad_requests)

@app.route('/admin/<int:id>/find')
def admin_find(id):
    admin = Admin.query.get(id)
    influencers = Influencer.query.all()
    campaigns = Campaign.query.all()
    return render_template('find-admin.html', admin=admin, influencers=influencers, campaigns=campaigns)
    # return render_template('find-admin.html')

@app.route('/admin/<int:id>/stats')
def admin_stats(id):
    admin = Admin.query.get(id)

    return render_template('stats-admin.html', admin=admin)

@app.route('/admin/<int:id>/logout', methods=['GET'])
def admin_logout(id):
    return redirect(url_for('home'))  

@app.route('/admin/<int:admin_id>/unflagcampaign/<int:campaign_id>', methods=['GET', 'POST'])
def unflag_campaign(admin_id, campaign_id):
    campaign = Campaign.query.get(campaign_id)
    campaign.isflagged = False
    db.session.commit()
    flash('Campaign unflagged successfully!', 'success')
    return redirect(url_for('admin_dashboard', id=admin_id))
@app.route('/admin/<int:admin_id>/flagcampaign/<int:campaign_id>', methods=['GET', 'POST'])
def flag_campaign(admin_id, campaign_id):
    campaign = Campaign.query.get(campaign_id)
    campaign.isflagged = True
    db.session.commit()
    flash('Campaign flagged successfully!', 'success')
    return redirect(url_for('admin_find', id=admin_id))

@app.route('/admin/<int:admin_id>/unflagsponsor/<int:sponsor_id>', methods=['GET', 'POST'])
def unflag_sponsor(admin_id, sponsor_id):
    sponsor = Sponsor.query.get(sponsor_id)
    sponsor.isflagged = False
    db.session.commit()
    flash('Sponsor unflagged successfully!', 'success')
    return redirect(url_for('admin_dashboard', id=admin_id))


# Sponsor Related Routes
@app.route('/register/sponsor', methods=['GET', 'POST'])
def sponsor_register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_repeat = request.form.get('password_repeat')
        industry = request.form.get('industry')
        contact_person = request.form.get('contact_person')
        contact_number = request.form.get('contact_number') 
        company_name = request.form.get('company_name')
        if password != password_repeat:
            flash('Passwords do not match!', 'error')
            print('Passwords do not match!',password, password_repeat)
            return redirect(url_for('sponsor_register'))
        sponsor = Sponsor(username=username, email=email, password =password,industry=industry,contact_person=contact_person, contact_number=contact_number, company_name=company_name)
        db.session.add(sponsor)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('sponsor_dashboard', sponsor_id=sponsor.id))
    return render_template('register-sponsor.html')

@app.route('/login/sponsor', methods=['GET', 'POST'])
def sponsor_login():
    if request.method == 'POST':
        flash('Incorrect username or password!', 'error')
        username = request.form.get('username')
        password = request.form.get('password')
        sponsor = Sponsor.query.filter_by(username=username).first()
        if not sponsor:
            print('User does not exit!')
            flash('User does not exit!', 'error')
            return redirect(url_for('sponsor_login'))
        elif sponsor.password != password:
            print("Incorrect password!")
            flash('Incorrect username or password!', 'error')
            return redirect(url_for('sponsor_login'))
        else:
            flash('Login successful!', 'success')
            return redirect(url_for('sponsor_dashboard', sponsor_id=sponsor.id))

    return render_template('login-sponsor.html')

@app.route('/sponsor/<int:id>/profilesettings', methods=['GET', 'POST'])
def update_sponsor_profile(id):
    sponsor = Sponsor.query.get(id)
    if request.method == 'POST':
        sponsor.username = request.form.get('username')
        sponsor.email = request.form.get('email')
        sponsor.contact_number = request.form.get('contact_number')
        sponsor.company_name = request.form.get('company_name')
        sponsor.company_website = request.form.get('company_website')
        sponsor.company_description = request.form.get('company_description')
        sponsor.contact_person = request.form.get('contact_person')
        sponsor.industry = request.form.get('industry')
        company_logo = request.files.get('company_logo')
        if company_logo:
            if sponsor.company_logo:
                os.remove(f'./static/uploads/{sponsor.company_logo}')
            company_logo.save(f'./static/uploads/{company_logo.filename}')
            sponsor.company_logo = company_logo.filename
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        print('Profile updated successfully!')
        return redirect(url_for('update_sponsor_profile', id=sponsor.id))
    return render_template('profile-setting-sponsor.html', sponsor=sponsor)

@app.route('/sponsor/<int:id>/profile')
def sponsor_profile(id):
    sponsor = Sponsor.query.get(id)
    return render_template('profile-sponsor.html', sponsor=sponsor)

@app.route('/sponsor/<int:sponsor_id>/dashboard')
def sponsor_dashboard(sponsor_id):
    sponsor = Sponsor.query.get(sponsor_id)
    return render_template('dashboard-sponsor.html', sponsor = sponsor)

@app.route('/sponsor/<int:sponsor_id>/find')
def sponsor_find(sponsor_id):
    sponsor = Sponsor.query.get(sponsor_id)
    campaigns = Campaign.query.all()
    influencers = Influencer.query.all()
    return render_template('find-sponsor.html', sponsor=sponsor, influencers=influencers, campaigns=campaigns)

@app.route('/sponsor/<int:sponsor_id>/stats')
def sponsor_stats(sponsor_id):
    sponsor = Sponsor.query.get(sponsor_id)
    return render_template('stats-sponsor.html', sponsor=sponsor)

@app.route('/campaign/<int:campaign_id>/ad')
def sponsor_ad_request(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    sponsor = campaign.sponsor
    return render_template('Ad-request-sponsor.html', campaign=campaign, sponsor=sponsor)


@app.route('/sponsor/<int:sponsor_id>/campaign', methods=['GET', 'POST'])  
def sponsor_campaigns(sponsor_id):
    if request.method == 'POST':
        name = request.form.get('campaign_name')
        details = request.form.get('campaign_details')
        age_group = request.form.get('age_group')
        gender = request.form.get('gender')
        budget = request.form.get('campaign_budget')
        # Assuming 'start_date' and 'end_date' are in 'YYYY-MM-DD' format
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')

        # Convert string dates to datetime.date objects
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None

        platforms = request.form.getlist('platforms')
        if 'youtube' in platforms:
            platform_youtube = True
        else:
            platform_youtube = False
        if 'instagram' in platforms:
            platform_instagram = True
        else:
            platform_instagram = False
        if 'twitter' in platforms:
            platform_twitter = True
        else:
            platform_twitter = False
        visibility = request.form.get('visibility')
        # campaign_images = request.files.getlist('campaign_images')
        if visibility == 'public':
            visibility = True
        else:
            visibility = False
        campaign = Campaign(name=name, details=details, age_group = age_group,gender = gender, budget = budget, platform_youtube = platform_youtube, platform_instagram = platform_instagram, platform_twitter = platform_twitter, visibility = visibility, sponsor_id = sponsor_id, start_date = start_date, end_date = end_date)
        db.session.add(campaign)
        db.session.commit()
        flash('Campaign added successfully!', 'success')
        return redirect(url_for('sponsor_campaigns', sponsor_id=sponsor_id))
    sponsor = Sponsor.query.get(sponsor_id)
    return render_template('campaigns-sponsor.html', sponsor=sponsor)


@app.route('/sponsor/<int:sponsor_id>/updatecampaign/<int:campaign_id>', methods=['GET', 'POST'])
def update_campaign(sponsor_id, campaign_id):
    campaign = Campaign.query.get(campaign_id)
    if request.method == 'POST':
        campaign.name = request.form.get('campaign_name')
        campaign.details = request.form.get('campaign_details')
        campaign.age_group = request.form.get('age_group')
        campaign.gender = gender = request.form.get('gender')
        campaign.budget = request.form.get('campaign_budget')
        platforms = request.form.getlist('platforms')
        if 'youtube' in platforms:
            campaign.platform_youtube = True
        else:
            campaign.platform_youtube = False
        if 'instagram' in platforms:
            campaign.platform_instagram = True
        else:
            campaign.platform_instagram = False
        if 'twitter' in platforms:
            campaign.platform_twitter = True
        else:
            campaign.platform_twitter = False
        if 'mvisibility' in request.form:
            campaign.visibility = False
        else:
            campaign.visibility = True
        db.session.commit()
        flash('Campaign updated successfully!', 'success')
        return redirect(url_for('sponsor_campaigns', sponsor_id=sponsor_id))
        

@app.route('/sponsor/<int:sponsor_id>/deletecampaign/<int:campaign_id>')
def delete_campaign(sponsor_id, campaign_id):
    campaign = Campaign.query.get(campaign_id)
    db.session.delete(campaign)
    db.session.commit()
    flash('Campaign deleted successfully!', 'success')
    return redirect(url_for('sponsor_campaigns', sponsor_id=sponsor_id))




@app.route('/addadvt/<int:campaign_id>', methods=['GET', 'POST'])
def add_advt(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    if request.method == 'POST':
        ad_name = request.form.get('ad_name')
        ad_description = request.form.get('ad_description')
        ad_terms = request.form.get('ad_terms')
        ad_payment = request.form.get('ad_payment')
        ad_platform = request.form.get('ad_platform')
        ad_request = AdRequest(ad_name=ad_name, ad_description=ad_description, ad_terms=ad_terms, ad_payment=ad_payment, campaign_id=campaign_id, ad_platform=ad_platform)
        db.session.add(ad_request)
        db.session.commit()
        flash('Ad request added successfully!', 'success')
        return redirect(url_for('sponsor_ad_request', campaign_id=campaign_id))
    return redirect(url_for('sponsor_ad_request', campaign_id=campaign_id))


@app.route('/assigninfluencer/<int:ad_id>')
def assign_influencer(ad_id):
    ad_request = AdRequest.query.get(ad_id)
    platform = ad_request.ad_platform.lower()
    platform_specific_influencers = []
    if platform == 'instagram':
        platform_specific_influencers = Influencer.query.filter(Influencer.instagram_handle != None).all()
    elif platform == 'twitter':
        platform_specific_influencers = Influencer.query.filter(Influencer.twitter_handle != None).all()
    elif platform == 'youtube':
        platform_specific_influencers = Influencer.query.filter(Influencer.youtube_channel_link != None).all()
    influencers = Influencer.query.all()
    return render_template('select-influencer-by-sponsor.html', ad_request=ad_request, influencers=influencers, relevant_influencers=platform_specific_influencers, )


@app.route('/request/<int:influencer_id>/<int:ad_id>')
def request_influencer(influencer_id, ad_id):
    ad_request = AdRequest.query.get(ad_id)
    existing_negotiations = []
    if ad_request.negotiation:
        existing_negotiations = ad_request.negotiation  
    for negotiation in existing_negotiations:
        if negotiation.influencer_id == influencer_id and negotiation.status in ('requested_by_sponsor', 'negotiating') :
            flash('Influencer already requested!', 'error')
            print('Influencer already requested!')
            return redirect(url_for('assign_influencer', ad_id=ad_id))
        elif negotiation.influencer_id == influencer_id and negotiation.status == 'accepted':
            flash('Influencer already assigned!', 'error')
            print('Influencer already assigned!')
            return redirect(url_for('assign_influencer', ad_id=ad_id))
        elif negotiation.influencer_id == influencer_id and negotiation.status == 'rejected':
            negotiation.status = 'requested_by_sponsor'
            negotiation.updated_at = db.func.now()
            db.session.commit()
            flash('Influencer requested successfully!', 'success')
            print('Influencer requested successfully!')
    else:
        negotiation = Negotiation(ad_request_id=ad_id, influencer_id=influencer_id)
        db.session.add(negotiation)
        db.session.commit()
        flash('Influencer requested successfully!', 'success')
        print('Influencer requested successfully!')

    
    return redirect(url_for('assign_influencer', ad_id=ad_id))

@app.route('/requestad/<int:influencer_id>/<int:ad_id>')
def requestad_influencer(influencer_id, ad_id):
    ad_request = AdRequest.query.get(ad_id)
    influencer = Influencer.query.get(influencer_id)
    if ad_request in influencer.ad_requests :
        negotiaton = Negotiation.query.filter_by(ad_request_id=ad_id, influencer_id=influencer_id).first()
        if negotiaton.status == 'requested_by_influencer':
            flash('Ad already requested!', 'error')
            return redirect(url_for('view_ads', influencer_id = influencer_id, campaign_id = ad_request.campaign_id))
        elif negotiaton.status == 'accepted':
            flash('Ad already assigned!', 'error')
            return redirect(url_for('view_ads', influencer_id = influencer_id, campaign_id = ad_request.campaign_id))
        elif negotiaton.status == 'rejected':
            negotiaton.status = 'requested_by_influencer'
            negotiaton.updated_at = db.func.now()
            db.session.commit()
            flash('Ad requested successfully!', 'success')
    else:
        negotiation = Negotiation(ad_request_id=ad_id, influencer_id=influencer_id, status = 'requested_by_influencer')
        db.session.add(negotiation)
        db.session.commit()
        flash('Ad requested successfully!', 'success') 

    
    return redirect(url_for('view_ads', influencer_id = influencer_id, campaign_id = ad_request.campaign_id))


@app.route('/request/<int:influencer_id>/<int:sponsor_id>', methods=['GET', 'POST'])
def request_influencer_from_find(influencer_id, sponsor_id):
    if request.method == 'POST':
        ad_id = request.form.get('ad_id')
        if not ad_id:
            flash('Ad ID is required!', 'error')
            return redirect(url_for('sponsor_find', sponsor_id=sponsor_id))
        return redirect(url_for('request_influencer', influencer_id=influencer_id, ad_id=ad_id))


#Influencer Related Routes
@app.route('/register/influencer', methods=['GET', 'POST'])
def influencer_register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_repeat = request.form.get('password_repeat')
        if password != password_repeat:
            flash('Passwords do not match!', 'error')
            
            print('Passwords do not match!',password, password_repeat)
            return redirect(url_for('influencer_register'))
        influencer = Influencer(username=username, email=email, password =password)
        db.session.add(influencer)
        db.session.commit()
        flash('Registration successful!', 'success')
        return render_template('profile-setting.html' , influencer=influencer)
    return render_template('register-influencer.html')



@app.route('/login/influencer', methods=['GET', 'POST'])
def influencer_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        influencer = Influencer.query.filter_by(username=username).first()
        if not influencer:
            print('User does not exit!')
            flash('User does not exit!', 'error')
            return redirect(url_for('influencer_login'))
        elif influencer.password != password:
            print("Incorrect password!")
            flash('Incorrect username or password!', 'error')
            return redirect(url_for('influencer_login'))
        else:
            flash('Login successful!', 'success')
            return redirect(url_for('influencer_dashboard', influencer_id=influencer.id))

    return render_template('login-influencer.html')

@app.route('/influencer/<int:id>/profilesettings', methods=['GET', 'POST'])
def update_profile(id):
    influencer = Influencer.query.get(id)
    if request.method == 'POST':
        influencer.username = request.form.get('username')
        influencer.email = request.form.get('email')
        influencer.phone_number = request.form.get('phone_number')
        
        dob_str = request.form.get('dob')
        if dob_str:  # Only parse the date if the string is not empty
            influencer.date_of_birth = datetime.strptime(dob_str, '%Y-%m-%d').date()
        
        influencer.instagram_handle = request.form.get('instagram_handle')
        influencer.instagram_follower_count = int(request.form.get('instagram_followers') or 0)
        influencer.twitter_handle = request.form.get('twitter_handle')
        influencer.twitter_follower_count = int(request.form.get('twitter_followers') or 0)
        influencer.youtube_channel_link = request.form.get('youtube_link')
        influencer.youtube_subscriber_count = int(request.form.get('youtube_subscribers') or 0)
        influencer.primary_content_categories = request.form.get('content_categories')
        influencer.description_of_content = request.form.get('content_description')
        influencer.links_to_portfolio_or_website = request.form.get('portfolio_link')
        profile_picture = request.files.get('profile_picture')
        if profile_picture:
            if influencer.profile_picture:
                os.remove(f'./static/uploads/{influencer.profile_picture}')
            profile_picture.save(f'./static/uploads/{profile_picture.filename}')
            influencer.profile_picture = profile_picture.filename
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        print('Profile updated successfully!')
        return redirect(url_for('update_profile', id=influencer.id))
    return render_template('profile-setting.html', influencer=influencer)



@app.route('/influencer/<int:influencer_id>/dashboard')
def influencer_dashboard( influencer_id):
    influencer = Influencer.query.get(influencer_id)
    return render_template('dashboard-influencer.html', influencer=influencer)

@app.route('/influencer/<int:influencer_id>/find')
def influencer_find(influencer_id):
    influencer = Influencer.query.get(influencer_id)
    campaigns = Campaign.query.all()
    return render_template('find-influencer.html', influencer=influencer, campaigns=campaigns)

@app.route('/influencer/<int:id>/stats')
def influencer_stats(id):
    influencer = Influencer.query.get(id)
    return render_template('stats-influencer.html', influencer=influencer)

@app.route('/influencer/<int:id>/profile')
def influencer_profile(id):
    influencer = Influencer.query.get(id)
    # Ensure counts default to 0 if None
    instagram_follower_count = influencer.instagram_follower_count if influencer.instagram_follower_count is not None else 0
    twitter_follower_count = influencer.twitter_follower_count if influencer.twitter_follower_count is not None else 0
    youtube_subscriber_count = influencer.youtube_subscriber_count if influencer.youtube_subscriber_count is not None else 0

    followers = instagram_follower_count + twitter_follower_count + youtube_subscriber_count
    # Avoid division by zero by ensuring followers is at least 1
    followers = max(followers, 1)

    follower_percent = {
        'instagram': round(instagram_follower_count / followers * 100),
        'twitter': round(twitter_follower_count / followers * 100),
        'youtube': round(youtube_subscriber_count / followers * 100)
    }
    return render_template('profile.html', influencer=influencer, follower_percent=follower_percent)


@app.route('/upload/post/<int:id>', methods=['GET', 'POST'])
def influencer_posts(id):
    influencer = Influencer.query.get(id)
    if request.method == 'POST':
        post = request.form.get('post')
        media = request.files.get('media')
        influencer_post = InfluencerPosts(influencer_id=id, post=post)
        if media:
            media.save(f'./static/uploads/{media.filename}')
            influencer_post.media = media.filename
        db.session.add(influencer_post)
        db.session.commit()
        flash('Post added successfully!', 'success')
        return redirect(url_for('influencer_profile', id=influencer.id))

    return render_template('posts.html', influencer=influencer)

@app.route('/influencer/<int:influencer_id>/viewads/<int:campaign_id>')
def view_ads(influencer_id, campaign_id):
    campaign = Campaign.query.get(campaign_id)
    ads = AdRequest.query.filter_by(campaign_id=campaign_id).all()
    influencer = Influencer.query.get(influencer_id)
    return render_template('show-ads-influencer.html', campaign=campaign, ads=ads, influencer=influencer)

@app.route('/negotiatesponsor/<int:nego_id>', methods=['GET', 'POST'])
def negotiate_sponsor(nego_id):
    negotiation = Negotiation.query.get(nego_id)
    if request.method == 'POST':
        msg = request.form.get('message')
        if not msg:
            flash('Message cannot be empty!', 'error')
            return redirect(url_for('negotiate_sponsor', nego_id=nego_id))
        message = Message(negotiation_id=nego_id, sender='sponsor', content=msg)
        db.session.add(message)
        db.session.commit()
        flash('Message sent successfully!', 'success')
        return redirect(url_for('negotiate_sponsor', nego_id=nego_id))
    messages = Message.query.filter_by(negotiation_id=nego_id).all()
    other_nego_with_same_influencer = Negotiation.query.filter_by(influencer_id=negotiation.influencer_id).all()
    return render_template('negotiate-sponsor.html',negotiation=negotiation, messages=messages, other_nego_with_same_influencer=other_nego_with_same_influencer)

@app.route('/negotiateinfluencer/<int:nego_id>', methods=['GET', 'POST'])
def negotiate_influencer(nego_id):
    negotiation = Negotiation.query.get(nego_id)
    if request.method == 'POST':
        msg = request.form.get('message')
        message = Message(negotiation_id=nego_id, sender='influencer', content=msg)
        db.session.add(message)
        db.session.commit()
        flash('Message sent successfully!', 'success')
        return redirect(url_for('negotiate_influencer', nego_id=nego_id))
    messages = Message.query.filter_by(negotiation_id=nego_id).all()

    return render_template('negotiate-influencer.html',negotiation=negotiation, messages=messages)

@app.route('/finalnegotiation/<int:nego_id>', methods = ['GET', 'POST'])
def final_nego(nego_id):
    negotiation = Negotiation.query.get(nego_id)
    ad_id = negotiation.ad_request_id
    ad_req = AdRequest.query.get(ad_id)
    if negotiation.status == 'accepted':
        flash('Negotiation already accepted!', 'error')
        return redirect(url_for('negotiate_sponsor', nego_id=nego_id))
    if request.method == 'POST':
        new_payment = request.form.get('new_payment')
        new_terms = request.form.get('new_terms')
        negotiation.status = 'accepted'
        negotiation.updated_at = db.func.now()
        ad_req.status = 'ongoing'
        ad_req.influencer_id = negotiation.influencer_id
        if new_payment:
            ad_req.ad_payment = new_payment
        if new_terms:
            ad_req.ad_terms = new_terms
        db.session.commit()
        flash('Negotiation successful!', 'success')
        return redirect(url_for('negotiate_sponsor', nego_id=nego_id))
    if negotiation.status == 'requested_by_sponsor' or negotiation.status == 'requested_by_influencer':
        negotiation.status = 'accepted'
        negotiation.updated_at = db.func.now()
        ad_req.status = 'ongoing'
        db.session.commit()
        flash('Negotiation successful!', 'success')
        return redirect(url_for('negotiate_influencer', nego_id=nego_id))

@app.route('/cancelnegotiation/<int:nego_id>')
def cancel_nego(nego_id):
    negotiation = Negotiation.query.get(nego_id)
    negotiation.status = 'rejected'
    negotiation.updated_at = db.func.now()
    db.session.commit()
    flash('Negotiation cancelled!', 'success')
    return redirect(url_for('negotiate_sponsor', nego_id=nego_id))

@app.route('/withdrawnegotiation/<int:nego_id>')
def withdraw_nego(nego_id):
    negotiation = Negotiation.query.get(nego_id)
    negotiation.status = 'withdrawn'
    negotiation.updated_at = db.func.now()
    db.session.commit()
    flash('Request withdrawn!', 'success')
    return redirect(url_for('negotiate_sponsor', nego_id=nego_id))

@app.route('/cancelinfluencernegotiation/<int:nego_id>')
def cancel_influencer_nego(nego_id):
    negotiation = Negotiation.query.get(nego_id)
    negotiation.status = 'rejected'
    negotiation.updated_at = db.func.now()
    db.session.commit()
    flash('Negotiation cancelled!', 'success')
    influencer_id = negotiation.influencer_id
    return redirect(url_for('influencer_dashboard', influencer_id=influencer_id))

@app.route('/withdrawad/<int:nego_id>')
def withdraw_influencer_nego(nego_id):
    negotiation = Negotiation.query.get(nego_id)
    negotiation.status = 'rejected'
    negotiation.updated_at = db.func.now()
    db.session.commit()
    flash('Negotiation cancelled!', 'success')
    influencer_id = negotiation.influencer_id
    return redirect(url_for('view_ads', influencer_id=influencer_id, campaign_id=negotiation.ad_request.campaign_id ))



@app.route('/updateprogress/<int:nego_id>/<int:ad_id>', methods=['GET', 'POST'])
def update_negotiation(nego_id, ad_id):
    negotiation = Negotiation.query.get(nego_id)
    ad_req = AdRequest.query.get(ad_id)
    if request.method == 'POST':
        progress_percent = request.form.get('progress_percent')
        remarks = request.form.get('remarks')
        if progress_percent:
            ad_req.progress_percent = progress_percent
        if remarks:
            ad_req.remarks = remarks
        db.session.commit()
        flash('Progress updated!', 'success')
        return redirect(url_for('negotiate_influencer', nego_id=nego_id))
    return redirect(url_for('negotiate_influencer', nego_id=nego_id))


@app.route('/withdraw/<int:influencer_id>/<int:ad_id>')
def withdraw_request(influencer_id, ad_id):
    negotiation = Negotiation.query.filter_by(influencer_id=influencer_id, ad_request_id=ad_id).first()
    negotiation.status = 'rejected'
    negotiation.updated_at = db.func.now()
    db.session.commit()
    flash('Request withdrawn!', 'success')
    return redirect(url_for('assign_influencer', ad_id=ad_id))


@app.route('/payment/<int:negotiation_id>')
def payment(negotiation_id):
    negotiation = Negotiation.query.get(negotiation_id)
    return render_template('payment.html', negotiation=negotiation)


@app.route('/generate_qr/<int:negotiation_id>', methods=['GET'])
def generate_qr(negotiation_id):

    negotiation = Negotiation.query.get(negotiation_id)
    if not negotiation:
        return jsonify({"error": "Invalid negotiation ID"}), 404

    company_name = negotiation.ad_request.campaign.sponsor.company_name
    amount = negotiation.ad_request.ad_payment
    payment_url = f'upi://pay?pa=your-upi-id&pn=YourName&am={amount}&cu=INR'

     # Generate QR Code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(payment_url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')

    # Add company name text to QR code
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()  # You can use a different font
    text_bbox = draw.textbbox((0, 0), company_name, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    img_width, img_height = img.size
    text_position = ((img_width - text_width) // 2, img_height - text_height - 10)
    draw.text(text_position, company_name, font=font, fill="black")

    # Save QR Code to a file in the 'static' directory
    filename = f'qr_{negotiation_id}.png'
    img.save(os.path.join('static', filename))

    qr_code_url = url_for('static', filename=filename)
    return jsonify({"qr_code_url": qr_code_url})

@app.route('/mark_as_paid/<int:negotiation_id>', methods=['POST'])
def mark_as_paid(negotiation_id):
    # Here you can add your logic to mark the payment as paid in your database.
    # For this example, we'll just return a success message.
    return jsonify({"message": "Payment marked as paid."}), 200

@app.route('/influencer/<int:influencer_id>/logout', methods=['GET'])
def influencer_logout(influencer_id):
    return redirect(url_for('home'))