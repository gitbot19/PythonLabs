from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
from shared_imports import *
from firestore import delete_full_collection,add_collection_firestore

# The `project` parameter is optional and represents which project the client
# will act on behalf of. If not supplied, the client falls back to the default
# project inferred from the environment.

# TODO(developer)
project_id = "greybunny"
db = firestore.Client(project=project_id)
subscription_id = "my-sub"
# Number of seconds the subscriber should listen for messages
timeout = 5

delete_full_collection() # This fucntion delete the entire collection

subscriber = pubsub_v1.SubscriberClient()
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_id}`
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    print(f"Received {message.data}.")
    add_collection_firestore(doc_id = message.data)
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