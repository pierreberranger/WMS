from .package import Package
from typing import Union

class SetOfPackages(set):

    def __getitem__(self, id: int) -> Package:
        for package in self:
            if package.id == id:
                return package
        raise KeyError("This id does not exist")

    def remove(self, other: Union[int, Package]) -> None:
        if isinstance(other, Package):
            super().remove(other)
        elif isinstance(other, int):
            for package in self.copy():
                if package.id == other:
                    super().remove(package)
                    return None
            raise KeyError("This id does not exist")
        else:
            
            raise ValueError("The argument must be an int or a Package")