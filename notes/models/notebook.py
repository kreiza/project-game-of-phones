from collections import UserDict

class NoteBook(UserDict):
    def add_note(self, record):
        self.data[record.name.value] = record

    def find_note(self, name):
        return self.data.get(name, f"No note found with name '{name}'")

    def delete_note(self, name):
        if name in self.data:
            del self.data[name]
            return "Note was deleted"
        return KeyError()
    
    def search(self, keyword):
        result = []
        for note in self.data.values():
            if (
                keyword.lower() in note.name.lower() or
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
    
    def show_note(self, name):
        note = self.find_note(name)
        if note:
            return f"{note}"
        return f"No note found with name '{name}'"

    def show_all(self):
        return list(self.data.values())
    
