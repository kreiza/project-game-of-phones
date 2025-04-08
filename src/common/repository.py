from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TypeVar, Generic

# Create a generic type variable to represent the entity type.
T = TypeVar("T")

class AbstractRepository(Generic[T], ABC):
    """
    Abstract base class defining the repository interface for generic entities.

    This interface can be implemented for different models/entities.
    """

    @abstractmethod
    def add(self, entity: T) -> T:
        """
        Add a new entity to the repository.

        :param entity: The entity to be added.
        :return: The entity with any updated attributes (e.g., assigned ID).
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[T]:
        """
        Retrieve an entity by its ID.

        :param entity_id: The unique identifier of the entity.
        :return: The entity if found, else None.
        """
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> List[T]:
        """
        List all entities in the repository.

        :return: A list of all entities.
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, entity_id: int, updates: Dict[str, Any]) -> Optional[T]:
        """
        Update an entity with the given updates.

        :param entity_id: The unique identifier of the entity to update.
        :param updates: A dictionary containing the fields to update.
        :return: The updated entity if successful, otherwise None.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        """
        Delete an entity by its ID.

        :param entity_id: The unique identifier of the entity to delete.
        :return: True if deletion was successful, False otherwise.
        """
        raise NotImplementedError
