# This should be a test or example startup script

require orkan
require recsync
require iocstats


epicsEnvSet ("IOCNAME", "ioc23-orkan")

# Uncommet the line below for the serial port connection (ModBus RTU)
#iocshLoad ("$(orkan_DIR)orkan.iocsh", "ASYN_PORT_NAME=PORT1,SERIAL_PORT=/dev/ttyUSB0,PREFIX=Cryo-Rec:LP:,DEV_NAME=C4:")

# Connect using Modbus TCP
iocshLoad ("$(orkan_DIR)orkan-tcp.iocsh", "ASYN_PORT_NAME=PORT1,IP_ADDR=192.168.10.39,PREFIX=Cryo-Rec:LP:,DEV_NAME=C4:,TOP=/opt/epics/autosave")

var(reccastTimeout, 5.0)
var(reccastMaxHoldoff, 5.0)

# iocStats database
dbLoadRecords("$(iocstats_DB)/iocAdminSoft-freia.db","IOC=$(IOCNAME)")

# Start recsync client
iocshLoad("$(recsync_DIR)/recsync.iocsh", "IOCNAME=$(IOCNAME)")
