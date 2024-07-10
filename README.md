# Influencer Engagement and Sponsorship Coordination Platform (IESCP)

## Project Overview

This project is a web-based platform designed to connect Sponsors and Influencers. It allows sponsors to advertise their products/services while enabling influencers to gain monetary benefits by promoting these campaigns. The system features roles for Admin, Sponsors, and Influencers, each with specific functionalities to facilitate seamless interactions and management of advertising campaigns.

## Frameworks and Technologies

The application is developed using the following mandatory frameworks and technologies:

- **Flask**: Used as the core web framework to manage the application logic and routing.
- **Jinja2**: Utilized for HTML templating, working in conjunction with Flask to generate dynamic content.
- **Bootstrap**: Provides a responsive and modern design to the application's frontend.
- **SQLite**: Serves as the database to store and manage all user and campaign data locally.

## Roles and Functionalities

### Admin

- **Admin Dashboard**: Displays comprehensive statistics about the application, including active users, campaigns, and flagged content.
- **Monitoring and Moderation**: Allows for oversight and management of all users and campaigns, with the ability to flag inappropriate content or users.

### Sponsors

- **Campaign Management**: Sponsors can create, update, and delete campaigns. They can also set campaigns as public or private and manage the budget and goals.
- **Ad Request Management**: Sponsors can create, edit, and delete ad requests within their campaigns. They can specify requirements, payment amounts, and manage the status of these requests.
- **Search for Influencers**: Sponsors can search for influencers based on niche, reach, and other relevant criteria to find suitable partners for their campaigns.

### Influencers

- **Profile Management**: Influencers can update their profile information, including their name, category, niche, and reach, which is publicly visible.
- **Ad Request Management**: Influencers can view, accept, reject, or negotiate terms for ad requests they receive. They can also search for public campaigns that match their niche and interests.

## Application Wireframe

The wireframe provides a visual guide to the flow and layout of the application. While it helps in understanding the expected user navigation, the design can be customized.

## Core Functionalities

1. **User Authentication**:
   - Separate login and registration forms for Admins, Sponsors, and Influencers.
   - User differentiation is managed through a robust user model.

2. **Admin Dashboard**:
   - Displays statistics such as active users, campaigns (public/private), ad requests status, and flagged content.

3. **Campaign Management for Sponsors**:
   - Features to create, update, and delete campaigns.
   - Management of campaign visibility and budgeting.

4. **Ad Request Management for Sponsors**:
   - Allows creating, editing, and deleting ad requests.
   - Sponsors can manage the requirements, payment details, and status of ad requests.

5. **Search Functionality**:
   - Sponsors can search for influencers based on niche and reach.
   - Influencers can search for public campaigns based on category and budget.

6. **Ad Request Actions for Influencers**:
   - View, accept, reject, or negotiate ad requests.
   - Search for relevant public campaigns and manage ad requests accordingly.

## Recommended Functionalities

- **API Resources**: For interacting with users, ad requests, and campaigns. This can be implemented using JSON responses or Flask extensions like `flask_restful`.
- **Chart Integration**: Using external libraries like ChartJS to visualize data.
- **Frontend Validation**: Implemented using HTML5 or JavaScript to ensure data integrity.
- **Backend Validation**: Ensures data is correctly handled and validated within the controllers.

## Optional Functionalities

- **Enhanced Frontend**: Using CSS or Bootstrap for a more appealing and responsive user interface.
- **Secure Login System**: Implemented using Flask extensions like `flask_login` or `flask_security` to prevent unauthorized access.
- **Dummy Payment Portal**: A simulated view for taking payment details for ad requests.
- **Additional Features**: Any extra functionalities that enhance the user experience or system operations.

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/IESCP.git
   cd IESCP
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up the Database**:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

4. **Run the Application**:
   ```bash
   flask run
   ```

   The application will be accessible at `http://127.0.0.1:5000`.

5. **Admin Access**:
   Create an admin user through the application interface or directly insert into the SQLite database.


---

