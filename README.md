# Django Logs API

Simple API project to learn Django Rest API Framework

The API allows:
- Unregistered users to:
  - View the inventory of unreserved logs
- Registered users to:
  - Reserve logs
  - View logs they have reserved
  - Unreserve logs
  - Split a log

## To Do:
- Add endpoint for users to reserve logs
- Add endpoint for users to cancel a reservation
- Add endpoint for users to split a log
- Add endpoints for user registration

### Done:
- Add a reservation model object containing
  - User
  - Log IDs
  - Creation date
- Add endpoints for user login and logout
- Set default permissions such that:
  - Authenticated users can view logs
  - Staff users can update logs
- Add endpoints to view their reservations lists and their individual reservations
