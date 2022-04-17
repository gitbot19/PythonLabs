In this example you will learn how to publish message on to pubsub topic then read those messages from pubsub subscription and add them to gcp firestore.
 
Follow the steps:

- Create python virtual environment

- Install all necessory libraries using pip (google cloud pubsub, firestore etc.)

- Create service account with necessary permissions and download the json key file

- export GOOGLE_APPLICATION_CREDENTIALS="/tmp/service-account-file.json"

- python publisher.py && python subscriber.py

The end