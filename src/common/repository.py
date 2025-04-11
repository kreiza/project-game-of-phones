from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Dict, Any

T = TypeVar('T')


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
    def get(self, **search_params) -> Optional[T]:
        """
        Retrieve an entity using arbitrary search parameters.
        This allows you to perform searches based on non-ID fields
        (e.g., name or tags) and returns the entity if exactly one match is found.

        :param search_params: Arbitrary keyword arguments representing search criteria.
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
