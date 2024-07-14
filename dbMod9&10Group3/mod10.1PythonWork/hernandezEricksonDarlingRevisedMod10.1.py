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
            """CREATE TABLE customers(
               id int NOT NULL AUTO_INCREMENT,
               firstName varchar(255)NOT NULL,
               lastName varchar(255) NOT NULL,
               excursionId int NOT NULL,
               bookingDate date DEFAULT (CURRENT_DATE),
               PRIMARY KEY(id)
            );""",
            """CREATE TABLE vaccinations(
               id int NOT NULL AUTO_INCREMENT,
               vaccinationName varchar(255) NOT NULL,
               PRIMARY KEY(id)
            );""",
            """CREATE TABLE customer_vaccinations(
               customerId int NOT NULL,
               vaccinationId int NOT NULL,
               FOREIGN KEY(customerId) REFERENCES customers(id),
               FOREIGN KEY(vaccinationId) REFERENCES vaccinations(id)
            );""",
            """CREATE TABLE trip_type(
               id int NOT NULL AUTO_INCREMENT,
               tripName varchar(255),
               PRIMARY KEY(id)
            );""",
            """CREATE TABLE excursions(
               id int NOT NULL AUTO_INCREMENT,
               tripTypeId int NOT NULL,
               excursionDate date DEFAULT (CURRENT_DATE),
               visaRequired bool DEFAULT false,
               aireFarePerPerson decimal(30, 2),
               minimumNumCustomers int DEFAULT 1,
               PRIMARY KEY(id),
               FOREIGN KEY(tripTypeId) REFERENCES trip_type(id)
            );""",
            """CREATE TABLE customer_excursions(
               excursionId int NOT NULL,
               customerId int NOT NULL,
               FOREIGN KEY(excursionId) REFERENCES excursions(id),
               FOREIGN KEY(customerId) REFERENCES customers(id)
            );""",
            """CREATE TABLE required_trip_vaccinations(
               tripId int NOT NULL,
               vaccinationId int NOT NULL,
               FOREIGN KEY(tripId) REFERENCES trip_type(id),
               FOREIGN KEY(vaccinationId) REFERENCES vaccinations(id)
            );""",
            """CREATE TABLE equipment(
               id int NOT NULL AUTO_INCREMENT,
               equipmentName varchar(255) NOT NULL,
               equipmentRentalPrice decimal(30, 2) DEFAULT 0.99,
               equipmentSalePrice decimal(30, 2) DEFAULT 0.99,
               PRIMARY KEY(id)
            );""",
            """CREATE TABLE equipment_trip(
               equipmentId int NOT NULL,
               tripId int NOT NULL,
               FOREIGN KEY(equipmentId) REFERENCES equipment(id),
               FOREIGN KEY(tripId) REFERENCES trip_type(id)
            );""",
            """CREATE TABLE equipment_sales(
               id int NOT NULL AUTO_INCREMENT,
               equipmentId int NOT NULL,
               customerId int NOT NULL,
               wasRented bool DEFAULT true,
               unitsRequisitioned int DEFAULT 1,
               PRIMARY KEY(id),
               FOREIGN KEY(equipmentId) REFERENCES equipment(id),
               FOREIGN KEY(customerId) REFERENCES customers(id)
            );""",
            """CREATE TABLE equipment_units(
               id int NOT NULL AUTO_INCREMENT,
               equipmentID int NOT NULL,
               purchaseDate date DEFAULT (CURRENT_DATE),
               PRIMARY KEY(id),
               FOREIGN KEY(equipmentId) REFERENCES equipment(id)
            );"""
        ]

        #INSERT statements to populate each table.
        insert = [
            """INSERT customers(firstName, lastName, excursionId, bookingDate)
               VALUES
               ('Blythe', 'Timmerson', 1, '2020-06-15'),
               ('Jim', 'Ford', 2, '2019-08-28'),
               ('John', 'MacNell', 3, '2022-08-18'),
               ('Anita', 'Gallegos', 4, '2024-11-29'),
               ('Mei', 'Wong', 4, '2020-12-10');""",
            """INSERT vaccinations(vaccinationName)
               VALUES
               ('polio'),
               ('malaria'),
               ('ebola'),
               ('rabies'),
               ('smallpox');""",
            """INSERT customer_vaccinations(customerId, vaccinationId)
               VALUES
               (1, 1),
               (2, 2),
               (2, 3),
               (3, 2),
               (3, 3),
               (4, 2),
               (4, 5),
               (5, 1),
               (5, 4),
               (5, 5);""",
            """INSERT trip_type(tripName)
               VALUES
               ('Camping in Australian Outback'),
               ('Costa Rica Jungle Zipline'),
               ('Fjords of Norway'),
               ('Cave Spelunking in Iceland'),
               ('Skydiving in France');""",
            """INSERT excursions(tripTypeId, excursionDate, visaRequired, aireFarePerPerson, minimumNumCustomers)
               VALUES
               (1, '2024-06-27', true, 200.00, 10),
               (2, '2024-10-02', false, 355.00, 9),
               (3, '2024-08-29', true, 265.00, 8),
               (3, '2024-10-02', true, 270.00, 8),
               (4, '2024-11-20', false, 400.00, 7),
               (5, '2024-11-29', true, 290.00, 5);""",
            """INSERT customer_excursions(excursionId, customerId)
               VALUES
               (1, 1),
               (1, 3),
               (2, 2),
               (3, 1),
               (3, 3),
               (4, 1),
               (5, 1),
               (5, 5),
               (5, 4);""",
            """INSERT required_trip_vaccinations(tripId, vaccinationId)
               VALUES
               (1, 3),
               (1, 4),
               (2, 5),
               (4, 3),
               (4, 1),
               (4, 2),
               (5, 4);""",
            """INSERT equipment(equipmentName, equipmentRentalPrice, equipmentSalePrice)
               VALUES
               ('sleeping pads', 40.00, 199.99),
               ('tent', 80.00, 550.00),
               ('backpack', 25.00, 79.00),
               ('flashlight', 5.00, 20.00),
               ('sleeping bag', 15.00, 88.00),
               ('camp chair', 20.00, 155.00);""",
            """INSERT equipment_trip(equipmentId, tripId)
               VALUES
               (1, 5),
               (1, 5),
               (2, 3),
               (2, 1),
               (2, 2),
               (2, 4),
               (3, 4),
               (3, 1),
               (4, 4),
               (5, 4)""",
            """INSERT equipment_sales(equipmentId, wasRented, unitsRequisitioned, customerId)
               VALUES
               (1, true, 2, 1),
               (1, true, 1, 2),
               (2, false, 4, 3),
               (2, true, 2, 4),
               (3, true, 3, 4),
               (4, false, 4, 5),
               (5, false, 2, 5),
               (6, true, 1, 1),
               (6, true, 1, 1),
               (6, true, 2, 1);""",
            """INSERT equipment_units(equipmentId, purchaseDate)
               VALUES
               (1, '2020-10-08'),
               (1, '2020-10-08'),
               (1, '2020-10-08'),
               (2, '2021-11-06'),
               (2, '2021-11-06'),
               (3, '2022-04-10'),
               (3, '2022-04-10'),
               (3, '2022-04-10'),
               (3, '2023-05-09'),
               (3, '2023-05-09'),
               (4, '2023-07-12'),
               (5, '2021-03-01'),
               (5, '2021-03-01'),
               (6, '2022-07-04'),
               (6, '2022-07-04'),
               (6, '2021-11-11'),
               (6, '2024-01-07');"""
        ]

        #Executing both the CREATE & INSERT statements
        for table in tables:
            cursor.execute(table)
        
        for query in insert:
            cursor.execute(query)
        
        db.commit()

        #Display existing table names
        cursor.execute("SHOW TABLES;")

        print("\n--TABLE LIST IN OutlandAdventuresCase--")
        for tablename in cursor:
            print(tablename[0])
        
        #DISPLAY TABLE CONTENTS
        def display_message(tableName):
            print(f"\n--DISPLAYING {tableName}--\n")
        #Display customers table
        cursor.execute("""SELECT *
                       FROM customers""")
        
        display_message("customers")
        for customer in cursor:
            print(f"Customer ID: {customer[0]}\nFirst Name: {customer[1]}\nLast Name: {customer[2]}\nExcursion ID: {customer[3]}\nBooking Date: {customer[4]}\n")
        
        #Display Vaccinations table
        cursor.execute("""SELECT *
                       FROM vaccinations""")
        
        display_message("vaccinations")
        for vaccination in cursor:
            print(f"Vaccination ID: {vaccination[0]}\nVaccination Name: {vaccination[1]}\n")

        #Display Customer Vaccinations table
        cursor.execute("""SELECT *
                       FROM customer_vaccinations""")
        
        display_message("customer_vaccinations")
        for customer_vaccination in cursor:
            print(f"Customer ID: {customer_vaccination[0]}\nVaccination ID: {customer_vaccination[1]}\n")

        #Display Trip Type table
        cursor.execute("""SELECT *
                       FROM trip_type""")
        
        display_message("trip_type")
        for trip in cursor:
            print(f"\nTrip ID: {trip[0]}\nTrip Name: {trip[1]}\n")

        #Display Excursions table
        cursor.execute("""SELECT *
                       FROM excursions""")
        
        display_message("excursions")
        for excursion in cursor:
            print(f"\nExcursion ID: {excursion[0]}\nTrip Type ID: {excursion[1]}\nExcursion Date: {excursion[2]}\nVisa Required: {excursion[3]}\nAire Faire/Person: ${excursion[4]}\nMin Num of Customers: {excursion[5]}\n")
            
        #Display Customer Excursions table
        cursor.execute("""SELECT *
                       FROM customer_excursions""")
        
        display_message("customer_excursions")
        for customer_excursion in cursor:
            print(f"\nExcursion ID: {customer_excursion[0]}\nCustomer ID: {customer_excursion[1]}\n")

        #Display Required Trip Vaccinations table
        cursor.execute("""SELECT *
                       FROM required_trip_vaccinations""")
        
        display_message("required_trip_vaccinations")
        for required_trip_vaccination in cursor:
            print(f"\nTrip ID: {required_trip_vaccination[0]}\nVaccination ID: {required_trip_vaccination[1]}\n")
            
        #Display Equipment table
        cursor.execute("""SELECT *
                       FROM equipment""")
        
        display_message("equipment")
        for equip in cursor:
            print(f"\nEquipment ID: {equip[0]}\nEquipment Name: {equip[1]}\nEquipment Rental Price: ${equip[2]}\nEquipment Sale Price: ${equip[3]}\n")
    
        #Display Equpment Trip table
        cursor.execute("""SELECT *
                       FROM equipment_trip""")
        
        display_message("equipment_trip")
        for equip_trip in cursor:
            print(f"\nEquipment ID: {equip_trip[0]}\nTrip ID: {equip_trip[1]}\n")
            
        #Display Equipment Sales table
        cursor.execute("""SELECT *
                       FROM equipment_sales""")
        
        display_message("equipment_sales")
        for equip_sale in cursor:
            print(f"\nSale ID: {equip_sale[0]}\nEquipment ID: {equip_sale[1]}\nWas Rented: {equip_sale[2]}\nUnits Requisitioned: {equip_sale[3]}\nCustomer Id: {equip_sale[4]}\n")
            
        #Display Equipment Units table
        cursor.execute("""SELECT *
                       FROM equipment_units""")
        
        display_message("equipment_units")
        for unit in cursor:
            print(f"\nUnit ID: {unit[0]}\nEquipment ID: {unit[1]}\nDate Purchased: {unit[2]}\n")
    

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