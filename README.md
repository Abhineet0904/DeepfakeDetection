# INSTRUCTIONS FOR TRAINING THE MODEL :

1. Download the .ipynb file from here and import it in Google Colab. Don't use Jupyter as it doesn't provide GPU/TPU acceleration.

2. Change the runtime to v2-8 TPU.

3. Upload the dataset in Google Drive.

4. After converting the keras model to TFLite, download the TFLite model and paste it in the root directory of your project.



#
---
---
#



# INSTRUCTIONS FOR LOCAL SETUP :

1. st_pages should be downloaded as :
   ```
   pip install st-pages==0.4.1
   ```
   - This version contains the show_pages() method, which is deprecated in recent versions.
   - Streamlit installed should be v1.25.0, to ensure compatibility with st-pages v0.4.1.


2. Create a firebase account.


3. In Firebase Authentication, go to Sign-in method, and add provider as Email/Password.


4. In project settings, go to Service accounts and click on Generate new private key. Paste the downloaded firebase-adminsdk file with .json extension in your project's root directory.
   - Then paste the name of this file in .env file in your root folder in the following way :
   ```
   FIREBASE_PRIVATE_JSON_KEY = "_______"
   ```


5. Then go to General in project settings. In SDK setup and configuration, click on Config radio button, and copy the Firebase configuration object. Paste the object in the .env file in the following way :
   ```
   FIREBASE_CONFIG = {"apiKey": "________", "authDomain": "________", "databaseURL": "_______", "projectId: "_______", "storageBucket": "_______", "messagingSenderId": "_______", "appId": "_______", "measurementId": "_______"}
   ```
   
   NOTE : If you haven't switched on Realtime database, then either "databaseURL" or "storageBucket" may not appear in your Firebase config object. Do not switch it on, since it isn't required. I had by mistake switched it on and then had to switch off.


6. Now go to https://aistudio.google.com/apikey and create a new API key, select your project and copy the generated key. Paste this key in your .env file like this :
   ```
   GEMINI_API_KEY = "_______"
   ```


7. Go to https://www.brevo.com/ and create an account.
   - Click on the top right dropdown arrow, then on SMTP & API. Copy the values of Login (________@smtp-relay.brevo.com)) and the Master Password in the .env file like this :
   ```
   SMTP_USERNAME = "________@smtp-relay.brevo.com"
   SMTP_PASSWORD = "________"
   ```


8. Also add other SMTP related information like this :
   ```
   SMTP_SERVER = "smtp-relay.brevo.com"
   SMTP_PORT = 587
   RECIPIENT_EMAIL = "________"
   ```
   NOTE : The RECIPIENT_EMAIL here, contains the email address you want to receive the user's feedback/query on.


9. Click on the top right dropdown arrow, then on Senders, Domains & Dedicated IPs. Here click on Add Sender, enter any name and the email you are going to use to create an account in this webapp.
   - You can enter any name, just ensure that the email address you enter should be used to create the account in the streamlit webapp, otherwise the feedback will not be received on the recipient email address.

```
Note : I have not provided the .env file or the Firebase Admin SDK private key, since they contain confidential data. Create your own .env file in the root directory of your project, and generate your own key.
```



#
---
---
#



# INSTRUCTIONS FOR DEPLOYMENT ON STREAMLIT CLOUD :

1. Upload your project on GitHub without the .env file or the .json file. Keep the repository public and include the `requirements.txt` file.


2. Run your project locally, click on Deploy, choose the `Deploy a public app from GitHub` option.


3. Enter your repository, branch, homepage, URL of your choice.


4. Click on Advanced, change the Python version to 3.11.
   Paste the content of the .env file in the `Secrets` textbox like this :
   ```
   FIREBASE_PRIVATE_JSON_KEY = '{ "type": "service_account", "project_id": "_____", "private_key_id": _____", "private_key": "-----BEGIN PRIVATE KEY-----\n_____\n-----END PRIVATE KEY-----\n", "client_email": "_____", "client_id": "_____", "auth_uri": "_____", "token_uri": "_____", "auth_provider_x509_cert_url": "_____", "client_x509_cert_url": "_____", "universe_domain": "_____" }'


   FIREBASE_CONFIG = '{ "apiKey": "_____", "authDomain": "_____", "databaseURL": "_____", "projectId": "deepfakedetection-5b108", "storageBucket": "_____", "messagingSenderId": "_____", "appId": "_____", "measurementId": "_____" }'


   GEMINI_API_KEY = "_____"

   SMTP_SERVER = "_____"
   SMTP_PORT = 587
   SMTP_USERNAME = "_____"
   SMTP_PASSWORD = "_____"
   RECIPIENT_EMAIL = "_____"
   ```


5. Click on Save and then on Deploy.

```
Note : For local deployment, you can paste the name of the Firebase Admin SDK ".json" file in `FIREBASE_PRIVATE_JSON_KEY`, but for Streamlit  Cloud deployment you will have to paste the entire JSON data in `FIREBASE_PRIVATE_JSON_KEY` in one single line.
```



#
---
---
#




# NOTE : THE ABOVE SOURCE CODE IS FOR DEPLOYMENT ON STREAMLIT COMMUNITY CLOUD. FOR LOCAL DEPLOYMENT, THE ABOVE SOURCE CODE WILL RESULT IN SOME ERRORS.
# `FOR LOCAL DEPLOYMENT, CONTACT ME ON LINKEDIN, MY ACCOUNT IS THERE IN THE PROJECT DESCRIPTION.`

