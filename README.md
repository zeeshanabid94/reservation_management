# Reservation Management
A backend to manage reservations in django.

# Running it locally
You can run this project locally as follows:

1- Start by making a virtual environment.  
```
virtualenv venv
```  
This creates a virtual environment in the folder venv. If you don't have virtualenv installed, please follow this link [link:https://virtualenv.pypa.io/en/stable/installation/]

2- Activate the virtual environment.  
```
source venv/bin/activate
```

3- Clone this repo.  
```
git clone https://github.com/zeeshanabid94/reservation_management.git
```

4- Now go into the cloned repo and install the required packages.    
``` 
cd reservation_management
pip install -r requirements.txt
```

5- Once the packages finish installing, run the following commands in order to migrate the database. This needs to be done once per setup.  
```
cd reservation_management
python manage.py migrate
```
6- Now to run the local server, try:
```
python manage.py runserver
```
Note: To run the server, you have to be in the directory with manage.py. If you are in upper level reservation_management, then cd into the right dir.  

7- You can view the data received in the browser. Going to the linke localhost:8000/reservations/, you will see a browseable api for you to test.

Note: The api can easily be switched to json by changing configuration of django. To allow ease of testing and demonstration, the browser displays the data.  

# Restful Routes

Reservation Model:  
start_date -> BigInt  
end_date -> BigInt  
user -> Id of user who has this reserved  
uuid -> UUID of the reservation  

- GET /reservations/  
  Displays the list of reservations between the date range 2 days from now to 32 days from now. This is the default start_date and end_date.  
Response:```[{"uuid":<uuid>, "start_date":<start>, "end_date":<end>},...]  ```

- GET /reservations/?start=<start>&end=<end>  
  Displays the list of reservations between the date range start to end. The start and end are integers and epoch time.  
Response:```[{"uuid":<uuid>, "start_date":<start>, "end_date":<end>},...]```

- GET /reservations/<uuid>  
  Displays the data for the reservation with uuid if it exists. Returns 404 if no reservation was found.  
Response:```{"uuid":<uuid>, "start_date":<start>, "end_date":<end>}```

- POST /reservations/
  Reserves the reservation with UUID to the user with the fullname and email. Reserving is critical, and to avoid race conditions, a distributed three lock scheme is used using memcache and sherlock python package. Returns the reservation if it was reserved otherwise returns an error.  
Request:```{"uuid":<uuid>, "start_date":<start>, "end_date":<end>, "fullname":<fullname>, "email":<email>}```  
Response:```{"uuid":<uuid>, "start_date":<start>, "end_date":<end>}```  

- PUT /reservations/
  Modifies the reservation with the given uuid to the specified start and end. Returns 404 if reservation not found.  
Request:```{"start_date":<start> (Optional), "end_date":<end> (Optional), "uuid":<uuid>}```   
Response```{"uuid":<uuid>, "start_date":<start>, "end_date":<end>}```

# Things to do
- Implement validation for modification requests using put.
- Implement configurable option for displaying date in human friendly format.
