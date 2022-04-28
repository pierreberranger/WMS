from sys import call_tracing
from package_v2 import Package
import functools

class Shipment(set):

    def __getitem__(self, id: int) -> Package:
        for package in self:
            if package.id == id:
                return package
        raise KeyError("This id does not exist")

    def remove_package(self, id: int) -> None:
        for package in self.copy():
            if package.id == id:
                self.remove(package)
                return None
        raise KeyError("This id does not exist")

    def package_filter(self, caracteristics_to_filter: dict): # Ici les listes ne seront jamais modifiées
        return Shipment(filter(lambda package: 
                                    functools.reduce(lambda bol, key:
                                        bol and package.__dict__[key] in caracteristics_to_filter[key], 
                                        caracteristics_to_filter, True), 
                                self))
        
    