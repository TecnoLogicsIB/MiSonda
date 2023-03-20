import time
import logging
from w1thermsensor import W1ThermSensor
import ConfigHelper

#Creacion del loger para los datos cientificos
logger = logging.getLogger('server_logger')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('/data/hab_sonda/logs/dallasdata.log')
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s|%(message)s|', datefmt='%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)
logger.addHandler(fh)

#Creacion del logger para los logs de aplicacion
loggerLog = logging.getLogger('server_logger1')
loggerLog.setLevel(logging.INFO)
inf = logging.FileHandler('/data/hab_sonda/logs/dallasService.log')
inf.setLevel(logging.INFO)
formatterInformer = logging.Formatter('[%(asctime)s][%(levelname)s][%(message)s]', datefmt='%Y-%m-%d %H:%M:%S')
inf.setFormatter(formatterInformer)
loggerLog.addHandler(inf)

sensor = W1ThermSensor()
dallasTemp = []

act = ConfigHelper.isDallasActivo()
tiempoMuestreoDallas = ConfigHelper.getTiempoMuestreoDallas()

loggerLog.info("[dallasService] tiempoMuestreoDallas: " + str(tiempoMuestreoDallas))

if act == 1:

    while True:

        try:
            for sensor in W1ThermSensor.get_available_sensors():
                dallasTemp.append(round(sensor.get_temperature(),2))  # lectura arrodonida amb 2 decimals
            logger.info (str(dallasTemp[0]) + '|' + str(dallasTemp[1]))
            dallasTemp.clear()
            time.sleep(tiempoMuestreoDallas)

        except Exception as e:
            loggerLog.error("[dallasService] Exception: " + str(e))
            loggerLog.error("[dallasService] Se ha producido un error, se sigue iterando...")
            time.sleep(5)
else:
    loggerLog.warn("[dallasService] El sensor no ha sido activado!")
