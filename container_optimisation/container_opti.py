from turtle import width
import data.pickle_data as database
from models import Dimensions, Package
import typing

def define_positions(args: dict) -> list[tuple]:
    for priority in args.keys():
        for package_id in args[priority]:
            

    return [(package_id, priority, x, y, is_turned)]

def package_extrema(package: Package, is_turned) -> tuple:
    if is_turned:
        return (package.dimensions.length, package.dimensions.width)
    return (package.dimensions.width, package.dimensions.length)