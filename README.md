# App_Doc
## Project 4

"App_Doc" for a health care website with appointment booking and notification system features. Here's a summary of the main components and functionality described in the document:

- HTML
- CSS 
- JS
- PYTHON (DJANGO)

![devises responsive](/static/readme/amIresponsive.png)

The web site is for booking a appointment for health care, with a log in to be able to delete or reschedule an appointment.

The user can book an appointment after sign up or through an email.

![devises responsive](/static/readme/emails.png)

## Navigation

* The features are on the top of the screen, the logo is located at the left of the screen and the navigation links are following up.
* The navigation links are: OUR TEAM, SERVICE, TESTIMONIAL and CONTACT US also has a Bell and a Notification post.
* The navigation is in a font that works well with the contrast of the background.
* The navigation is simple and with a elegant style.


![devises responsive](/static/readme/navbar.png)

## Our Team

This section as four card with an image and a description of our team and their field of expertise.

![devises responsive](/static/readme/ourteam.png)


## Service

Here it is explained what service we provide to our costumers, such as:
* Primary Care 
* Dermatology 
* PrEP Therapy
* Team Member

![devises responsive](/static/readme/service.png)

# Testimonial
 We used a carousel with HTML and CSS to create a more dynamic our website.
 Using some of our testimonial comments.


![devises responsive](/static/readme/testimonial.png)

# Location and Get in Touch
![devises responsive](/static/readme/emails.png)

This section is the final of the fist page, it has a google location able to be connected to our maps, aso has an email section in case our future patients have some questions.

# Book An Appointment 

![devises responsive](/static/readme/bkapp.png)

Clicking on book an appointment the user will be able to request an appointment filling the form.
## Form
![devises responsive](/static/readme/appointmentform.png)
The patient will be able to insert some personal date such as:
* Full Name
* Email address 
* Phone Number
* Subject
* A message that explain his case.

Once the patient will sent the request it will show on the Admin notification that will confirm the appointment and set a date.

As displayed in the picture below.

![devises responsive](/static/readme/notification.png)
# Admin Log in
* UserName:
    admin
 * password:
    CodeStart 
# User features

![devises responsive](/static/readme/book_appoinmt.png)

- The user will be able to book an appointment either will have created an account or without.

- Users can submit appointment requests by filling out a form with their personal details and appointment information.

- Creating an account will have his advantage like be able to keep track of the status of the booking itself.

- The user  will able to reschedule or delete his appointment.

![devises responsive](/static/readme/user_first_request.png)
![devises responsive](/static/readme/cancel_your_appointment.png)
Here it will be displayed the confirmation of the admin with the appointment date.
![devises responsive](/static/readme/user_reschedule_appoiment.png)
In the following pic, a scenario were the user is rescheduling the date given from the admin.
![devises responsive](/static/readme/user_reschedule_date.png)
![devises responsive](/static/readme/user_reschedule_date.png)
Here the date set from the user will be displayed on the left hand-side with the day and the month after the admin accepted it.
![devises responsive](/static/readme/admin_accepted_date2.png)


- Also the user is able to communicate with the admin 
through emails that he can find on the homepage.

- Administrators can view and manage the appointments, including accepting or rescheduling appointments.
In the following pic it will be illustrated the path of the admin from the accepting the user request to the reschedule date.

![devises responsive](/static/readme/admin_accepting_booking.png)
![devises responsive](/static/readme/admin_accepting_reschedule_date.png)


# Feature and Implementation 
* A System of Chat bot, so the user can requests some answer on generic     issues, such as:
    * Bookings
    * General Healthcare advice
    * Request a special service due his condition.

* Have a medical journal so the doctors will have a record of his patients. 

* FAQ'S section.


## Validation 
## HMTL
- ![devises responsive](/static/readme/html_appiment_validation.png)
- ![devises responsive](/static/readme/html_validation.png)

## CSS
- ![devises responsive](/static/readme/css_validator.png)


## JS
- ![devises responsive](/static/readme/js_validator.png)
![devises responsive](/static/readme/lighthouse.png)
![devises responsive](/static/readme/lighthouse_vali_appointment.png)
![devises responsive](/static/readme/lighthouse_manage.png)

## Installation and Usage

 Instructions for cloning the repository, installing dependencies, running the development server, and accessing the application are provided.

 Installation :
1. Clone the repository: `git clone https://github.com/your/repo.git`
2. Change to the project directory: `cd project-directory`
3. Install dependencies: `pip install -r requirements.txt`

Usage:

1. Run the development server: `python manage.py runserver`
2. Access the application in your web browser at `http://localhost:8000`
3. Fill out the appointment form with your details and submit the request.
4. Administrators can log in to the admin dashboard at `http://localhost:8000/admin` to manage appointments.

## Configuration

The project uses environment variables for configuration, including a secret key and a database connection URL.

- `SECRET_KEY`: Secret key for Django application
- `DATABASE_URL`: Database connection URL

Make sure to set up these environment variables before running the application.

# Debug

- I had some issues the different if else statements on the template.
for example: on the manage-appointment.html line 74. I could not abe able to follow the logic that I wanted to use and the results was giving a loop between the reschedule appointment and the accepting and I wasn’t able to make it work.
So instead to be able to reschedule the the date only once it was going infinite time. 
I fixed the issue adding one more if else statements and I made the logic more simple that was before givin the user and the admin different inputs.
![devises responsive](/static/readme/if_else_statement.png)

- Another issue was also regarding an if else statement, this time was for the Notifications for the admin. I wasn’t able to separate the admin from the user.
I fixed the bug adding 
{% if request.user.is_authenticated and request.user.is_staff %}
![devises responsive](/static/readme/if_else_statement_count.png)

now all the bugs are fixed and working fine.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.


# Credits 
- https://www.youtube.com/watch?v=YtzFtkV4TTM&t=30s
- https://www.youtube.com/watch?v=-9dhCQ7FdD0&list=PL_6Ho1hjJirn8WbY4xfVUAlcn51E4cSbY
- https://www.youtube.com/watch?v=rHZwE1AK1h8&t=1422s
