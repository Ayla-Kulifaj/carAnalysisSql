# library used to connect to snowflake
import snowflake.connector

#creating a class to hold on to connection string in order to execute SQL
class SnowflakeConnector():

    # initialize variables #connection parameters

#1.calling class
#2. assigns all the variables to self
#3. it calls get snowflakecon to hold on to our connection into snowflake

    def __init__(self, user, password, account, warehouse, database, schema) -> None:
        self.user = user
        self.password = password
        self.account = account
        self.warehouse = warehouse
        self.database = database
        self.schema = schema
        self.conn = self.get_snowflake_conn(self.user, self.password, self.account, self.warehouse, self.database, self.schema)
    
    # function to get snowflake connection
    def get_snowflake_conn(self, user, password, account, warehouse, database, schema):
        conn = snowflake.connector.connect(
            user=user,
            password=password,
            account=account,
            warehouse=warehouse,
            database=database,
            schema=schema
    )
        return conn #returning the link to snowflake
    
    # Function to execute SQL
    def execute(self, sql):
        cur = self.conn.cursor()
        print(f"Executing SQL: {sql}")
        rez = cur.execute(sql)
        return rez
    #one function you need in Python to run SQL in Snowflake