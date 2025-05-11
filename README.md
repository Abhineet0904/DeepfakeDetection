# INSTRUCTIONS :


1. st_pages should be downloaded as : `pip install st-pages==0.4.1`
   - This version contains the show_pages() method, which is deprecated in recent versions.
   - Streamlit installed should be v1.25.0, to ensure compatibility with st-pages v0.4.1.
   - `pip install streamlit==1.25.0`



2. Create a **firebase account**.



3. In Firebase Authentication, go to Sign-in method, and **add provider as Email/Password**.



4. In project settings, go to Service accounts and click on Generate new private key. Paste the downloaded firebase-adminsdk file with .json extension in your project's root directory.      - Then paste the name of this file in .env file in your root folder in the following way :
   - `FIREBASE_PRIVATE_JSON_KEY = "_______"`



5. Then go to General in project settings. In SDK setup and configuration, click on Config radio button, and copy the Firebase configuration object. Paste the object in the .env file in  the following way :
   - `FIREBASE_CONFIG = {"apiKey": "________", "authDomain": "________", "databaseURL": "_______", "projectId": "_______", "storageBucket": "_______", "messagingSenderId": "_______", "appId": "_______", "measurementId": "_______"}`
   - **Ensure that this firebase config object is in your .env file in ONE SINGLE LINE, otherwise error occurs.**
     
   - *NOTE : If you haven't switched on Realtime database, then either "databaseURL" or "storageBucket" may not appear in your Firebase config object. Do not switch it on, since it isn't required. I had by mistake switched it on and then had to switch off.*



6. Now go to **https://aistudio.google.com/apikey** and create a new API key, select your project and copy the generated key. Paste this key in your .env file like this :
   - GEMINI_API_KEY = "_______"



7. Go to **https://www.brevo.com/** and create an account.
   - Click on the top right dropdown arrow, then on SMTP & API. Copy the values of Login (`________@smtp-relay.brevo.com`) and the Master Password (`________`) in the .env file like this :
   - `SMTP_USERNAME = "________@smtp-relay.brevo.com"`
   - `SMTP_PASSWORD = "________"`



8. Also add other SMTP related information like this :
   - `SMTP_SERVER = "smtp-relay.brevo.com"`
   - `SMTP_PORT = 587`
   - `RECIPIENT_EMAIL = "admin's_email_address"`



9. In **Brevo dashboard**, click on the top right dropdown arrow, then on Senders, Domains & Dedicated IPs. Here click on Add Sender, enter any name and the email you are going to use to create an account in this webapp.
   - You can enter any name, just ensure that the email address you enter should be used to create the account in the streamlit webapp, otherwise the feedback will not be received on the recipient email addres.






# NOTE :
- THE PLACES I HAVE LEFT BLANK IN HERE AND IN THE .env FILE, THOSE VALUES ARE SENSITIVE AND MAY REVEAL MY FIREBASE PROJECT DETAILS AND MY BREVO ACCOUNT DETAILS.
- REPLACE THE BLANKS WITH YOUR VALUES.
