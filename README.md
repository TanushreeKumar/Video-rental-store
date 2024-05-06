# Video-rental-store
A video rental store is a brick-and-mortar business offering temporary rentals of movies, VCR, and video games. Customers browse titles in-store or online, pay for rentals per item, and return them by a specified deadline to avoid late fees. Membership programs offer discounts and benefits. Stores primarily deal with physical media like DVDs and Blu-rays, with some offering additional services like sales and special events. Despite challenges from digital streaming, video rental stores remain community hubs for movie enthusiasts seeking a curated experience.
The project involves a meticulously designed database schema for comprehensive data management, including entities like customers, items, transactions, payment and categories, ensuring data coherence and integrity constraints.

 **Person**<br/>
   Users: User_id, username, password, email.<br/>
   Customers: Customer ID, name, email, phone number.<br/>
   Employees: Employee ID, name, position.<br/>

 **Items**<br/>
   Movies: Movie ID, name, director, charge per day, producer, type/genre, quantity.<br/>
   VCR: VCR ID, type, VCR brand name, charge, made by, quantity.<br/> 
   Video Camera: Video camera ID, brand name, made by, charge, quantity.<br/>

**Transactions**<br/>
   Movie_transactions: ID, type, movie ID, amount paid, due date, return date, customer ID, employee ID.<br/>
   VCR_transactions: ID, type, VCR ID, amount paid, due date, return date, customer ID, employee ID.<br/>
   VCamera_transactions: ID, type, Video camera ID, amount paid, due date, return date, customer ID, employee ID.<br/>
   
**Payment**<br/>
   Tracks payment details for transactions, including payment method, amount, date, etc.<br/>

**Categories**<br/>
   Defines categories for movies, VCR, and other media items.<br/>

**Libraries Used**<br/>
Tkinter:- Tkinter is a Python library that can be used to construct basic graphical user interface (GUI) applications. (tkinter)<br/>
Regular Expression:- A RegEx, or Regular Expression, is a sequence of characters that forms a search pattern. RegEx can check if a string contains the specified search pattern. (re)<br/>
MySQL Connector:- Python MySQL Connector is a Python driver that helps to integrate Python and MySQL. This Python MySQL library allows the conversion between Python and MySQL data types. (mysql.connector)
