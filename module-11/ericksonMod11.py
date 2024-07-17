import mysql.connector
from mysql.connector import errorcode

def display_remaining_vaccinatons_needed_for_each_customer(my_cursor):
    def get_query_result(query):
        my_cursor.execute(query)
        return my_cursor.fetchall()

    # Vaccinatons Needed Report -- data needed (trip vaccionaion requirements, customers on excursions of those trip types, vaccinations those customers have)
    # Determine discrepancies/mismatches of vaccinatons required vs. vaccinatons obtained for each customer
    
    # This query gets all the vaccinatons required for a tripType
    vaccs_per_trip_query = """
    select trip_type.tripName, vaccinations.vaccinationName
    from trip_type
    left join required_trip_vaccinations on trip_type.id = required_trip_vaccinations.tripId
    left join vaccinations on required_trip_vaccinations.vaccinationId = vaccinations.id"""

    # This query gets all the trip types a customer is signed up for
    trip_type_per_customer = """
    select customers.lastName, trip_type.tripName
    from customers
    left join excursions on customers.excursionId = excursions.id
    left join trip_type on excursions.tripTypeId = trip_type.id;"""

    # This query gets all the vaccinations a customer has
    vaccs_per_customer_query = """
    select customers.lastName, vaccinations.vaccinationName
    from customers
    left join customer_vaccinations on customers.id = customer_vaccinations.customerId
    left join vaccinations on customer_vaccinations.vaccinationId = vaccinations.id;"""

    vaccs_per_trip_data = get_query_result(vaccs_per_trip_query)
    trips_per_customer_data = get_query_result(trip_type_per_customer)
    vaccs_per_customer_data = get_query_result(vaccs_per_customer_query)

    def group_data_into_dict(query_data):
        group_dict = {}
        for row in query_data:
            dict_keys = list(group_dict.keys())
            if row[0] not in dict_keys:
                group_dict[row[0]] = []

        for row in query_data:
            group_dict[row[0]].append(row[1])

        return group_dict

    def group_trip_vaccs(trip_vacc_data):
        trip_vacc_dict = {}
        for row in trip_vacc_data:
            dict_keys = list(trip_vacc_dict.keys())
            if row[0] not in dict_keys:
                trip_vacc_dict[row[0]] = []

        for row in trip_vacc_data:
            trip_vacc_dict[row[0]].append(row[1])

        return trip_vacc_dict
    
    def group_customer_trips(customer_trip_data):
        customer_trip_dict = {}
        for row in customer_trip_data:
            dict_keys = list(trip_vacc_dict.keys())
            if row[0] not in dict_keys:
                customer_trip_dict[row[0]] = []

        for row in customer_trip_data:
            customer_trip_dict[row[0]].append(row[1])
        return customer_trip_dict
    
    def group_customer_vaccs(customer_vaccs_data):
        customer_vacc_dict = {}
        for row in customer_vaccs_data:
            dict_keys = list(customer_vacc_dict.keys())
            if row[0] not in dict_keys:
                customer_vacc_dict[row[0]] = []

        for row in customer_vaccs_data:
            customer_vacc_dict[row[0]].append(row[1])
        return customer_vacc_dict

    trip_vacc_dict = group_trip_vaccs(vaccs_per_trip_data)
    customer_trip_dict = group_customer_trips(trips_per_customer_data)
    customer_vacc_dict = group_customer_vaccs(vaccs_per_customer_data)

    def flatten_extend(matrix):
        flat_list = []
        for row in matrix:
            flat_list.extend(row)
        return flat_list

    def generate_required_customer_vacc_dict(trip_vacc_dict, customer_trip_dict):
        required_customer_vacc_dict = {}
        for customer in list(customer_trip_dict.keys()):
            required_customer_vacc_dict[customer] = []

        for customer in customer_trip_dict:
            for trip in trip_vacc_dict:
                if trip in customer_trip_dict[customer]:
                    required_customer_vacc_dict[customer].append(trip_vacc_dict[trip])

        # Each entry in needed_customer_vacc_dict is a list of lists, we want to flatten that into one list
        for customer in required_customer_vacc_dict:
            required_customer_vacc_dict[customer] = flatten_extend(required_customer_vacc_dict[customer])

        return required_customer_vacc_dict
    
    required_customer_vacc_dict = generate_required_customer_vacc_dict(trip_vacc_dict, customer_trip_dict)

    def generate_needed_customer_vacc_dict(customer_vacc_dict, required_customer_vacc_dict):
        needed_customer_vacc_dict = {}
        customers = list(customer_vacc_dict.keys())
        for customer in customers:
            needed_customer_vacc_dict[customer] = []

        for customer in customers:
            for vacc in required_customer_vacc_dict[customer]:
                if vacc not in customer_vacc_dict[customer] and vacc != None:
                    needed_customer_vacc_dict[customer].append(vacc)

        customers_to_pop = []
        for customer in needed_customer_vacc_dict:
            if len(needed_customer_vacc_dict[customer]) == 0:
                customers_to_pop.append(customer)
        
        for customer in customers_to_pop:
            needed_customer_vacc_dict.pop(customer)

        return needed_customer_vacc_dict
    needed_customer_vacc_dict = generate_needed_customer_vacc_dict(customer_vacc_dict, required_customer_vacc_dict)

    def display_needed_customer_vaccs(needed_customer_vacc_dict):
        print("---DISPLAYING REMAINING NEEDED VACCINATONS TO FULFILL TRIP REQUIREMENTS---\n")
        for customer in needed_customer_vacc_dict:
            print(f"--Customer with last name of {customer} still needs the following vaccinatons:")
            for vacc in needed_customer_vacc_dict[customer]:
                print(f"the {vacc.upper()} vaccinaton\n")


    display_needed_customer_vaccs(needed_customer_vacc_dict)
# ---------
# Note that in the data, there is no customer who is going on two excursions
# Note three out of five of the customers in the data are going to Fjords of Norway which doesn't require any vaccinations. This does not make for an interesting report
#----------

    

def display_reports(config):

    try: 
        db = mysql.connector.connect(**config)
        print("\n Database user {} connected to MySql on host {} with database {}".format(config["user"], config["host"], config["database"]))
        my_cursor = db.cursor()

        display_remaining_vaccinatons_needed_for_each_customer(my_cursor)

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("   The supplied username or password are invalid")
        
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("   The specified database does not exist")

        else:
            print(err)
        
    finally:
        db.close()


def main():
    config = {
    "user": "root",
    "password": input("Please enter your root database password: "), #YOUR MYSQL PASSWORD HERE!
    "host": "127.0.0.1",
    "database": "OutlandAdventuresCase",
    "raise_on_warnings": True
    }

    display_reports(config)

    input("\nPress ENTER to exit...")

if __name__ == '__main__':
    main()