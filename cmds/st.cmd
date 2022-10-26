# This should be a test or example startup script

require orkan

epicsEnvSet ("IOCNAME", "ioc01-orkan")

iocshLoad ("$(orkan_DIR)orkan.iocsh", "ASYN_PORT_NAME=PORT1,SERIAL_PORT=/dev/ttyUSB0,PREFIX=Cryo-Rec:LP:,DEV_NAME=Compr:")
