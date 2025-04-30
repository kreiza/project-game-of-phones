from collections import UserDict
from datetime import datetime

class Note:
    def __init__(self, title, content, tags=None):
        self.title = title
        self.content = content
        self.tags = tags if tags else []
        self.updated_at = datetime.now()
        self.audit_message = f"Note '{self.title}' created."

    def edit_note(self, title=None, content=None):
        if title:
            self.title = title
        if content:
            self.content = content
        self.updated_at = datetime.now()
        self.audit_message = f"Last change: Note '{self.title}' and content has been changed."


class NoteBook(UserDict):
    def add_note(self, record):
        note = self.find_note(record.title)
        if note:
            return f"Note with title '{record.title}' already exists."
        self.data[record.title] = record

    def find_note(self, title):
        return self.data.get(title, None)

    def delete_note(self, title):
        if title in self.data:
            del self.data[title]
            return f"Note '{title}' was deleted."
        return f"No note found with title '{title}'."
    
    def search(self, keyword):
        result = []
        for note in self.data.values():  
            if (
                keyword.lower() in note.title.lower() or
                keyword.lower() in note.content.lower() or
                any(keyword.lower() in tag.lower() for tag in note.tags)
            ):
                result.append(note)
        return result
    
    def search_by_tag(self, keyword):
        result = []
        for note in self.data.values():  
            if keyword.lower() in (t.lower() for t in note.tags):
                result.append(note)
        return result
    
    def show_note(self, title):
        note = self.find_note(title)
        if note:
            return f"Title: {note.title}\nContent: {note.content}\nTags: {note.tags}\nLast Updated: {note.updated_at}\nAudit: {note.audit_message}"
        return f"No note found with title '{title}'."

    def show_all(self):
        if not self.data:
            return "No notes available."
    
        return "\n\n".join(str(note) for note in self.data.values())
