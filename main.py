from backend import Package, Dimensions, SetOfPackages

def main():
    package_database = SetOfPackages() # À stocker dans un fichier externe

    package = Package(Dimensions(100, 55, 25), "delivered", "classic")
    package_database.add(package)

if __name__ == '__main__':
    main()