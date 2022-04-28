from backend.package_v2 import Package
import functools

class Shipment(set):

    def __getitem__(self, id: int) -> Package:
        for package in self:
            if package.id == id:
                return package
        raise KeyError("This id does not exist")

    def __remove__(self, id: int) -> None:
        for package in self:
            if package.id == id:
                self.remove(package)
        raise KeyError("This id does not exist")

    def package_fitler(self, caracteristics_to_filter: dict): # Ici les listes ne seront jamais modifiées
        return functools.filter(lambda package: 
                                    functools.reduce(lambda key,value: 
                                        value in caracteristics_to_filter[key], 
                                        package.__dict__, True), 
                                self)
        
        """return functools.filter(lambda package:
                            package.id in id
                            and package.dimensions in dimensions
                            and package.status in status
                            and package.package_type in package_type,
                            self)"""
