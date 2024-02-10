# Database Design

1. **Entity: User**
   - Attributes:
     - ID (Primary Key)
     - Username
     - Password
     - Role (Librarian or General User)
     - SubscriptionType (Free or Premium)
     - SubscriptionExpiryDate
     - SubscriptionRenewalAmount
     - BooksAllowed (Number of books allowed for the current subscription)
     - AccessDuration (Duration for which the user has access to books)

2. **Entity: Librarian**
   - Attributes:
     - ID (Primary Key)
     - Username
     - Password

3. **Entity: Section**
   - Attributes:
     - ID (Primary Key)
     - Name
     - DateCreated
     - Description

4. **Entity: Book**
   - Attributes:
     - ID (Primary Key)
     - Name
     - Content
     - Author(s)
     - DateIssued
     - ReturnDate
     - SectionID (Foreign Key referencing Section)

5. **Entity: Request**
   - Attributes:
     - ID (Primary Key)
     - UserID (Foreign Key referencing User)
     - BookID (Foreign Key referencing Book)
     - RequestDate
     - ReturnDate

6. **Entity: Feedback**
   - Attributes:
     - ID (Primary Key)
     - UserID (Foreign Key referencing User)
     - BookID (Foreign Key referencing Book)
     - Comment
     - Rating

7. **Entity: Subscription**
   - Attributes:
     - ID (Primary Key)
     - Type (Free, Monthly, Quarterly, Annual)
     - RenewalAmount
     - MaxBooksAllowed
     - AccessDurationDays

Now, let's establish relationships:

- A User has one Subscription (One-to-One relationship between User and Subscription).
- A Subscription can have multiple Users (One-to-Many relationship between Subscription and User).
- A User can make multiple Requests (One-to-Many relationship between User and Request).
- A Book can have multiple Requests (One-to-Many relationship between Book and Request).
- A User can give multiple Feedbacks (One-to-Many relationship between User and Feedback).
- A Book can have multiple Feedbacks (One-to-Many relationship between Book and Feedback).
- A Section can have multiple Books (One-to-Many relationship between Section and Book).

Now, the `Section` and `Book` entities are connected, indicating that a book must belong to at least one section, and a section can contain multiple books. Please update your ER diagram accordingly. If you have any more questions or need further assistance, feel free to ask!
