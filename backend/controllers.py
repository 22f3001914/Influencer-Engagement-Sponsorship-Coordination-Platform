from flask import Flask, render_template, request, redirect, url_for, flash
from flask import current_app as app
from .models import * 

#App related routes
@app.route('/login')
def login():
    return render_template('login.html')


# Admin Related Routes
@app.route('/')
def home():
    return render_template('index.html')

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

@app.route('/admin/dashboard/<int:id>')
def admin_dashboard(id):
    admin = Admin.query.get(id)
    return render_template('dashboard-admin.html', admin=admin)

@app.route('/admin/find')
def admin_find():
    return render_template('find-admin.html')

@app.route('/admin/stats')
def admin_stats():
    return render_template('stats.html')



# Sponsor Related Routes
@app.route('/register/sponsor')
def sponsor_register():
    return render_template('register-sponsor.html')

@app.route('/sponsor/dashboard')
def sponsor_dashboard():
    return render_template('dashboard-sponsor.html')

@app.route('/sponsor/find')
def sponsor_find():
    return render_template('find-sponsor.html')

@app.route('/sponsor/stats')
def sponsor_stats():
    return render_template('stats.html')

@app.route('/sponsor/add/ad')
def sponsor_ad_request():
    return render_template('Ad-request-sponsor.html')

@app.route('/sponsor/campaigns')
def sponsor_campaigns():
    return render_template('campaigns-sponsor.html')

#Influencer Related Routes
@app.route('/register/influencer')
def influencer_register():
    return render_template('register-influencer.html')


@app.route('/influencer/dashboard')
def influencer_dashboard():
    return render_template('dashboard-influencer.html')

@app.route('/influencer/find')
def influencer_find():
    return render_template('find-influencer.html')

@app.route('/influencer/stats')
def influencer_stats():
    return render_template('stats.html')

@app.route('/influencer/profile')
def influencer_profile():
    return render_template('profile.html')
