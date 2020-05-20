from .pyModbusTCP.client import ModbusClient
import logging

logger = logging.getLogger(__name__)

class Winch():

    # If a connection to the PLC can't be made, messages will be displayed
    DEBUG = 1
    OFFLINE = 1

    """Jog speed is between 1-10, so let's multiply by some factor 
       so we don't move super slow"""
    JOG_MULTIPLIER = 100
    TICKS_PER_METER = 1000 # TODO: Check this value

    # Home position
    POS_MIN = 0
    # Bottom of the ocean.  Need to test to find this value.
    POS_MAX = 9999

    def __init__(self):
        # First, see if we have a working connection to the PLC
        if not self.OFFLINE and not self.ModbusConnection.testConnection():
            logger.error("Unable to connect to winch PLC")

        """Let self.position have a default value of 0 in case we are OFFLINE"""
        self.position = 0
        self.pos_offset = 0

        self.position = self.get_position()


    def jog(self, speed):
        logger.info("Jogging at speed " + str(speed))
        self.go_to_position_raw(self.position + (speed*self.JOG_MULTIPLIER))

    def go_to_position_raw(self, position):
        desired_position = self.saturate_position(position)
        logger.info("Going to raw position " + str(desired_position))
        if not self.OFFLINE and position > 0:
            self.ModbusConnection.goToPos(desired_position)
        if self.OFFLINE:
            self.position = desired_position

    def saturate_position(self, position):
        if position > self.POS_MAX:
            return self.POS_MAX
        elif position < self.POS_MIN:
            return self.POS_MIN
        else:
            return position

    """Returns the position as indicated by the PLC, if offline, returns known position"""
    def get_position_PLC(self):
        position = self.position
        if not self.OFFLINE:
            position = int(self.ModbusConnection.readRegister(self.ModbusConnection.POSITION_REG))
        return position
    
    def set_zero_position(self):
        self.pos_offset = self.position

    def home(self):
        self.position = 0

    def get_position_raw(self):
        return self.get_position_PLC() - self.pos_offset
    
    def get_position(self):
        return self.get_position_raw() / self.TICKS_PER_METER
        


    class ModbusConnection():

        """Modbus FC offsets, see PLC code"""
        WINCH_ENABLE = 0
        SETPOINT_REG = 1
        POSITION_REG = 5

        winch_host = "192.168.1.1"
        client = ModbusClient(host=winch_host, auto_open=True, auto_close=True)

        @classmethod
        def testConnection(cls):
            # Attempts to read from 100 registers, starting at Modbus register 0
            if Winch.OFFLINE:
                return True
            return cls.client.read_holding_registers(0, 100) is not None

        @classmethod
        def writeRegister(cls, reg, data):
            if not cls.client.write_single_register(reg,data):
                logger.error("Unable to write to Winch PLC register: " + reg)
        
        @classmethod
        def readRegister(cls, reg):
            return cls.client.read_holding_registers(reg, 1)
        
        @classmethod
        def readRegisterRange(cls, reg, numRegs):
            return cls.client.read_holding_registers(reg, numRegs)

        @classmethod
        def goToPos(cls, pos):
            cls.writeRegister(cls.POSITION_REG, pos)
            cls.writeRegister(cls.WINCH_ENABLE, 1)

        @classmethod
        def homeWinch(cls):
            # TODO: There will probably be some extra PLC-side check here
            cls.goToPos(0)
