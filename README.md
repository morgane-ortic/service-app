Overview of the Massage App:

User model:
  A user will be able to view the main page of the app which will have bar at the top of the page consisting of different menu options:
Home, Login, Register, Therapist Locations, Contacts... all the normal stuff. We could add more later on when we have a better idea of how it should look/work like.
  In the main/home page itself we will have a widget that lets the user to choose the kind of service they want, it will be on the left half of the screen. 
It will be a list of items consisting of different massage types such as 'Full body massage', 'Shoulder Massage', 'Leg Massage'.
We can show the list on the screen by making a widget in the home page that is scrollable enabling the user to press on an option. Or a drop down menu with a list
of massage types that can be selected. There also will be a search bar excactly above this widget that will let customers type in the type of massage they want.
The widget that will hold the list and the input bar will be vertically centered and will occupy only the left side of the screen. 
  A second widget that will hold a map will be on the excact opposite side of the screen, it will ocupy the right side of the screen and
based on the user input in the search bar or the option chosen from the list it will redirect the view of the map to the closest therapist location.
For example if the user chooses to press on the 'Full body massage' option from the list the map will take the user to the closes therapist 
to his IP adress/location that provides a full body massage. Or if the user writed 'Full body' or similar the map will take the user to the closest therapist as well.
After that on the map, the user will have the option to press on the Therapist and after pressing on their name/location an option to book will appear.
After pressing that option the user will be taken to the therapists page to finish the booking IF they are logged in. If not the user will be asked with a pop-up
or smth similar to login or register. And there will be 2 buttons saying Login/Register. Then the user will finish logging in or registering as a user 
(when registering we have 2 option - register as user/regsiter as therapist) and be redirected to the therapists page to finish the booking.
   
   This model will have access to the Login, Register, Home, Therapist Details, Therapist Services and Booking Services pages. 
