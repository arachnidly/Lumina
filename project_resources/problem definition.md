
# Frameworks to use

- Flask for app code
- Jinja2 templates + Bootstrap for HTML generation and styling
- SQLite for data storage
- All demos should be possible on your local machine using any local IDE and should not require setting up new servers for database and frontend management

# Library Management System

- What: It is a multi-user app (one required librarian and other general users/students)
- Used for issuing e-books to users
- User can request, read, return e-books
- Librarian can add new sections/e-books, issue/revoke access for a book.

- Each Section **may** have
  - ID
  - Name
  - Date created
  - Description

- Each Book **will** have
  - ID
  - Name
  - Content
  - Author(s)
  - Date issued
  - Return date

- Every section can have a number of books

- System will automatically show recently added sections/books or based on certain rating

- Terminology
  - Sections
  - User, Librarian, Admin
  - e-Book, content
  - Policies

# Core functionality

Base requirements:

- Librarian's Dashboard
- General User's Profile
- Section Management
- Book Management
- Search functionality for section/e-books

# Core - Librarian and User Login

- Form for username and password for user
- Separate form for librarian login for simplicity
  - Can either use a proper login framework, or just use a simple HTML form with username and password. Security is not a concern for this project.
- Suitable model for user (Model that stores the type of users and differentiates them correctly based on their role)

# Core - General user functionality

- Login/Register
- View all the existing Sections/e-books
- Request/Return Books (content)
- A user can request for a maximum of 5 e-books at a time
- A user can access a book for a specific period of time (say N hours/days/weeks)
  - For e.g. if N = 7 days, user can return a book before 7 days. If he/she fails to do so, the access for that will be automatically revoked after 7 days.
- User can give feedback for an e-book

# Core - Librarian functionality

- Issue one or multiple e-book(s) to a user
- Revoke access for one or multiple e-book(s) from a user
  - Storage should handle multiple languages - usually UTF-8 encoding is sufficient for this
- Edit an existing section/e-book
  - Change content, author name,  no. of pages/volume etc.
- Remove an existing section/e-book
- Assign a book to a particular section
- Monitor current status of each e-book and the user it is issued to
- Make e-books available in the library

# Core - Search functionality

- Ability to search for a particular section
- Ability to search e-books based on section, author etc

# Recommended (graded)

- Download e-books as PDF for a price
- APIs for interaction with sections and books
  - CRUD on e-books
  - Additional APIs for getting the creating graphs for librarian dashboard
- Validation
  - All form inputs fields - text, numbers, dates etc. with suitable messages
  - Backend validation before storing / selecting from database

# Optional

- Styling and Aesthetics
- Proper login system
- Subscriptions or paid versions of the app, become author etc
- Ability of app to read books for a user (text-to-speech)

# Project Evaluation

- Report (not more than 2 pages) describing models and overall system design
  - Include as PDF inside submission folder
- All code to be submitted on portal
- A brief (2-3 minute) video explaining how you approached the problem, what you have implemented, and any extra features
  - This will be viewed during or before the viva, so should be a clear explanation of your work
- Viva: after the video explanation, you are required to give a demo of your work, and answer any questions
  - This includes making changes as requested and running the code for a live demo
  - Other questions that may be unrelated to the project itself but are relevant for the course
- The project has to be submitted as single zip file
