from twisted.internet import reactor, protocol
import pynmea2
import psycopg
from datetime import datetime
import pytz  

class NMEAServer(protocol.Protocol):
    def __init__(self):
        self.connection = psycopg.connect(
            "dbname=nmea user=postgres password=Starbucks2020 host=localhost"
        )
        self.cursor = self.connection.cursor()

    def dataReceived(self, data):
        message = data.decode('utf-8').strip()
        if message.startswith('$GPGGA'):
            nmea_data = self.parse_nmea_gpgga(message)
            if nmea_data:
                response = f"Parsed NMEA Data: {nmea_data}"
                self.save_nmea_data(nmea_data)
            else:
                response = "Error: Invalid NMEA data"
        else:
            response = "Error: Unsupported NMEA sentence"

        self.transport.write(response.encode('utf-8'))

    def parse_nmea_gpgga(self, sentence):
        try:
            msg = pynmea2.parse(sentence)
            # Convertir el timestamp al formato correcto
            if msg.timestamp:
                gps_time = datetime.combine(datetime.today(), msg.timestamp)
                gps_time = gps_time.replace(tzinfo=pytz.utc)
            else:
                gps_time = None
            nmea_data = {
                'gps_time': gps_time,
                'latitude': float(msg.latitude) if msg.latitude else None,
                'longitude': float(msg.longitude) if msg.longitude else None,
                'altitude': float(msg.altitude) if msg.altitude else None
            }
            return nmea_data
        except pynmea2.nmea.ParseError as e:
            print(f"Error parsing NMEA: {e}")
            return None

    def save_nmea_data(self, data):
        query = """
        INSERT INTO nmea_data (gps_time, latitude, longitude, altitude)
        VALUES (%s, %s, %s, %s)
        """
        values = (
            data['gps_time'],
            data['latitude'],
            data['longitude'],
            data['altitude']
        )
        self.cursor.execute(query, values)
        self.connection.commit()

    def connectionLost(self, reason):
        self.cursor.close()
        self.connection.close()

class NMEAFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return NMEAServer()

reactor.listenTCP(8000, NMEAFactory())
reactor.run()
