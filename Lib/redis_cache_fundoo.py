import pickle


from Lib import redis_cache
from fundoonotes.models import Note, Label


def update_redis(user):
    """
    :param user:This is our LOGGED IN user
    :return:This function is used to update the notes in redis
    """
    try:
        all_notes = Note.objects.filter(user_id=int(user.id), is_trashed=False, is_archive=False)
        all_archive_notes = Note.objects.filter(user_id=int(user.id), is_archive=True)
        all_trash_notes = Note.objects.filter(user_id=int(user.id), is_trashed=True)
        if all_notes:
            notes = pickle.dumps(all_notes)
            redis_cache.Set(user.username + ' notes', notes)
        if all_archive_notes:
            archive_notes = pickle.dumps(all_archive_notes)
            redis_cache.Set(user.username + ' archive_notes', archive_notes)
        if all_trash_notes:
            trash_notes = pickle.dumps(all_trash_notes)
            redis_cache.Set(user.username + ' trash_notes', trash_notes)
    except Exception:
        return False


def label_update_in_redis(user):
    """
    :param user:this our logged in user
    :return:this function is used for update_redis labels in redis
    """
    try:
        # import pdb
        # pdb.set_trace()
        labels = Label.objects.filter(user_id=user.id)
        all_labels = pickle.dumps(labels)
        redis_cache.Set(user.username + ' labels', all_labels)

    except Exception:
        return False
