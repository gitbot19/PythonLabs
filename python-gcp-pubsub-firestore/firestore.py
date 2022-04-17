from shared_imports import *
import random
import country

def create_user_profile():
    profile = dict()
    random_country = random.choice(country.countries)
    profile['Age'] = random.randint(15,70)
    profile['Country_name'] = random_country[1]
    profile['Country_code'] = random_country[0]
    return profile

def add_collection_firestore(doc_id):
    ''' Add messages to firestore '''
    db = firestore.Client()
    name = doc_id.decode("utf-8")
    names_list = name.split(' ')
    user_profile = dict()
    user_profile = create_user_profile()
    data = {
        u'name': names_list[3],
        u'age' : user_profile['Age'],
        u'country': user_profile['Country_name'],
        u'country_code': user_profile['Country_code']
    }
    # Add a new doc in collection 'messages' with ID 'the msg'
    db.collection(u'messages').document(name).set(data)
    return

def delete_full_collection():
    '''This function will delete your entire collection.'''
    my_collection = 'messages'
    db = firestore.Client()

    # [START firestore_data_delete_collection]
    def delete_collection(coll_ref, batch_size):
        docs = coll_ref.limit(batch_size).stream()
        deleted = 0

        for doc in docs:
            print(f'Deleting doc {doc.id} => {doc.to_dict()}')
            doc.reference.delete()
            deleted = deleted + 1

        if deleted >= batch_size:
            return delete_collection(coll_ref, batch_size)
    # [END firestore_data_delete_collection]

    delete_collection(db.collection(my_collection), 10)