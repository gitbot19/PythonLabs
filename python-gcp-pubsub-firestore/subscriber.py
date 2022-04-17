from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
from google.cloud import firestore

# The `project` parameter is optional and represents which project the client
# will act on behalf of. If not supplied, the client falls back to the default
# project inferred from the environment.

# TODO(developer)
project_id = "greybunny"
db = firestore.Client(project=project_id)
subscription_id = "my-sub"
# Number of seconds the subscriber should listen for messages
timeout = 5

def firestore(doc_id):
    ''' Add messages to firestore '''
    name = doc_id.decode("utf-8")
    print(name.split( ))
    split_name = name[6]
    data = {
        u'name': split_name
    }
    # Add a new doc in collection 'messages' with ID 'the msg'
    db.collection(u'messages').document(name).set(data)
    return

subscriber = pubsub_v1.SubscriberClient()
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_id}`
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    print(f"Received {message.data}.")
    firestore(doc_id = message.data)
    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n")

# Wrap subscriber in a 'with' block to automatically call close() when done.
with subscriber:
    try:
        # When `timeout` is not set, result() will block indefinitely,
        # unless an exception is encountered first.
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()  # Trigger the shutdown.
        streaming_pull_future.result()  # Block until the shutdown is complete.