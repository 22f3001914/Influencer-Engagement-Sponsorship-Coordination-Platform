from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
from flask import current_app as app
from .models import * 
import os


#App related routes
@app.route('/login')
def login():
    return render_template('login.html')


# Admin Related Routes
@app.route('/')
def home():
    return render_template('landing.html')

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
    return redirect(url_for('admin_find', id=admin_id))

@app.route('/admin/<int:admin_id>/delete/<int:influencer_id>')
def delete_influencer(admin_id, influencer_id):
    posts = InfluencerPosts.query.filter_by(influencer_id=influencer_id).all()
    for post in posts:
        if post.media:
            os.remove(f'./static/uploads/{post.media}')
        db.session.delete(post)
    
    influencer = Influencer.query.get(influencer_id)
    db.session.delete(influencer)
    db.session.commit()
    flash('Influencer deleted successfully!', 'success')
    return redirect(url_for('admin_find', id=admin_id))
@app.route('/admin/dashboard/<int:id>')
def admin_dashboard(id):
    admin = Admin.query.get(id)
    campaigns = Campaign.query.all()
    influencers = Influencer.query.all()
    return render_template('dashboard-admin.html', admin=admin, campaigns=campaigns, influencers=influencers)

@app.route('/admin/find/<int:id>')
def admin_find(id):
    admin = Admin.query.get(id)
    influencers = Influencer.query.all()
    return render_template('find-admin.html', admin=admin, influencers=influencers)
    # return render_template('find-admin.html')

@app.route('/admin/stats')
def admin_stats():
    return render_template('stats.html')



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

@app.route('/update/sponsorprofile/<int:id>', methods=['GET', 'POST'])
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

@app.route('/sponsor/profile/<int:id>')
def sponsor_profile(id):
    sponsor = Sponsor.query.get(id)
    return render_template('profile-sponsor.html', sponsor=sponsor)

@app.route('/sponsor/dashboard/<int:sponsor_id>')
def sponsor_dashboard(sponsor_id):
    sponsor = Sponsor.query.get(sponsor_id)
    return render_template('dashboard-sponsor.html', sponsor = sponsor)

@app.route('/sponsor/find')
def sponsor_find():
    return render_template('find-sponsor.html')

@app.route('/sponsor/stats')
def sponsor_stats():
    return render_template('stats.html')

@app.route('/campaign/<int:campaign_id>/ad')
def sponsor_ad_request(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    return render_template('Ad-request-sponsor.html', campaign=campaign)

@app.route('/sponsor/<int:sponsor_id>/campaign', methods=['GET', 'POST'])  
def sponsor_campaigns(sponsor_id):
    if request.method == 'POST':
        name = request.form.get('campaign_name')
        details = request.form.get('campaign_details')
        age_group = request.form.get('age_group')
        gender = request.form.get('gender')
        budget = request.form.get('campaign_budget')
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
        campaign = Campaign(name=name, details=details, age_group = age_group,gender = gender, budget = budget, platform_youtube = platform_youtube, platform_instagram = platform_instagram, platform_twitter = platform_twitter, visibility = visibility, sponsor_id = sponsor_id)
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
    return render_template('find-sponsor.html', ad_request=ad_request, influencers=influencers, relevant_influencers=platform_specific_influencers, )


@app.route('/request/<int:influencer_id>/<int:ad_id>')
def request_influencer(influencer_id, ad_id):
    ad_request = AdRequest.query.get(ad_id)
    existing_negotiations = []
    if ad_request.negotiation:
        existing_negotiations = ad_request.negotiation  
    for negotiation in existing_negotiations:
        if negotiation.influencer_id == influencer_id and negotiation.status == 'negotiating':
            flash('Influencer already requested!', 'error')
            print('Influencer already requested!')
            return redirect(url_for('assign_influencer', ad_id=ad_id))
        elif negotiation.influencer_id == influencer_id and negotiation.status == 'accepted':
            flash('Influencer already assigned!', 'error')
            print('Influencer already assigned!')
            return redirect(url_for('assign_influencer', ad_id=ad_id))
        elif negotiation.influencer_id == influencer_id and negotiation.status == 'rejected':
            negotiation.status = 'negotiating'
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

from datetime import datetime

@app.route('/update/profile/<int:id>', methods=['GET', 'POST'])
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



@app.route('/influencer/dashboard')
def influencer_dashboard():
    return render_template('dashboard-influencer.html')

@app.route('/influencer/find')
def influencer_find():
    return render_template('find-influencer.html')

@app.route('/influencer/stats')
def influencer_stats():
    return render_template('stats.html')

@app.route('/influencer/profile/<int:id>')
def influencer_profile(id):
    influencer = Influencer.query.get(id)
    followers = influencer.instagram_follower_count + influencer.twitter_follower_count + influencer.youtube_subscriber_count
    if followers == 0:
        followers = 1
    follower_percent = {
        'instagram': round(influencer.instagram_follower_count / followers * 100),
        'twitter': round(influencer.twitter_follower_count / followers * 100),
        'youtube': round(influencer.youtube_subscriber_count / followers * 100)
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


@app.route('/negotiatesponsor/<int:nego_id>', methods=['GET', 'POST'])
def negotiate_sponsor(nego_id):
    negotiation = Negotiation.query.get(nego_id)
    if request.method == 'POST':
        msg = request.form.get('message')
        message = Message(negotiation_id=nego_id, sender='sponsor', content=msg)
        db.session.add(message)
        db.session.commit()
        flash('Message sent successfully!', 'success')
        return redirect(url_for('negotiate_sponsor', nego_id=nego_id))
    messages = Message.query.filter_by(negotiation_id=nego_id).all()

    return render_template('negotiate-sponsor.html',negotiation=negotiation, messages=messages)

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
    new_payment = request.form.get('new_payment')
    new_terms = request.form.get('new_terms')
    if negotiation.status == 'accepted':
        flash('Negotiation already accepted!', 'error')
        return redirect(url_for('negotiate_sponsor', nego_id=nego_id))
    if request.method == 'POST':

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
    redirect(url_for('negotiate_sponsor', nego_id=nego_id))

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
    negotiation.status = 'rejected'
    negotiation.updated_at = db.func.now()
    db.session.commit()
    flash('Request withdrawn!', 'success')
    return redirect(url_for('negotiate_sponsor', nego_id=nego_id))


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

import qrcode
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

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
