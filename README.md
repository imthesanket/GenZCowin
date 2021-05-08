# GenZCowin
Get email alerts when vaccines are available in your district for age group 18-44.

* Configure sender's email credentials:
In send_mail() function, you'll need to add the credential of sender's email id. I used Gmail service for the same. You can use your gmail email id as 'gmail_user' and for password you'll need to generate app password for your gmail account. Check here how you can generate the same: https://devanswers.co/create-application-specific-password-gmail/

For 'receivers_list' variable, add email ids of receivers, seperated by commas. 

* For State id and district id, refer the IDs folder which contains json files detailing about the state name and their ids respectively.
