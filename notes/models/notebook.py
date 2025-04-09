from collections import UserDict

class NoteBook(UserDict):
    def add_note(self, record):
        self.data[record.title.value] = record

    def find_note(self, title):
        return self.data.get(title, f"No note found with name '{title}'")

    def delete_note(self, title):
        if title in self.data:
            del self.data[title]
            return "Note was deleted"
        return KeyError()
    
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
            return f"{note}"
        return f"No note found with name '{title}'"

    def show_all(self):
        return list(self.data.values())
    
