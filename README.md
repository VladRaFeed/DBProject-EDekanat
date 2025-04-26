# EDekanat

This application was developed to facilitate and digitalize the processes of creating requests, generating and receiving documents between students and dekanat office.

# Important

To use this application on your machine, you will need to install requirememts.txt and create a .env file, where you need to add:
1) POSTGRES_EXTERNAL - External connection link/key to remote db(we used remote postgres db)
2) EMAIL_HOST
3) EMAIL_HOST_USER - basically email from which you will send pdf documents to students as admin
4) EMAIL_HOST_PASSWORD - a password that allows django use your email to send messages via code
5) EMAIL_PORT
