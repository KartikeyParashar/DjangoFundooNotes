from .documents import NotesDocument


def search_notes(data):
    note = NotesDocument.search().query({
        "bool": {
            "must": [{"multi_match": {"query": data, "fields": ["title", "color"]}}],
        }
    })

    return note
