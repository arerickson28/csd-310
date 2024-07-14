import mysql.connector
from mysql.connector import errorcode

def completion_time(cursor):
        cursor.execute("SELECT NOW()")
        datetime = cursor.fetchone()
        print("\nThis report was completed on: {}".format(datetime[0]))

def create_database(config):
    try:
        db = mysql.connector.connect(**config)
        
        print("\nDatabase user {} connected to MySQL on host {}".format(config["user"], config["host"]))

        cursor = db.cursor()

        cursor.execute("SHOW DATABASES LIKE 'OutlandAdventuresCase';")
        database_exists = cursor.fetchone()

        if database_exists:
            cursor.execute("DROP DATABASE OutlandAdventuresCase;") #Deletes database if it exists
        
        cursor.execute("CREATE DATABASE OutlandAdventuresCase;") #Creates new database named OutlandAdventuresCase
        
        #Displays existing databases
        cursor.execute("SHOW DATABASES;")

        print("\n--DATABASE LIST--")
        for dbname in cursor:
            print(dbname[0])


    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Username or password are invalid")
        else:
            print(err)

    finally:
        cursor.close()
        db.close()

def create_tables(config):
    config["database"] = "OutlandAdventuresCase" #Adds OutlandAdventuresCase database to the connector config

    try:
        db = mysql.connector.connect(**config)
        
        print("\nDatabase user {} connected to MySQL on host {} with database {}".format(config["user"], config["host"], config["database"]))

        cursor = db.cursor()

        #CREATE TABLE statements
        tables = [
            """CREATE TABLE EMPLOYEES(
               EmpID int NOT NULL AUTO_INCREMENT,
               FirstName varchar(255) NOT NULL,
               LastName varchar(255) NOT NULL,
               TitleJob varchar(255) NOT NULL,
               PRIMARY KEY(EmpID));""",
            """CREATE TABLE CUSTOMERS(
               CustomerID int NOT NULL AUTO_INCREMENT,
               FirstName varchar(255)NOT NULL,
               LastName varchar(255) NOT NULL,
               Inoculation bool DEFAULT false,
               Visa bool DEFAULT false,
               PRIMARY KEY(CustomerID));""",
            """CREATE TABLE InventorySupplies(
               ProductID int NOT NULL AUTO_INCREMENT,
               Description varchar(255) NOT NULL,
               PriceUnit decimal(30, 2) DEFAULT 0.99,
               PriceRental decimal(30, 2) DEFAULT 0.99,
               TotalUnit int DEFAULT 1,
               In_Date date DEFAULT (CURRENT_DATE),
               PRIMARY KEY(ProductID));""",
            """CREATE TABLE EquipmentSalesRent(
               TransactionID int NOT NULL AUTO_INCREMENT,
               Sales_Rent varchar(255) NOT NULL DEFAULT 'rental',
               ProductID int NOT NULL,
               TotalUnit int,
               Cost decimal(30, 2) DEFAULT 0.00,
               EmpID int,
               CustomerID int,
               Transaction_Date date DEFAULT (CURRENT_DATE),
               CHECK(Sales_Rent IN('rental', 'sale')),
               PRIMARY KEY(TransactionID, ProductID, EmpID, CustomerID),
               FOREIGN KEY(ProductID) REFERENCES InventorySupplies(ProductID),
               FOREIGN KEY(EmpID) REFERENCES Employees(EmpID),
               FOREIGN KEY(CustomerID) REFERENCES Customers(CustomerID));""",
            """CREATE TABLE Locations(
               LocationID int NOT NULL AUTO_INCREMENT,
               Locationdescription varchar(255) NOT NULL,
               PRIMARY KEY(LocationID));""",
            """CREATE TABLE TripsPlaces(
               TripplaceID int NOT NULL AUTO_INCREMENT,
               CustomerID int NOT NULL,
               EmpID int NOT NULL,
               LocationID int NOT NULL,
               Cost double,
               TripDate date DEFAULT (CURRENT_DATE),
               PRIMARY KEY(TripplaceID),
               FOREIGN KEY(CustomerID) REFERENCES Customers(CustomerID),
               FOREIGN KEY(EmpID) REFERENCES Employees(EmpID),
               FOREIGN KEY(LocationID) REFERENCES Locations(LocationID));""",
            """CREATE TRIGGER calculate_price
               BEFORE INSERT ON EquipmentSalesRent
               FOR EACH ROW
               BEGIN
                 IF NEW.Sales_Rent = 'sale' THEN
                    SET NEW.Cost = NEW.totalunit * (SELECT PriceUnit FROM InventorySupplies WHERE ProductID = NEW.ProductID);
                 ELSE
                    SET NEW.Cost = NEW.totalunit * (SELECT PriceRental FROM InventorySupplies WHERE ProductID = NEW.ProductID);
                 END IF;
               END;"""
        ]

        #INSERT statements to populate each table.
        insert = [
            """INSERT Employees(FirstName, LastName, TitleJob)
               VALUES
               ('Blythe', 'Timmerson', 'Admin'),
               ('Jim', 'Ford', 'Admin'),
               ('John','MacNell', 'Guide'),
               ('D.B', 'Marland', 'Guide'),
               ('Anita', 'Gallegos','Marketing'),
               ('Dimitrios', 'Stravopolous', 'Supply'),
               ('Mei', 'Wong', 'Developer');""",
            """INSERT Customers(FirstName, LastName, Inoculation, Visa)
               VALUES
               ('John', 'Ruiz', true, true),
               ('Mario', 'Fonseca', true, true),
               ('Sara', 'Di', true, true),
               ('Walter', 'Hernandez', true, true),
               ('Al', 'Smit', true, true),
               ('Ernesto', 'Vega', true, true);""",
            """INSERT INTO InventorySupplies (ProductID, Description, PriceUnit, PriceRental, TotalUnit, In_Date)
               VALUES
               (1, 'Sleeping pads', 199.99, 40.00, 8, '2020-06-15'),
               (2, 'Camping pillow', 95.99, 35.00, 10, '2018-05-23'),
               (3, 'Tents', 550.00, 80.00, 5, '2019-08-28'),
               (4, 'Backpacks', 109.95, 39.00, 8, '2024-09-21'),
               (5, 'Flashlights', 38.99, 10.00, 12, '2016-12-12'),
               (6, 'Sleeping Bags', 145.98, 100.00, 17, '2022-08-20'),
               (7, 'Camp chairs', 39.99, 10.00, 50, '2019-10-08');""",
            """INSERT INTO EquipmentSalesRent (Sales_rent, ProductID, totalunit, EmpID, CustomerID, Transaction_Date)
               VALUES
               ('sale', 1, 3, 1, 1, '2024-05-11'),
               ('sale', 2, 2, 2, 2, '2023-07-24'),
               ('rental', 3, 1, 3, 3, '2021-06-03'),
               ('sale', 1, 4, 4, 4, '2023-04-28'),
               ('rental', 2, 2, 2, 5, '2023-09-27'),
               ('sale', 3, 3, 3, 6, '2022-05-18'),
               ('rental', 1, 3, 2, 4, '2021-07-15'),
               ('sale', 3, 1, 1, 3, '2019-05-20'),
               ('sale', 2, 2, 4, 2, '2020-12-10'),
               ('rental', 5, 4, 3, 5, '2021-03-05'),
               ('sale', 4, 1, 5, 1, '2018-09-28'),
               ('sale', 6, 2, 2, 4, '2022-08-18'),
               ('rental', 5, 2, 1, 5, '2018-07-30'),
               ('rental', 3, 1, 2, 1, '2021-09-12'),
               ('sale', 6, 1, 3, 4, '2022-04-18'),
               ('sale', 2, 4, 3, 2, '2023-04-05');""",
            """INSERT Locations(LocationID, LocationDescription)
               VALUES
               (1, 'Africa'),
               (2, 'Asia'),
               (3, 'Italy'),
               (4, 'Spain'),
               (5, 'Nepal'),
               (6, 'Southern Europe');""",
            """INSERT TripsPlaces(TripplaceID, CustomerID, EmpID, LocationID, Cost, TripDate)
               VALUES
               (1, 3, 3, 6, 1623.93, '2024-02-10'),
               (2, 5, 4, 1, 2027.34, '2024-11-29'),
               (3, 1, 4, 3, 1051.24, '2024-06-27'),
               (4, 2, 3, 3, 2424.86, '2024-11-20'),
               (5, 6, 3, 5, 1709.65, '2024-08-29'),
               (6, 4, 4, 2, 1815.34, '2024-10-02');"""
        ]

        #Executing both the CREATE & INSERT statements
        for table in tables:
            cursor.execute(table)
        
        for query in insert:
            cursor.execute(query)
        
        db.commit()

        #Display existing tables
        cursor.execute("SHOW TABLES;")

        print("\n--TABLE LIST IN OutlandAdventuresCase--")
        for tablename in cursor:
            print(tablename[0])
        
        #Display Employees table
        cursor.execute("""SELECT *
                       FROM EMPLOYEES""")
        
        print("\n--DISPLAYING EMPLOYEES--")
        for employee in cursor:
            print("\nEmployee ID: {} | First Name: {} | Last Name: {} | Job Title: {}".format(employee[0], employee[1], employee[2], employee[3]))
        
        #Display Customers table
        cursor.execute("""SELECT *
                       FROM Customers""")
        
        print("\n--DISPLAYING Customer--")
        for customer in cursor:
            print("\nCustomer ID: {} | First Name: {} | Last Name: {} | Inoculated: {} | Travel Visa: {}".format(customer[0], customer[1], customer[2], customer[3], customer[4]))

        #Display InventorySupplies table
        cursor.execute("""SELECT *
                       FROM InventorySupplies""")
        
        print("\n--DISPLAYING InventorySupplies--")
        for InventorySupplies in cursor:
            print("\nItem ID: {} | Description: {} | Unit Price: {} | Rental Price: {} | Quantity: {} | Intake Date: {}".format(InventorySupplies[0], InventorySupplies[1], InventorySupplies[2], InventorySupplies[3], InventorySupplies[4], InventorySupplies[5]))

        #Display EquipmentSalesRent table
        cursor.execute("""SELECT *
                       FROM EquipmentSalesRent""")
        
        print("\n--DISPLAYING EquipmentSalesRent--")
        for salerent in cursor:
            print("\nTransaction ID: {} | Category: {} | Item ID: {} | Quantity: {} | Price: {} | Employee ID: {} | Customer ID: {} | Transaction Date: {}".format(salerent[0], salerent[1], salerent[2], salerent[3], salerent[4], salerent[5], salerent[6], salerent[7]))

        #Display Locations table
        cursor.execute("""SELECT *
                       FROM Locations""")
        
        print("\n--DISPLAYING Locations--")
        for location in cursor:
            print("\nLocation ID: {} | Location: {}".format(location[0], location[1]))

        #Display TripsPlaces table
        cursor.execute("""SELECT *
                       FROM TripsPlaces""")
        
        print("\n--DISPLAYING TripsPlaces--")
        for TripsPlaces in cursor:
            print("\nTrip ID: {} | Customer ID: {} | Employee ID: {} | Location ID: {} | Price: {} | Trip Date: {}".format(TripsPlaces[0], TripsPlaces[1], TripsPlaces[2], TripsPlaces[3], TripsPlaces[4], TripsPlaces[5]))

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("The supplied username or password are invalid")

        elif err.errno == errorcode.ER_BAD_DB_ERROR:
          print("The specified database does not exist")

        else:
            print(err)

    finally:
        cursor.close()
        db.close()


def main():
    config = {
    "user": "root",
    "password": input("Please enter your root database password: "), #YOUR MYSQL PASSWORD HERE!
    "host": "127.0.0.1",
    "raise_on_warnings": True
    }

    create_database(config)

    input("\nPress ENTER to continue...")

    create_tables(config)





    input("\nPress ENTER to exit...")

if __name__ == '__main__':
    main()