import random 

user_ids = list(range(1, 10))
recipient_ids = list(range(1, 10))

def generate_message():
    random_user_id = random.choice(user_ids)

    # Copy the recipients array
    recipient_ids_copy = recipient_ids.copy()

    # User can't send message to himself
    recipient_ids_copy.remove(random_user_id)
    random_recipient_id = random.choice(recipient_ids_copy)

    # Generate a random message
    message = f'This is a message from user {random_user_id} to user {random_recipient_id}'

    return {
        'user_id': random_user_id,
        'recipient_id': random_recipient_id,
        'message': message
    }
