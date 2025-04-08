from datetime import datetime
from models import Tag
    
class Note:
    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.tags = []
        self.created_at = datetime.now()
        self.modified_at = self.created_at
        self.audit_message = ""

    def add_tag(self, tag):
        if tag not in self.tags:
            self.tags.append(Tag(tag))
            self.modified_at = datetime.now()
            self.audit_message = f"Last change: tag '{self.title}' has been added"
            print(f"Tag '{tag}' has been added to the note '{self.title}'.")
        else:
            print(f"Tag '{tag}' is already present in the note '{self.title}'.")

    def remove_tag(self, tag):
        if tag in self.tags:
            self.tags.remove(tag)
            self.modified_at = datetime.now()
            self.audit_message = f"Last change: tag '{self.title}' has been removed"
            print(f"Tag '{tag}' has been removed from the note '{self.title}'.")
        else:
            print(f"Tag '{tag}' does not exist in the note '{self.title}'.")
    
    def __str__(self):
        tag_names = [tag.name for tag in self.tags]
        return (f"Note Title: {self.title}\n"
                f"Content: {self.content}\n"
                f"Tags: {', '.join(tag_names) if tag_names else 'No tags'}\n"
                f"Created At: {self.created_at}\n"
                f"Last Modified: {self.modified_at}\n"
                f"Audit Message: {self.audit_message if self.audit_message else 'No changes made yet.'}")


note = Note("Meeting Notes", "Discussion about the project progress.")
note.add_tag("work")
note.add_tag("important")
print(note)  # Will call the __str__ method
note.remove_tag("work")
print(note)  # Will show updated note