# To-Do Lists
Since this is an OOP program, I intend for each type of person to be its own "class" in this program.

## An admin
- ~~Find a way for him to log himself in before the login database containing his credentials is created~~
- Make him the only person to access database and the login table

## The project
The projects shall be store as a **Table in the Database**. Each project shall be a dictionary with the following keys

- Project name (str)
- A Project Leader (str)
- Members (list of str)
- An Advisor (str)
- The proposal's content (str)
- Status (approved/denied)

Each of the person class can interact with only specific keys as outlined in the document.