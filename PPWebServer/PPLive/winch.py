from pyModbusTCP.client import ModbusClient
import logging

logger = logging.getLogger(__name__)

class Winch():

    # Use a positive speed to jog up, negative speed to jog down
    def jog(self, speed):
        logger.info("Jogging at speed " + str(speed))

    def go_to_position(self, position):
        logger.info("Going to position " + str(position))

"""
def doTest():
	# TCP auto connect on modbus request, close after it
	c = ModbusClient(host="192.168.1.1", auto_open=True, auto_close=True)

	regs = c.read_holding_registers(0, 100)
	if regs:
		print(regs)
	else:
		print("read error")

def doWrite(goToPos):
	c = ModbusClient(host="192.168.1.1", auto_open=True, auto_close=True)

	if c.write_single_register(1,goToPos):
		print("write ok")
	else:
		print("write error")



if __name__=='__main__':
	c = ModbusClient(host="192.168.1.1", auto_open=True, auto_close=True)
	while(True):
		if c.write_single_register(0,0):
			print("Waiting for instruction")
		goto = int(input("Enter Go To Pos: "))
		doWrite(goto)
		if c.write_single_register(0,1):
			print("Going!")
		time.sleep(.1)
"""