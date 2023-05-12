from abc import ABC, abstractmethod


class GetVacancies(ABC):

    @abstractmethod
    def set_params(self, key: str, value: str | int):
        pass

    @abstractmethod
    def reset_params(self):
        pass

    @abstractmethod
    def set_headers(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def display_vacancies(self):
        pass

    @abstractmethod
    def provide_vacancies(self) -> list:
        pass


class StorageVac(ABC):
    @staticmethod
    @abstractmethod
    def to_dict(vac_obj):
        pass

    @abstractmethod
    def update(self, new_data: list):
        pass

    @abstractmethod
    def load_vac(self, keywords: str = "") -> list:
        pass

    @abstractmethod
    def mark_del(self, id_vac: str):
        pass

    @abstractmethod
    def clear_marks(self):
        pass

    @abstractmethod
    def del_marked(self):
        pass

    @abstractmethod
    def del_all(self):
        pass

    @staticmethod
    @abstractmethod
    def display_vac(data: list):
        pass
