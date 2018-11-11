import sys
import ConfigAP
import Constantes as ctes

if __name__ == '__main__':
    on = ConfigAP.ConfigAP()
    if sys.argv[1] == "off":
        on.offAP()
    else:
        on.onAP()
    
    ctes.add_to_file(ctes.FILE_LOG, ctes.LOG)