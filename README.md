# Overview of the Massage App

## User Model

A user will be able to view the main/home page of the app which will have bar at the top of the page consisting of different menu options:  
Home, Login, Register, Therapist Locations, Contacts... all the normal stuff, this bar will be present in all pages throughout the website.  
We could add more options for the bar on the top of the screen later on when we have a better idea of how it should look/work like.

In the main/home page itself we will have a widget that lets the user to choose the kind of service they want, it will be on the left half of the screen.  
It will be a list of items consisting of different massage types such as 'Full body massage', 'Shoulder Massage', 'Leg Massage'.  
We can show the list on the screen by making a widget in the home page that is scrollable enabling the user to press on an option.  
Or a drop-down menu with a list of massage types that can be selected.  

There also will be a search bar exactly above this widget that will let customers type in the type of massage they want.  
The widget that will hold the list and the input bar will be vertically centered and will occupy only the left side of the screen.  

A second widget that will hold a map will be on the exact opposite side of the screen, it will occupy the right side of the screen and  
based on the user input in the search bar or the option chosen from the list it will redirect the view of the map to the closest therapist location.  
For example, if the user chooses to press on the 'Full body massage' option from the list the map will take the user to the closest therapist  
to his IP address/location that provides a full body massage. Or if the user writes 'Full body' or similar the map will take the user to the closest therapist as well.  

After that, on the map, the user will have the option to press on the Therapist and after pressing on their name/location, an option to book will appear.  
After pressing that option the user will be taken to the therapist's page to finish the booking **IF** they are logged in.  
If not, the user will be asked with a pop-up or something similar to login or register. And there will be 2 buttons saying Login/Register.  
Then the user will finish logging in as a user or registering as a user (when registering we have 2 options - register as user/register as therapist)  
and be redirected to the therapist's page to finish the booking.  

When a user is registered, they will be automatically logged in. To register, a user will need to input their first and last name, age, sex (male, female, other - we let Morgane do this part),  
full address, and email address, phone number (optional, not everyone wants to be contacted by phone), a profile photo (optional), and a password.  

We can additionally ask for some security questions/answers in case the user loses (I believe this part could be expanded on in the future, we will see)  
their login password and needs to reset it. The questions/answers method is optional. Captcha or verification codes could also be implemented but not necessary.

This model will have access to the Login, Register, Home, Therapist Services, Therapist Details, and Booking Services pages.

---

## Therapist Model

Therapists will be able to view the main/home page and the hot bar at the top as well but once they login or register as a therapist, their home page will change.  
The home page of a therapist will consist of a schedule - a calendar of sorts that will show them their schedule for the whole month, the whole week, or just a specific day.  
The format in which the therapist will be able to see their schedule will be up for debate by the person who will work on it.  
It would be preferred to be able to see a calendar on which the therapist could just press on a day and see all of their appointments.  

Or the calendar could be separate from a widget that will show them all their bookings for today. For example, we could have the calendar on the left half of the screen  
and on the right side, we could see which hours are booked out. Another thing that the therapist will need is receiving notification.  

Every time a user books with them they **HAVE** to receive a notification with a sound that will pop up on the top of the screen and show them that they have a client booked.  
The notification part is important.

Another important detail for the therapist model is that when a Therapist starts the registering process, they will also need to upload their credentials - ID and papers  
that show that they are real therapists. In the registering process, they will send all of their information to the Admin of the page, then the Admin will contact the therapist by phone.  

The registration process for therapists will be the same as the user registration process plus more information.  
ID and their certifications/degrees, an address for the establishment they will work at, and the massage types that they provide together with pricing.  
After the Admin contacts the therapist, verifies that they are the real deal, and the registration process is done, the therapist will appear on the map  
together with a verification badge on the right of their name.  

Unlike for customers, for therapists, it is mandatory to have a profile picture. The profile picture will be shown on the left side of their name on the map.  
Therapists will be able to see the details of customers who have booked with them such as name, profile picture, and type of service.  
Therapists will also have access to their own Services' page and will be able to delete, add new services and change pricing.  
(I assume we will have more updates for this model later on)

This model will have access to the Login, Register, Home, Therapist Services, and User Details pages.

---

Feel free to edit the description if you work on a specific part of the project and have a better idea about how that specific part should work. Notify us.
