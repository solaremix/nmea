from twisted.internet import reactor, protocol
import pynmea2
 
class NMEAServer(protocol.Protocol):
    def dataReceived(self, data):
        message = data.decode('utf-8').strip()
        if message.startswith('$GPGGA'):
            nmea_data = self.parse_nmea_gpgga(message)
            if nmea_data:
                response = f"Parsed NMEA Data: {nmea_data}"
            else:
                response = "Error: Invalid NMEA data"
        else:
            response = "Error: Unsupported NMEA sentence"
 
        self.transport.write(response.encode('utf-8'))
 
    def parse_nmea_gpgga(self, sentence):
        try:
            msg = pynmea2.parse(sentence)
            nmea_data = {
                'gps_time': msg.timestamp,
                'latitude': msg.latitude,
                'longitude': msg.longitude,
                'altitude': msg.altitude
            }
            return nmea_data
        except pynmea2.nmea.ParseError as e:
            print(f"Error parsing NMEA: {e}")
            return None
 
class NMEAFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return NMEAServer()
 
reactor.listenTCP(8000, NMEAFactory())
reactor.run()