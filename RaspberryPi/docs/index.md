# Machine Program Documentation

## Overview
This is the general software documentation for the Ecozone. This document was created to help all developers work together. This document will contain all relevant details for the various API's that make up the software for this machine. When developing routines and programs for the machine please refer to this documentation to avoid any confusion.

## Index
- [main.py](https://github.com/Dormtech/Ecotech/blob/master/RaspberryPi/docs/index.md#mainpy)
- [mainGUI.py](https://github.com/Dormtech/Ecotech/blob/master/RaspberryPi/docs/index.md#mainGUIpy)
- [logg.py](https://github.com/Dormtech/Ecotech/blob/master/RaspberryPi/docs/index.md#loggpy)
- [control.py](https://github.com/Dormtech/Ecotech/blob/master/RaspberryPi/docs/index.md#controlpy)
- [networking.py](https://github.com/Dormtech/Ecotech/blob/master/RaspberryPi/docs/index.md#networkingpy)
- [atmSequence.py](https://github.com/Dormtech/Ecotech/blob/master/RaspberryPi/docs/index.md#atmSequencepy)
- [cameraSequence.py](https://github.com/Dormtech/Ecotech/blob/master/RaspberryPi/docs/index.md#cameraSequencepy)
- [pumpSequence.py](https://github.com/Dormtech/Ecotech/blob/master/RaspberryPi/docs/index.md#pumpSequencepy)
- [DCT.py](https://github.com/Dormtech/Ecotech/blob/master/RaspberryPi/docs/index.md#DCTpy)

## main.py
### Overview
This is the main entry point for all software on the machine. This wrapper program connects all machine wide functions including the UI.

## mainGUI.py
### Overview
This program contains the UI for the machine. Inside this program you will find logic related to machine UI and UX. This program is built using the python framework kivy in combination with our numerous API's.

## logg.py
### Overview
This is the logg API for the machine. This API is in charge of handeling all machine logging of statistics.

## control.py
### Overview
This is the control API for the machine. This API is in charge of handeling all low level machine actions.

## networking.py
### Overview
This is the networking API for the machine. This API is in charge of handeling all network interactions for the machine.

## atmSequence.py
### Overview
This is the atmSequence API for the machine. This API is in charge of handeling all atmosphere related sequences the machine might need to perform.

## cameraSequence.py
### Overview
This is the cameraSequence API for the machine. This API is in charge of handeling all camera related sequences the machine might need to perform.

## pumpSequence.py
### Overview
This is the pumpSequence API for the machine. This API is in charge of handeling all pump and nutrient related sequences the machine might need to perform.

## DCT.py
### Overview
This is the DCT API for the machine. This is an advanced security API that is capable of various image DCT encyption functions.
