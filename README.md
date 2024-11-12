# MPSTME Connect

#### Video Demo: [Watch Here](https://www.youtube.com/watch?v=lnqHV-p4KwA)

### Description:
MPSTME Connect is a platform designed for students at MPSTME (my university) to connect based on skills, interests, and more. Firstly, when a user comes to the platform, they are directed to the landing page (the index page). This page gives them an overview of the features the platform offers, including hints about the profile page, the search page, and the events page.

If a student is interested, they can register to create an account. An account can only be created with a university email, and since every student is provided with only one email, they can only create one account. This prevents the creation of duplicate accounts. After entering their email, Flask, with the help of the Flask-Mail library (and with me enabling an app password for this Flask application in my Gmail account), will automatically send an email to the user, including their verification code. The user will only be allowed to create an account if their verification code matches the code sent on their email. After creating an account, the email and the password is stored in my MySQL database, which contains the emails and passwords in a table user_auth (given in the schema.sql file). The passwords are hashed with the help of the Werkzeug library, making them inaccessible to even me or anyone who could gain access to the database.

Once logged in, the user can go to the profile page, where they can edit their profile and enter the details they want, including their very own profile picture. All these details are visible to the user immediately and even if they logging out, as the data is stored in the MySQL database, and displayed dynamically. This profile is also visible to other users.

The user can check out the search feature, where they can then check out other users based on multiple parameters given by the filters button. The user can search by bio, name, skills, interests, and soft-skills. Once the user finds a user that matches their search request, they can click on the profile preview, which leads them to the profile of the user they are visiting. This profile would display all the fields that the user they are visiting had filled. The current user also has the ability to follow/unfollow the user they are visiting. This feature is also handled dynamically in the MySQL database.

The user can also check out the events page, where they can check out a few events that are displayed. They can also create their own events, by filling out a small form on the page, and sending an approval request. This request again handled by flask_mail, sends me an email on my own account with the details that the user had entered for their event, including the name of the user, their email, the description and name of the event, a website or instagram link, the location of the event, and the date of the event. If I find the event legitimate, I can create an event that would be displayed on the website to all the users on the platform. This would ensure that the event gets publicity, and people show up, or atleast know about which events are taking place in college.

The platform also has a button which enables the user to toggle between light and dark modes, according to what they prefer. This is handled by javascript, which also changes the pictures present on the webpage the user is looking at, if necessary.

What I used:
The platform uses flask in python as the backend, uses HTML, CSS, and javascript in the frontend, and uses MySQL as the database.
