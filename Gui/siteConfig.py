
import logging

# Customize the logging configuration
logging.basicConfig(
   level=logging.INFO,
   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
   filename='my_project.log',  # Specify a log file
   filemode='w'  # 'w' for write, 'a' for append
)

logger = logging.getLogger(__name__)

######################################################################
# To be edited by expert as default setting for Hardware configuration
######################################################################

# Set gpib debug mode to True if you want to see SCPI commands sent to HV and LV devices:
GPIB_DebugMode = False


##  The following block sets defaults that are to be used in the simplified (non-expert) mode.  ##
##  This mode is currently under development, so these values don't currently do anything       ##

# default FC7 boardName
defaultFC7 = "fc7.board.1"
# default IP address of IP address
defaultFC7IP = '192.168.1.80'
# default FMC board number
defaultFMC = '0'
# default mode for LV powering (Direct,SLDO,etc)
defaultPowerMode = "SLDO"
#default DBServerIP
defaultDBServerIP = '127.0.0.1'
#default DBName
defaultDBName = 'SampleDB'
##################################


## The following block assigns ports to devices when the "connect all devices" button is clicked ##

# default USB port for HV power supply
defaultUSBPortHV = ["ASRL/dev/ttyUSBHV::INSTR"]
# default model for HV power supply
defaultHVModel = ["Keithley 2410 (RS232)"]
# default USB port for LV power supply
defaultUSBPortLV = ["ASRL/dev/ttyUSBLV::INSTR"]
# default model for LV power supply
defaultLVModel = ["KeySight E3633 (RS232)"]
#default BaudRate for Arduino sensor
defaultSensorBaudRate = 9600
#################################

# Icicle variables
icicle_instrument_setup = { "lv":"KeysightE3633A",
                            "lv_resource" : "ASRL/dev/ttyUSBLV::INSTR",
                            "default_lv_channel" : 1,
                            "default_lv_voltage" : 1.8,
                            "default_lv_current" : 3,
                            "hv": "Keithley2410",
                            "hv_resource": "ASRL/dev/ttyUSBHV::INSTR",
                            "default_hv_voltage": -80,
                            "default_hv_compliance_current": 5e-6,
                            "default_hv_delay": 2,
                            "default_hv_step_size": 10,
                            "relay_board": "RelayBoard",
                            "relay_board_resource": "ASRL/dev/ttyUSB4::INSTR",
                            "multimeter": "HP34401A",
                            "multimeter_resource": "ASRL/dev/ttyUSB1::INSTR"}
## Update this dictionary for the IP addreses of your FC7 devices ##

FC7List =  {
	'fc7.board.1'			 :  '192.168.1.80',
	'fc7.board.2'			 :  '192.168.1.81',
	}

##############################################


## Specify whether of not you want to monitor chip temperature during the tests ##
## Set this to "1" if you want the monitoring enabled.  Set it to "0" if you want it disabled. ##
Monitor_RD53A = "1"
Monitor_CROC = "1"

#setting default HV current compliance in mA
defaultHVCurrentCompliance = 0.00001

#setting HV bias voltage in V
defaultHVsetting = -60

## Configuring the current settings for each module type.  These values are in Amps. 
ModuleCurrentMap = {
	"SingleSCC" : 0.6,
	"TFPX Quad" : 6.5,
	"TEPX Quad" : 6,
	"TBPX Quad" : 6.5,
	"TFPX CROC 1x2"  : 4.5,
	"TFPX CROC Quad" : 6.5,
	"CROC SCC"  : 2.0,
}

## Configuring the voltage limit for each module type when operating in SLDO mode.  These values are in Volts.
ModuleVoltageMapSLDO = {
	"SingleSCC" : 1.8,
	"TFPX Quad" : 2.98,
	"TEPX Quad" : 2.0,
	"TBPX Quad" : 2.98,
	"TFPX CROC 1x2"  : 2.3,
	"TFPX CROC Quad" : 2.98,
	"CROC SCC"  : 1.8,
}

###### Should not be using direct voltage, so this block can probably be removed #####
##  Configuring the voltage settings for each module type.  These values are in Volts.
ModuleVoltageMap = {
	"SingleSCC" : 1.3,
	"CROC SCC"  : 1.6,
}
#####################################################


######  can probably remove this block  #############
#setting the sequence of threshold tuning targets:
#defaultTargetThr = ['2000','1500','1200','1000','800']

##### The following settings are for SLDO scans developed for Purdue.#####
##### Do not modify these settings unless you know what you are doing.####
#default settings for SLDO scan.
defaultSLDOscanVoltage = 0.0
defaultSLDOscanMaxCurrent = 0.0
#####################################################


### Setting for Peltier Controller
usePeltier = False
defaultPeltierPort = '/dev/ttyUSBPeltier'
defaultPeltierBaud = 9600
defaultPeltierSetTemp = 20
defaultPeltierWarningTemp = 40
