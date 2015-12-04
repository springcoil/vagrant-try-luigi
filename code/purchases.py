import luigi
import luigi.postgres
import csv
import datetime
import psycopg2

class ExternalPurchases(luigi.ExternalTask):
    task_namespace = 'testing'

    def output(self):
        return luigi.LocalTarget("/home/vagrant/data/purchases.csv")

class PurchasesTotal(luigi.Task):
    task_namespace = 'testing'

    def output(self):
        return luigi.LocalTarget("/home/vagrant/data/total.txt")

    def run(self):
        total = 0
        with self.input().open("r") as fin:
            fin.next() #skip the header
            total = sum(int(r[2])*int(r[3]) for r in csv.reader(fin))

        with self.output().open("w") as out_file:
            out_file.write(str(total))

    def requires(self):
       return ExternalPurchases()

class PurchasesToDatabase(luigi.postgres.CopyToTable):
    task_namespace = 'testing'

    host = "localhost"
    database = "vagrantdb"
    user = "vagrant"
    password = "vagrant"
    table = "purchases"

    columns = [("name", "TEXT"),
               ("date", "TIMESTAMP"), #DATE would truncate at the day resolution
               ("price", "INT"),
               ("amount", "INT")]

    def rows(self):
        with self.input().open('r') as fobj:
            fobj.next() #skip the header

            for line in fobj:
                split = line.strip('\n').split(', ')

                #unix timestamp to date
                date = datetime.datetime.fromtimestamp(
                    int(split[1])
                ).strftime('%Y-%m-%d %H:%M:%S')

                yield (split[0], date, split[2], split[3])

    def requires(self):
       return ExternalPurchases()

class QueryPostgres(luigi.Task):
    task_namespace = 'testing'

    def output(self):
        return luigi.LocalTarget("/home/vagrant/data/same_purchases.csv")

    def requires(self):
       return PurchasesToDatabase()

    def run(self):
        # these are here for convenience
        host = "localhost"
        database = "vagrantdb"
        user = "vagrant"
        password = "vagrant"

        conn = psycopg2.connect(
            dbname=database,
            user=user,
            host=host,
            password=password)
        cur = conn.cursor()
        cur.execute("""SELECT
          name,
          date,
          price,
          amount
          FROM purchases
        """)
        rows = cur.fetchall()

        with self.output().open("w") as out_file:
            out_file.write("name, date, price, amount") #write a header by hand
            for row in rows:
                out_file.write("\n")
                # without the :%s, the date will be output in year-month-day format
                out_file.write("{}, {:%s}, {}, {}".format(*row)) #each element of row by itself, unpacked by the star

if __name__ == '__main__':
    # if you want to execute one task per default without further arguments
    #luigi.run(['testing.PurchasesToDatabase'])
    luigi.run()

