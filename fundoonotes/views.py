from django.shortcuts import render

# Create your views here.

"""
******************************************************************************************************************
Purpose: In this views module, I created a rest_api for CRUD operations for NOTES, LABELS,
         Rest API for TRASH and ARCHIVE Notes, Reminder API
Author:  KARTIKEY PARASHAR
Since :  20-02-2020
******************************************************************************************************************
"""
import datetime
import json
import logging
import pickle

import jwt
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from Lib import redis_cache
from Lib.user_detail import get_user
from Lib.smd_response import SMD_Response
from Lib.decorators import login_required
from Lib.redis_cache_fundoo import update_redis, label_update_in_redis

from .models import Note, Label
from .documents import NotesDocument
from .serializers import NoteSerializer, LabelSerializer, SearchSerializer, CollaboratorSerializer

logger = logging.getLogger(__name__)
User = get_user_model()


class CreateNote(GenericAPIView):
    serializer_class = NoteSerializer

    def post(self, request, *args, **kwargs):
        """

        :param request:Request data from a Logged In user by passing a Token
        :return:Save the Note in the database
        """
        try:
            # import pdb
            # pdb.set_trace()
            note_user = get_user(request)
            if note_user:
                data = request.data
                data['user'] = str(note_user.id)
                if 'collaborator' in data:
                    collaborator_list = []
                    collaborators = data['collaborator']
                    for mail in collaborators:
                        user = User.objects.filter(email=mail)
                        if user:
                            for usr in user:
                                collaborator_list.append(usr.id)
                        else:
                            return Response(SMD_Response(message="Something went wrong when "
                                                                 "validating your collaborator"))
                    data['collaborator'] = collaborator_list
                if 'label' in data:
                    label_list = []
                    labels = data['label']
                    for name in labels:
                        user = Label.objects.get(name=name, user_id=note_user.id)
                        if user:
                            label_list.append(user.id)
                        else:
                            return Response(SMD_Response(message="Something went wrong when"
                                                                 "validating your label"))
                    data['label'] = label_list
                if 'reminder' in data:
                    remainder = data['reminder']
                    rem = datetime.datetime.strptime(remainder, "%Y-%m-%d %H:%M:%S")
                    if rem:
                        data['reminder'] = remainder
                    else:
                        return Response(SMD_Response(message="Does Not match format '%Y-%m-%d %H:%M:%S"))
                serializer = NoteSerializer(data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    update_redis(note_user)
                    logger.info("Successfully Note Created")
                    smd = SMD_Response(status=True, message="Successfully Note Created",
                                       data=[serializer.data])
                    return Response(smd, status=status.HTTP_201_CREATED)
                else:
                    logger.error("Invalid Format or Details!!!")
                    smd = SMD_Response(status=True, message="Note Creation Failed",
                                       data=[serializer.errors])
                    return Response(smd, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(SMD_Response(message="You Need to LOGIN FIRST and Provide Valid Credentials"))
        except Exception as e:
            logger.warning("Something went wrong " + str(e))
            smd = SMD_Response(status=False, message="Something Went Wrong")
            return Response(smd, status=status.HTTP_404_NOT_FOUND)


class GetNote(GenericAPIView):
    serializer_class = NoteSerializer

    def get(self, request, *args, **kwargs):
        """

        :param request:User request for getting all the notes
        :return:All the Notes belongs to the Logged In User
        """
        try:
            # import pdb
            # pdb.set_trace()
            note_user = get_user(request)
            if note_user:
                note_data = redis_cache.Get(note_user.username + ' notes')
                if note_data:
                    notes = pickle.loads(note_data)
                    serializer = NoteSerializer(notes, many=True)
                    logger.info("Successfully Read Notes from REDIS")
                    smd = SMD_Response(status=True, message="Successfully Read Notes from REDIS",
                                       data=[serializer.data])
                    logger.info('Successfully Get notes from Redis')
                    return Response(smd, status=status.HTTP_200_OK)
                else:
                    all_notes = Note.objects.filter(user_id=note_user.id, is_archive=False, is_trashed=False)
                    if all_notes:
                        serializer = NoteSerializer(all_notes, many=True)
                        # notes = pickle.dumps(all_notes)
                        update_redis(note_user)
                        smd = SMD_Response(status=True, message="Successfully Read Notes from Database",
                                           data=[serializer.data])
                        logger.info('successfully get notes from database')
                        return Response(smd, status=status.HTTP_200_OK)
                    else:
                        logger.error("No data available to be fetch from Redis and in DATABASE")
                        smd = SMD_Response(status=False, message="No Content Available")
                        return Response(smd, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(SMD_Response(message="You Need to LOGIN FIRST and Provide Valid Credentials"))
        except Exception as e:
            logger.warning("Something went wrong" + str(e))
            smd = SMD_Response(status=False, message="Something went wrong",
                               data=[])
            return Response(smd, status=status.HTTP_404_NOT_FOUND)


class GetNoteWithID(GenericAPIView):
    serializer_class = NoteSerializer

    def get(self, request, id, *args, **kwargs):
        """

        :param request: User request for get the particular Note, operation
        :param id: Here, we pass an ID for update of a specific Note
        :return: It will get a requested Note with ID from the Database
        """
        try:
            # import pdb
            # pdb.set_trace()
            note_user = get_user(request)
            if note_user:
                note_data = Note.objects.filter(id=id, user_id=note_user.id)
                if note_data:
                    serializer = NoteSerializer(note_data, many=True)
                    logger.info("Successfully Read Notes")
                    smd = SMD_Response(status=True, message="Successfully Read Notes",
                                       data=[serializer.data])
                    logger.info('Successfully Get notes')
                    return Response(smd, status=status.HTTP_200_OK)
                else:
                    logger.error("No data available/invalid id or user_id")
                    smd = SMD_Response(status=False, message="No Content Available",
                                       data=[])
                    return Response(smd, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(SMD_Response(message="You Need to LOGIN FIRST and Provide Valid Credentials"))

        except Exception as e:
            logger.warning("Something went wrong" + str(e))
            smd = SMD_Response(status=False, message="Something Went Wrong")
            return Response(smd, status=status.HTTP_404_NOT_FOUND)


class UpdateNoteWithID(GenericAPIView):
    serializer_class = NoteSerializer

    def put(self, request, id, *args, **kwargs):
        """

        :param request:User request for put(update) the Note, operation
        :param id:Here, we pass an ID for update of a specific Note
        :return:It will Update a requested Note in Database
        """
        try:
            # import pdb
            # pdb.set_trace()
            note_user = get_user(request)
            if note_user:
                note = Note.objects.get(id=id, user_id=note_user.id)
                if note is not None:
                    data = request.data
                    if 'collaborator' in data:
                        collaborator_list = []
                        collaborators = data['collaborator']
                        for mail in collaborators:
                            user = User.objects.filter(email=mail)
                            if user:
                                for usr in user:
                                    collaborator_list.append(usr.id)
                            else:
                                return Response(SMD_Response(message="Something went wrong when "
                                                                     "validating your collaborator"))
                        data['collaborator'] = collaborator_list
                    if 'label' in data:
                        label_list = []
                        labels = data['label']
                        for name in labels:
                            user = Label.objects.filter(name=name, user_id=note_user.id)
                            if user:
                                label_list.append(user.id)
                            else:
                                return Response(SMD_Response(message="Something went wrong when"
                                                                     "validating your label"))
                        data['label'] = label_list
                    if 'reminder' in data:
                        remainder = data['reminder']
                        rem = datetime.datetime.strptime(remainder, "%Y-%m-%d %H:%M:%S")
                        if rem:
                            data['reminder'] = remainder
                        else:
                            return Response(SMD_Response(message="Does Not match format '%Y-%m-%d %H:%M:%S"))
                    serializer = NoteSerializer(note, data=data)
                    if serializer.is_valid():
                        serializer.save()
                        update_redis(note_user)
                        logger.info("Successfully Updated the Note")
                        smd = SMD_Response(status=True, message="Note Successfully Updated",
                                           data=[serializer.data])
                        return Response(smd, status=status.HTTP_202_ACCEPTED)
                    else:
                        logger.error("Please provide valid details")
                        smd = SMD_Response(message="Invalid Request/No such query exist",
                                           data=[serializer.errors])
                        return Response(smd, status=status.HTTP_400_BAD_REQUEST)
                else:
                    logger.info("No DATA Present")
                    return Response(SMD_Response(message="No Data Present in Note"),
                                    status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(SMD_Response(message="You Need to LOGIN FIRST and Provide Valid Credentials"))

        except Exception as e:
            logger.warning("SOMETHING WENT WRONG" + str(e))
            return Response(SMD_Response(message="Please Provide a Valid ID/Valid token or "
                                                 "Something Went Wrong"),
                            status=status.HTTP_400_BAD_REQUEST)


class DeleteNoteWithID(GenericAPIView):
    serializer_class = NoteSerializer

    def delete(self, request, id, *args, **kwargs):
        """

        :param request: User Request for Delete a Note
        :param id: Here, we pass a ID for deleting requested ID
        :return: This function delete the requested note from the DATABASE
        """
        try:
            # import pdb
            # pdb.set_trace()
            note_user = get_user(request)
            if note_user:
                note = Note.objects.filter(id=id, user_id=note_user.id)
                if note:
                    note.delete()
                    update_redis(note_user)
                    logger.info("Note Deleted")
                    return Response(SMD_Response(status=True, message="Successfully Deleted the Note"),
                                    status=status.HTTP_204_NO_CONTENT)
                else:
                    logger.error("Please provide valid details")
                    smd = SMD_Response(message="Not found such Note")
                    return Response(smd, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(SMD_Response(message="You Need to LOGIN FIRST and Provide Valid Credentials"))

        except Exception as e:
            logger.warning("SOMETHING WENT WRONG" + str(e))
            return Response(SMD_Response(message="Not a VALID ID/Invalid Token or Something went wrong!!"),
                            status=status.HTTP_400_BAD_REQUEST)


class GetLabel(GenericAPIView):
    serializer_class = LabelSerializer

    def get(self, request, *args, **kwargs):
        """

        :param request:User request for getting all the Labels
        :return:All the Labels belongs to the Logged In User
        """
        try:
            # import pdb
            # pdb.set_trace()
            label_user = get_user(request)
            if label_user:
                label_data = redis_cache.Get(label_user.username + ' labels')
                if label_data:
                    labels = pickle.loads(label_data)
                    serializer = LabelSerializer(labels, many=True)
                    logger.info("Successfully Read Labels from Redis")
                    smd = SMD_Response(status=True, message="Successfully Read Labels from Redis",
                                       data=[serializer.data])
                    logger.info('successfully get labels from redis')
                    return Response(smd, status=status.HTTP_200_OK)
                else:
                    all_labels = Label.objects.filter(user_id=label_user.id)
                    if all_labels:
                        serializer = LabelSerializer(all_labels, many=True)
                        label_update_in_redis(label_user)
                        smd = SMD_Response(status=True, message="Successfully Read Labels from Database",
                                           data=[serializer.data])
                        logger.info('successfully get labels from database')
                        return Response(smd, status=status.HTTP_200_OK)
                    else:
                        logger.error("No data available to be fetch from Redis")
                        smd = SMD_Response(status=False, message="No Content Available",
                                           data=[])
                        return Response(smd, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(SMD_Response(message="You Need to LOGIN FIRST and Provide Valid Credentials"))
        except Exception as e:
            logger.warning("Something went wrong" + str(e))
            smd = SMD_Response(status=False, message="Something went wrong")
            return Response(smd, status=status.HTTP_404_NOT_FOUND)


class CreateLabel(GenericAPIView):
    serializer_class = LabelSerializer

    def post(self, request, *args, **kwargs):
        """

        :param request:Request data from a Logged In user by passing a Token
        :return:Save the Labels in the database
        """
        try:
            # import pdb
            # pdb.set_trace()
            label_user = get_user(request)
            if label_user:
                data = request.data
                data['user'] = str(label_user.id)
                if Label.objects.filter(name=data['name'], user_id=label_user.id).exists():
                    logger.info("Label already Exists")
                else:
                    serializer = LabelSerializer(data=data)
                    if serializer.is_valid():
                        serializer.save()
                        label_update_in_redis(label_user)
                        logger.info("Successfully Note Created")
                        smd = SMD_Response(status=True, message="Successfully Label Created",
                                           data=[serializer.data])
                        return Response(smd, status=status.HTTP_201_CREATED)
                    else:
                        logger.error("Invalid Format or Details!!!")
                        smd = SMD_Response(status=True, message="Label Creation Failed",
                                           data=[serializer.errors])
                        return Response(smd, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(SMD_Response(message="You Need to LOGIN FIRST and Provide Valid Credentials"))
        except Exception as e:
            logger.warning("Something went wrong" + str(e))
            smd = SMD_Response(status=False, message="Something Went Wrong")
            return Response(smd, status=status.HTTP_404_NOT_FOUND)


class GetLabelWithId(GenericAPIView):
    serializer_class = LabelSerializer

    def get(self, request, id, *args, **kwargs):
        """

        :param request: User request for get the particular Note, operation
        :param id: Here, we pass an ID for update of a specific Note
        :return: It will get a requested Note with ID from the Database
        """
        try:
            # import pdb
            # pdb.set_trace()
            label_user = get_user(request)
            if label_user:
                label_data = Label.objects.filter(id=id, user_id=label_user.id)
                if label_data:
                    serializer = LabelSerializer(label_data, many=True)
                    logger.info("Successfully Read Notes")
                    smd = SMD_Response(status=True, message="Successfully Read Labels",
                                       data=[serializer.data])
                    logger.info('Successfully Get Labels')
                    return Response(smd, status=status.HTTP_200_OK)
                else:
                    logger.error("No data available/invalid id or user_id")
                    smd = SMD_Response(status=False, message="No Content Available")
                    return Response(smd, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(SMD_Response(message="You Need to LOGIN FIRST and Provide Valid Credentials"))

        except Exception as e:
            logger.warning("Something went wrong" + str(e))
            smd = SMD_Response(status=False, message="Something Went Wrong",
                               data=[])
            return Response(smd, status=status.HTTP_404_NOT_FOUND)


class UpdateLabelWithId(GenericAPIView):
    serializer_class = LabelSerializer

    def put(self, request, id, *args, **kwargs):
        """

        :param request:User request for put(update) the LABEL operation
        :param id:Here, we pass an ID for update of a specific Label
        :return:It will Update a requested Label in Database
        """
        try:
            # import pdb
            # pdb.set_trace()
            label_user = get_user(request)
            if label_user:
                label = Label.objects.get(id=id, user_id=label_user.id)
                if label is not None:
                    data = request.data
                    serializer = LabelSerializer(label, data=data)
                    if serializer.is_valid():
                        serializer.save()
                        label_update_in_redis(label_user)
                        logger.info("Successfully Updated the label")
                        smd = SMD_Response(status=True, message="Label Successfully Updated",
                                           data=[serializer.data])
                        return Response(smd, status=status.HTTP_202_ACCEPTED)
                    else:
                        logger.error("Please provide valid details")
                        smd = SMD_Response(message="Invalid Request/No such query exist",
                                           data=[serializer.errors])
                        return Response(smd, status=status.HTTP_400_BAD_REQUEST)
                else:
                    logger.info("No DATA Present")
                    return Response(SMD_Response(message="No Data Present in Label"),
                                    status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(SMD_Response(message="You Need to LOGIN FIRST and Provide Valid Credentials"))

        except Exception as e:
            logger.warning("SOMETHING WENT WRONG" + str(e))
            return Response(SMD_Response(message="Please Provide a Valid ID/Valid token or "
                                                 "Something Went Wrong"),
                            status=status.HTTP_400_BAD_REQUEST)


class DeleteLabelWithId(GenericAPIView):
    serializer_class = LabelSerializer

    def delete(self, request, id, *args, **kwargs):
        """

        :param request: User Request for Delete a LABEL
        :param id: Here, we pass an ID for deleting requested ID
        :return: This function delete the requested label from the DATABASE
        """
        try:
            label_user = get_user(request)
            if label_user:
                label = Label.objects.get(id=id, user_id=label_user.id)
                if label is not None:
                    label.delete()
                    logger.info("Label Deleted")
                    label_update_in_redis(label_user)
                    return Response(SMD_Response(status=True, message="Successfully Deleted the Label"),
                                    status=status.HTTP_204_NO_CONTENT)
                else:
                    logger.error("Please provide valid details")
                    smd = SMD_Response(message="Not found such Label")
                    return Response(smd, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(SMD_Response(message="You Need to LOGIN FIRST and Provide Valid Credentials"))
        except Exception as e:
            logger.warning("SOMETHING WENT WRONG" + str(e))
            return Response(SMD_Response(message="Not a VALID ID/Invalid Token or Something went wrong!!"),
                            status=status.HTTP_400_BAD_REQUEST)


class AddCollaborator(GenericAPIView):
    serializer_class = CollaboratorSerializer

    def put(self, request, id, *args, **kwargs):
        """

        :param request: User add a collaborator to the note
        :return: update the database with collaborator
        """
        try:
            # import pdb
            # pdb.set_trace()
            collaborator_user = get_user(request)
            if collaborator_user:
                note = Note.objects.get(id=id, user_id=collaborator_user.id)
                if note is not None:
                    data = request.data
                    if 'collaborator' in data:
                        collaborator_list = []
                        collaborators = data['collaborator']
                        for mail in collaborators:
                            user = User.objects.filter(email=mail)
                            if user:
                                for usr in user:
                                    collaborator_list.append(usr.id)
                            else:
                                logger.error("Invalid Format or Details!!!")
                                return Response(SMD_Response(message="Something went wrong when "
                                                                     "validating your collaborator"))
                        data['collaborator'] = collaborator_list
                    serializer = CollaboratorSerializer(note, data=data)
                    if serializer.is_valid():
                        serializer.save()
                        update_redis(collaborator_user)
                        logger.info("Successfully Collaborator Added")
                        smd = SMD_Response(status=True, message="Successfully Added Collaborator",
                                           data=[serializer.data])
                        return Response(smd, status=status.HTTP_201_CREATED)

                    else:
                        logger.error("Invalid Format or Details!!!")
                        smd = SMD_Response(status=True, message="Collaborator Addition Failed",
                                           data=[serializer.errors])
                        return Response(smd, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response(SMD_Response(message="You Need to LOGIN FIRST and Provide Valid Credentials"))
        except Exception as e:
            logger.warning("Something went wrong" + str(e))
            smd = SMD_Response(status=False, message="Something Went Wrong")
            return Response(smd, status=status.HTTP_404_NOT_FOUND)


class ArchiveNotes(GenericAPIView):
    serializer_class = NoteSerializer

    def get(self, request, *args, **kwargs):
        """
        :param request:User request for get all archive notes of LOGGED IN User
        :return:This function return all the archive notes of LOGGED IN user
        """
        try:
            # import pdb
            # pdb.set_trace()
            archive_notes_user = get_user(request)
            if archive_notes_user:
                archive_note_data = redis_cache.Get(archive_notes_user.username + ' archive_notes')
                if archive_note_data is not None:
                    archive_note = pickle.loads(archive_note_data)
                    serializer = NoteSerializer(archive_note, many=True)
                    logger.info("Successfully Get the ARCHIVED Notes")
                    smd = SMD_Response(status=True, message="Successfully Note Found",
                                       data=[serializer.data])
                    return Response(smd, status=status.HTTP_302_FOUND)
                else:
                    logger.error("Please provide the valid NOTE Details and Token")
                    smd = SMD_Response(status=True,
                                       message="No Archive Notes are there for this User_ID EXISTS!!",
                                       data=['NOT FOUND'])
                    return Response(smd, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(SMD_Response(message="You Need to LOGIN FIRST and Provide Valid Credentials"))

        except Exception as e:
            logger.warning("SOMETHING WENT WRONG" + str(e))
            return Response(SMD_Response(message="Not a VALID User/Invalid Token or Something went wrong!!"),
                            status=status.HTTP_400_BAD_REQUEST)


class TrashNotes(GenericAPIView):
    serializer_class = NoteSerializer

    def get(self, request, *args, **kwargs):
        """
        :param request:User request for get all archive notes of LOGGED IN User
        :return:This function return all the archive notes of LOGGED IN user
        """
        try:
            # import pdb
            # pdb.set_trace()
            trash_notes_user = get_user(request)
            if trash_notes_user:
                trash_note_data = redis_cache.Get(trash_notes_user.username + ' trash_notes')
                if trash_note_data is not None:
                    trash_note = pickle.loads(trash_note_data)
                    serializer = NoteSerializer(trash_note, many=True)
                    logger.info("Successfully Get the ARCHIVED Notes")
                    smd = SMD_Response(status=True, message="Successfully Note Found",
                                       data=[serializer.data])
                    return Response(smd, status=status.HTTP_302_FOUND)
                else:
                    logger.error("Please provide the valid NOTE Details and Token")
                    smd = SMD_Response(status=True,
                                       message="No Trash Notes are there for this User_ID EXISTS!!",
                                       data=["Not FOUND"])
                    return Response(smd, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(SMD_Response(message="You Need to LOGIN FIRST and Provide Valid Credentials"))
        except Exception as e:
            logger.warning("SOMETHING WENT WRONG" + str(e))
            return Response(SMD_Response(message="Not a VALID User/Invalid Token or Something went wrong!!"),
                            status=status.HTTP_400_BAD_REQUEST)


class ReminderNotes(GenericAPIView):
    serializer_class = NoteSerializer

    @method_decorator(login_required, name='dispatch')
    def get(self, request, *args, **kwargs):
        try:
            # import pdb
            # pdb.set_trace()
            remind_user = get_user(request)
            if remind_user:
                reminder_note = Note.objects.filter(user_id=remind_user.id, reminder__isnull=False)
                serializer = NoteSerializer(reminder_note, many=True)
                if reminder_note is not None:
                    logger.info("Successfully Get the Reminder Notes")
                    smd = SMD_Response(status=True, message="Successfully Note Found",
                                       data=[serializer.data])
                    return Response(smd, status=status.HTTP_302_FOUND)
                else:
                    logger.error("Please provide the valid NOTE Details and Token")
                    smd = SMD_Response(status=True,
                                       message="No Reminder Notes are there for this User_ID EXISTS!!",
                                       data=[serializer.errors])
                    return Response(smd, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(SMD_Response(message="You Need to LOGIN FIRST and Provide Valid Credentials"))
        except Exception as e:
            logger.warning("SOMETHING WENT WRONG" + str(e))
            return Response(SMD_Response(message="Not a VALID User/Invalid Token or Something went wrong!!"),
                            status=status.HTTP_400_BAD_REQUEST)


class PaginationForNotes(GenericAPIView):

    def get(self, request, *args, **kwargs):
        """
        :param request:user request for get pages
        :return:this function used for pagination means gives data after request of page
        """
        try:
            # import pdb
            # pdb.set_trace()
            note_list = Note.objects.all()
            paginator = Paginator(note_list, 4)
            page = request.GET.get('page', 1)
            notes = paginator.page(page)
        except PageNotAnInteger:
            notes = paginator.page(1)
        except EmptyPage:
            notes = paginator.page(paginator.num_pages)
        except Exception as e:
            logger.error("Something went wrong" + str(e))
            smd = SMD_Response()
            return HttpResponse(smd, status=status.HTTP_400_BAD_REQUEST)
        return render(request, 'fundoonotes/pagination.html', {'notes': notes})


# class SearchNote(GenericAPIView):
#     serializer_class = SearchSerializer
#
#     def post(self, request):
#         """
#
#         :param request:user request for POST
#         :return: the requested note
#         """
#         try:
#             title = request.data['title']
#             if title:
#                 note = NotesDocument.search().query("match", title=title)
#                 serializer = NoteSerializer(note.to_queryset(), many=True)
#                 if serializer:
#                     logger.info("Successfully Found Note")
#                     return Response(SMD_Response(status=True, message="Successfully Found the Note",
#                                                  data=[serializer.data]), status=status.HTTP_200_OK)
#                 else:
#                     logger.error("Please Provide Valid DATA")
#                     return Response(SMD_Response(message="Please Provide Valid Data"),
#                                     status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 logger.info("Title Not Found")
#                 return Response(SMD_Response(message="Title Not Found"), status=status.HTTP_404_NOT_FOUND)
#
#         except Exception as e:
#             logger.error("Something Went Wrong " + str(e))
#             return Response(SMD_Response(message="Something Went Wrong"), status=status.HTTP_400_BAD_REQUEST)
