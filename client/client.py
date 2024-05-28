from twisted.internet import reactor, protocol
 
class NMEAClient(protocol.Protocol):
    def connectionMade(self):
        # Enviar una sentencia NMEA GPGGA al servidor
        nmea_sentence = "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47\r\n"
        self.transport.write(nmea_sentence.encode('utf-8'))
 
    def dataReceived(self, data):
        print("Server said:", data.decode('utf-8'))
        self.transport.loseConnection()
 
class NMEAFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return NMEAClient()
 
    def clientConnectionFailed(self, connector, reason):
        print("Connection failed.")
        reactor.stop()
 
    def clientConnectionLost(self, connector, reason):
        print("Connection lost.")
        reactor.stop()
 
reactor.connectTCP("localhost", 8000, NMEAFactory())
reactor.run()