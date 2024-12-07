Security Policy
Supported Versions
Below is the list of current versions for the project dependencies and their security update status. These versions have been carefully selected to ensure compatibility, security, and reliability, particularly in protecting against common vulnerabilities such as SQL injections.

Package	Version	Supported
asgiref	3.8.1	:white_check_mark:
Django	5.1.4	:white_check_mark:
Faker	33.1.0	:x:
pillow	11.0.0	:white_check_mark:
python-dateutil	2.9.0.post0	:white_check_mark:
six	1.16.0	:white_check_mark:
sqlparse	0.5.2	:white_check_mark:
typing_extensions	4.12.2	:white_check_mark:


Why These Versions?
Django 5.1.4: This version includes the latest security updates and mitigations against SQL injection vulnerabilities by ensuring proper query parameterization and validation. 
By using the built-in ORM (Object-Relational Mapping), Django eliminates the need for raw SQL in most cases, significantly reducing the risk of injection attacks.

sqlparse 0.5.2: sqlparse is a critical component when working with SQL queries in Django. 
The selected version ensures compatibility with Django's ORM and provides robust parsing, reducing the risk of malformed queries that could expose vulnerabilities.

python-dateutil 2.9.0.post0 and six 1.16.0: These libraries are essential for handling date/time operations and compatibility. 
Their maintained versions ensure no indirect vulnerabilities affect SQL query logic.

Importance of Maintaining Supported Versions
Using the recommended versions ensures that the latest security patches are applied, addressing known vulnerabilities proactively. 
Older versions, such as those marked with an ❌, may have unresolved security issues that expose the project to risks such as SQL injection, data leakage, and privilege escalation.
