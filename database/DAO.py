from database.DB_connect import DBConnect
from model.arco import Arco
from model.circuito import Circuito
from model.posizione import Posizione


class DAO():
    @staticmethod
    def getAllCircuits():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT * 
                    from circuits"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(Circuito(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getPiaz(circuito, min, max):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select ra.`year` as y, r.driverId as id, r.`time` as t 
                    from circuits c, results r, races ra
                    where c.circuitId = %s
                    and ra.`year` > %s and ra.`year` < %s
                    and ra.circuitId = c.circuitId and ra.raceId = r.raceId 
                    """
        cursor.execute(query, (circuito.circuitId, min, max))

        diz = {}
        for row in cursor:
            if row['y'] in diz:
                diz[row['y']].append(Posizione(row['id'], row['t']))
            else:
                diz[row['y']] = [Posizione(row['id'], row['t'])]

        cursor.close()
        cnx.close()
        return diz

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct year FROM seasons s ORDER BY year"

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getArchi(mappaC, min, max):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        #query = """select ra1.circuitId as c1, ra2.circuitId as c2, count(*) as peso
                    #from races ra1, races ra2, results r1, results r2
                    #where ra1.circuitId < ra2.circuitId and ra1.`year` > %s and ra1.`year` < %s and ra2.`year` > %s and ra2.`year` < %s
                    #and ra1.raceId = r1.raceId and ra2.raceId = r2.raceId and r1.`time` is not null and r2.`time` is not null
                    #group by ra1.circuitId, ra2.circuitId"""
        query = """select c1.circuitId as c1, c2.circuitId as c2, (c1.cnt + c2.cnt) as peso
                    from(select ra.circuitId, count( *) as cnt
                    from races ra, results r
                    where ra.year > %s and ra.year < %s and ra.raceId = r.raceId and r.time is not null
                    group by ra.circuitId) c1, 
                    (select ra.circuitId, count(*) as cnt
                    from races ra, results r
                    where ra.year > %s and ra.year < %s and ra.raceId = r.raceId and r.time is not null
                    group by ra.circuitId
                    ) c2
                    where c1.circuitId < c2.circuitId"""

        cursor.execute(query, (min, max, min, max))

        for row in cursor:
            results.append(Arco(mappaC[row["c1"]], (mappaC[row["c2"]]), row["peso"]))

        cursor.close()
        conn.close()
        return results
