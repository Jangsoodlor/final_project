# Final project for 2023's 219114/115 Programming I
* Starting files for part 1
  - database.py
  - project_manage.py
  - persons.csv

# Classes and Functions
## Class Container
This class is, like the name suggests, a container class. Which all the other classes except the main class inherited its attributes from.

|method|explanation|
|__init__|take in table object as a starting attribute|
|get_table|returns the table object|
|find_dict|returns the first dictionary which matches the key and value the user inputted|
|__str__|print table|

## Class Request
This class handled requests. Inherited attributes from container.
|method|explanation|

# Files necessary to run the program:
  - database.py
  - project_manage.py
  - persons.csv
  - a database subdirectory in the program's directory. Which contains:
    - login.csv
    - persons.csv

  additionally, the program utilizes these following libraries
  - os
  - csv
  - datetime
  - copy
  all of which are standard python libraries.
  
# How to run?
  - clone or download the project
  - run the **project_manage.py** file.

# Bugs
I've spent three hours finding and fixing bugs. The only bugs I can think of is IndentationError. Since I run pylint after all the debuggings. But that should be almost impossible because I rigorously checked for indentation mistakes before pushing the final commit.

# Copyright Notice
Graduation Project Management System.
Copyright (C) 2023 Jangsoodlor. All Rights Reserved.

This program is part of 01219114/15 Computer Programming I Course
Semester 1 Academic Year 2566 B.E. (2023 A.D.)
Kasetsart University

DO NOT copy, modify, merge, publish, distribute, sublicense, and/or sell copies of this Software.
UNLESS you're a Kasetsart University Computer Engineering Department's Professor or Teacher Assistant.

THERE IS NO WARRANTY FOR THE PROGRAM. IN NO EVENT WILL THE COPYRIGHT HOLDER BE LIABLE TO YOU FOR DAMAGES, 
INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE 
OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF DATA 
OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD PARTIES 
OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS), 
EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.