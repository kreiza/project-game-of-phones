from abc import abstractmethod, ABC
from typing import Optional, List, Dict, Any

from src.common.models import PhoneBookRecord


class AbstractRepository(ABC):
    """
    Abstract base class defining the repository interface for phonebook records.
    """

    @abstractmethod
    def add(self, record: PhoneBookRecord) -> PhoneBookRecord:
        """
        Add a new phonebook record to the repository.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, record_id: int) -> Optional[PhoneBookRecord]:
        """
        Retrieve a phonebook record by its ID.
        """
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> List[PhoneBookRecord]:
        """
        List all phonebook records.
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, record_id: int, updates: Dict[str, Any]) -> Optional[PhoneBookRecord]:
        """
        Update a phonebook record with the given updates.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, record_id: int) -> bool:
        """
        Delete a phonebook record by its ID.
        """
        raise NotImplementedError

