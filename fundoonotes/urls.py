from django.urls import path
from . import views


urlpatterns = [
    path('note/create/', views.CreateNote.as_view(), name='create_note'),
    path('note/get/', views.GetNote.as_view(), name='get_note'),
    path('note/get/<id>/', views.GetNoteWithID.as_view(), name='get_note_with_id'),
    path('note/update/<id>/', views.UpdateNoteWithID.as_view(), name='update_note_with_id'),
    path('note/delete/<id>/', views.DeleteNoteWithID.as_view(), name='delete_note_with_id'),
    path('label/create/', views.CreateLabel.as_view(), name='create_label'),
    path('label/get/', views.GetLabel.as_view(), name='get_label'),
    path('label/get/<id>/', views.GetLabelWithId.as_view(), name='get_label_with_id'),
    path('label/update/<id>/', views.UpdateLabelWithId.as_view(), name='update_label_with_id'),
    path('label/delete/<id>/', views.DeleteLabelWithId.as_view(), name='delete_label_with_id'),
    path('note/archive_note/', views.ArchiveNotes.as_view(), name='archive_notes'),
    path('note/trash_note/', views.TrashNotes.as_view(), name='trash_notes'),
    path('note/reminder_notes/', views.ReminderNotes.as_view(), name='reminder_notes'),
    path('note/pagination/', views.PaginationForNotes.as_view(), name='pagination'),
    path('note/search/', views.SearchNote.as_view(), name='search')

]
