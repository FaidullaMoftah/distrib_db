import pyodbc

#add customer
#add item
#update item
#buy
#view inventory(locataion)
#view customers
#delete customer
#delete item
class Query:
    def __init__(self, tp, q):
        self.q = q
        self.tp = tp
class Database:
    def __init__(self, address, street, region, num, tp,db,slaves=0, master = 0):
        self.state = 1 #0 available 1 busy
        self.queue = []
        self.address = address
        self.region = region
        self.street = street
        self.type = tp
        self.master = master
        self.slaves = slaves
        self.db = db
        self.cursor = None
        self.number = num
    def connect(self, USERNAME, PASSWORD, SERVER):
        Trust = "yes"
        connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};UID={USERNAME};PWD={PASSWORD};TrustServerCertificate={Trust};'
        try:
            conn = pyodbc.connect(connectionString)
        except:
            raise Exception("Connection failed!")
        self.cursor = conn.cursor()
        SET_XACT = f'SET XACT_ABORT ON'
        self.cursor.execute(SET_XACT)
    def view_items(self, slv = -1):
        whr = ""
        if(slv == -1):
            slv_site = self.slaves[slv].site
            slv_street = self.slaves[slv].street
            whr ="""
                WHERE
                SITE =  {} 
                AND 
                STREET =  {}
                """.format(slv_site, slv_street)
        q = """
        BEGIN DISTRIBUTED TRANSACTION;
        USE {}
        BEGIN TRY
            SELECT * FROM PRODUCTS
            {}
        END TRY
        BEGIN CATCH
            ROLLBACK TRANSACTION;
        END CATCH
        COMMIT TRANSACTION;
        """.format(self.db, whr)
        try:
            self.cursor.execute(q)
            self.cursor.commit()
        except:
            if(self.type == 'master'):
                print("master database down: fatal error")
            else:
                pass
                #self.master.apply()
                #self.master.view_items_master(self.num)
                #self.master.apply()
        return self.cursor.fetchall()
    def stock_items(self, item_id, count):
        q = """
        BEGIN DISTRIBUTED TRANSACTION;
        USE {}
        BEGIN TRY
            UPDATE PRODUCTS
            SET quantity = quantity + count
            WHERE  product_id = {};
        END TRY
        BEGIN CATCH
            ROLLBACK TRANSACTION;
        END CATCH
        COMMIT TRANSACTION;
        """.format(self.db, str(item_id))
        try:
            self.cursor.execute(q)
            self.cursor.commit()
        except:
            if(self.type == 'master'):
                print("master database down: fatal error")
            else:
                print("implement what happens when slave is down but master is up")
    def take_item(self, item_id, count):
        res1 = self.view_items()
        #somehow get count of item_id
    def apply(self):
        for i in self.queue:
            if(i.tp == "add_item"):
                pass
            if(i.tp == "stock_item"):
                pass
            if(i.tp == "take_item"):
                pass
            if(i.tp == "remove_item"):
                pass
            if(i.tp == "view"):
                self.view_items()


