# Virtual Workspace Room Booking System 🏠

A RESTful API for managing workspace room bookings, cancellations, and availability in a shared office setup.

##### NOTE: `: Please read the openapi.yml file in a swagger viewer to see better api documentation.`

## Testing

```
Username: admin
Password: admin
```

## Demo Video: -

Please check out the demo for this API here: <a href="https://www.youtube.com/watch?v=4PZ_LEmEWJk">Demo Video Link</a>

## Features

- Book rooms (Private, Conference, Shared Desks)
- Cancel bookings
- View all bookings
- Check room availability
- Support for team bookings
- Time slot management (9 AM - 6 PM)
- Automatic room allocation based on booking type and team size
- Pagination for booking listings
- Role-based access control (Manager/Admin)

## Tech Stack

- Python 3.11
- Django 5.0.2
- Django REST Framework 3.14.0
- PostgreSQL 15
- Docker & Docker Compose
- Swagger/OpenAPI Documentation

## Setup Instructions

1. Clone the repository:

```bash
git clone https://github.com/KunalMehra075/Frejun-Assignment
cd Frejun-Assignment
```

2. Build and start the containers:

```bash
docker-compose up --build
```

3. The API will be available at `https://frejun-assignment.onrender.com`

4. API Documentation is available at `https://frejun-assignment.onrender.com/docs/`

## API Endpoints

### Bookings

#### List/Create Bookings

- **Endpoint**: `GET/POST /api/v1/bookings/`
- **Access**: Manager/Admin only
- **GET Query Parameters**:
  - `status` (optional): Filter by booking status (e.g., 'cancelled')
- **POST Request Body**:

  ```json
  {
    "user": {
      "name": "string",
      "age": "integer",
      "gender": "string"
    }
  }
  ```

  OR

  ```json
  {
    "team": {
      "name": "string",
      "members": [
        {
          "name": "string",
          "age": "integer",
          "gender": "string"
        }
      ]
    },
    "room_type": "PRIVATE|CONFERENCE|SHARED",
    "slot": "YYYY-MM-DDTHH:MM"
  }
  ```

- **Response**: Paginated list of bookings or created booking details

#### Cancel Booking

- **Endpoint**: `POST /api/v1/cancel/{booking_id}/`
- **URL Parameters**:
  - `booking_id`: ID of the booking to cancel
- **Response**: Success message or error if booking not found

### Rooms

#### Get Currently Booked Rooms

- **Endpoint**: `GET /api/v1/rooms/`
- **Access**: Manager/Admin only
- **Response**: List of currently occupied rooms with details

#### Check Room Availability

- **Endpoint**: `GET /api/v1/rooms/available/`
- **Query Parameters**:
  - `room_type`: Type of room (PRIVATE/CONFERENCE/SHARED)
  - `slot`: ISO 8601 formatted datetime (YYYY-MM-DDTHH:MM)
- **Response**: List of available rooms matching criteria

## Database Schema

### Users

- id (Primary Key)
- name
- age
- gender

### Teams

- id (Primary Key)
- name
- members (Many-to-Many with Users)

### Rooms

- id (Primary Key)
- room_type (Private, Conference, Shared)
- capacity
- room_number

### Bookings

- id (Primary Key)
- room (Foreign Key to Rooms)
- user/team (Foreign Key to Users/Teams)
- start_time
- end_time
- booking_type (Individual/Team)
- status (Active/Cancelled)
- created_at

## Business Rules

1. Room Types and Capacities:

   - 8 Private Rooms (1 person per room)
   - 4 Conference Rooms (3+ team members)
   - 3 Shared Desks (up to 4 users per desk)

2. Booking Rules:

   - Time slots: 9 AM - 6 PM (hourly slots)
   - One booking per user/team at a time
   - No overlapping bookings for the same room
   - Children (< 10 years) count in team size but don't occupy seats
   - Conference rooms require minimum 3 team members (excluding children)
   - Private rooms are for individual users only
   - Shared desks are for individual users only

3. Access Control:

   - Only managers and administrators can create/cancel bookings
   - Only managers and administrators can view all bookings
   - Room availability check is public

4. Validation Rules:
   - Bookings must be made for future time slots
   - Time slots must be within business hours (9 AM - 6 PM)
   - Room type must be valid (PRIVATE/CONFERENCE/SHARED)
   - User/team data must be valid
   - No double bookings for users/team members

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- 400: Bad Request (invalid input data)
- 401: Unauthorized (missing/invalid authentication)
- 403: Forbidden (insufficient permissions)
- 404: Not Found (resource doesn't exist)
- 500: Internal Server Error

## Testing

Run tests using:

```bash
docker-compose run web pytest
```

## Assumptions

1. All times are in the same timezone (UTC)
2. Bookings are made for full hours only
3. Children are included in team size calculations but don't occupy seats
4. Room capacity is fixed and cannot be modified
5. Users can only have one active booking at a time
6. Business hours are 9 AM to 6 PM
7. Bookings cannot be made for past time slots
