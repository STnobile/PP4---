# App_Doc


# Mocks


this is a quick sketch to give an idea about the design of the website.

  ![devises responsive](/static/readme/mock3.png)
  ![devises responsive](/static/readme/mock2.png)
  ![devises responsive](/static/readme/mock1..png)
  ![devises responsive](/static/readme/mock.png)



## Project 4

"App_Doc" for a health care website with appointment booking and notification system features. Here's a summary of the main components and functionality described in the document:

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

![devises responsive](/static/readme/book-app.png)

The patient will be able to insert some personal date such as:
* Full Name
* Email address 
* Phone Number
* Subject
* A message that explain his case.


# Features
  - User Features
  - Book Appointment Interface
  - Notification 

  ![devises responsive](/static/readme/book-app.png)

- Appointment Booking for All: Whether you've created an account or not, you can book  
   an appointment.

- Simple Appointment Requests: Just fill out a form with your personal details and 
   appointment information, and you're set.

- Account Benefits: Creating an account isn't just for show. It comes with perks such  
  as being able to track the status of your booking.
  

   - Manage Your Appointment: Did something come up? No worries! You can easily reschedule 
   or even delete your appointment.
   
      ![devises responsive](/static/readme/accept-date.png)
 ## Initial Appointment Request:

   - User's First Request, will get notification.
     ![devises responsive](/static/readme/message-notification.png)

   - Canceling an Appointment:
     ![devises responsive](/static/readme/cancel-appointment.png)

   - User Rescheduling
     ![devises responsive](/static/readme/reschedule.png)


 Open Communication: Users can always reach out to the admin through the provided email addresses on the homepage.

 # Notifications 
  In this section the user will received notifications during his booking steps,
  from the booking of the appointments to the booking accepted and the reschedule date.
  here below there is a series of screenshot that represent the process.

   ![devises responsive](/static/readme/app.conf.png)
   ![devises responsive](/static/readme/app_res.png)
   ![devises responsive](/static/readme/app.not.png)

 # Admin Features
 
 Manage Appointments: The admin has the capability to view all appointments, accept them, or suggest reschedules.

 Admin Accepting Booking.
 ![devises responsive](/static/readme/admin-accept-res.png)

 Accepting Rescheduled Date.
  ![devises responsive](/static/readme/admin-reschedule.png)


# Future Features
* A System of Chat bot, so the user can requests some answer on generic     issues, such as:
    * Bookings
    * General Healthcare advice
    * Request a special service due his condition.

* Have a medical journal so the doctors will have a record of his patients. 

* FAQ'S section.


## Validation 

## HTML
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

# Technology 
- HTML
- CSS 
- JS
- PYTHON (DJANGO)

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

## Testing
 Run test and working fine on the terminal insert:
   - python manage.py test.

    Before you will run the test make sure to modify the setting.py inside the pp4 file.


  ![devises responsive](/static/readme/setting.py.png)

 after you have done that go to the terminal and run it. 


![devises responsive](/static/readme/testing.png)


## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.


# Credits 
- https://www.youtube.com/watch?v=YtzFtkV4TTM&t=30s
- https://www.youtube.com/watch?v=-9dhCQ7FdD0&list=PL_6Ho1hjJirn8WbY4xfVUAlcn51E4cSbY
- https://www.youtube.com/watch?v=rHZwE1AK1h8&t=1422s
