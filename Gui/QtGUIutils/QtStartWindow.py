import logging

# Customize the logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="my_project.log",  # Specify a log file
    filemode="w",  # 'w' for write, 'a' for append
)

logger = logging.getLogger(__name__)

from PyQt5.QtCore import *
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateTimeEdit,
    QDial,
    QDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QScrollBar,
    QSizePolicy,
    QSlider,
    QSpinBox,
    QStyleFactory,
    QTableWidget,
    QTabWidget,
    QTextEdit,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QMainWindow,
    QMessageBox,
)


import sys
import os
import math
import subprocess
import time

from Gui.QtGUIutils.QtRunWindow import *
from Gui.QtGUIutils.QtFwCheckDetails import *
from Gui.QtGUIutils.QtApplication import *
from Gui.python.CustomizedWidget import *
from Gui.python.Firmware import *
from Gui.GUIutils.DBConnection import *
from Gui.GUIutils.FirmwareUtil import *
from Gui.GUIutils.settings import *
from Gui.siteSettings import *
from InnerTrackerTests.TestSequences import TestList
# from Gui.QtGUIutils.QtProductionTestWindow import *


class SummaryBox(QWidget):
    def __init__(self, master, module, index=0):
        super(SummaryBox, self).__init__()
        self.module = module
        self.master = master
        self.index = index
        self.result = False
        self.verboseResult = {}
        self.chipSwitches = {}

        self.mainLayout = QGridLayout()
        self.initResult()
        self.createBody()
        self.measureFwPar()
        # self.checkFwPar()
        self.setLayout(self.mainLayout)

    def initResult(self):
        for i in ModuleLaneMap[self.module.getType()].keys():
            self.verboseResult[i] = {}
            self.chipSwitches[i] = True

    def createBody(self):
        FEIDLabel = QLabel("Module: {}".format(self.module.getSerialNumber()))
        FEIDLabel.setStyleSheet("font-weight:bold")
        PowerModeLabel = QLabel()
        PowerModeLabel.setText("FE Power Mode:")
        self.PowerModeCombo = QComboBox()
        self.PowerModeCombo.addItems(FEPowerUpVD.keys())
        # self.PowerModeCombo.currentTextChanged.connect(self.checkFwPar)
        # self.ChipBoxWidget = ChipBox(self.module.getType())

        self.CheckLabel = QLabel()
        self.DetailsButton = QPushButton("Details")
        self.DetailsButton.clicked.connect(self.showDetails)

        self.mainLayout.addWidget(FEIDLabel, 0, 0, 1, 1)
        # self.mainLayout.addWidget(self.ChipBoxWidget,0,1,1,1)
        self.mainLayout.addWidget(PowerModeLabel, 1, 0, 1, 1)
        self.mainLayout.addWidget(self.PowerModeCombo, 1, 1, 1, 1)
        self.mainLayout.addWidget(self.CheckLabel, 2, 0, 1, 1)
        self.mainLayout.addWidget(self.DetailsButton, 2, 1, 1, 1)

    def measureFwPar(self):
        for index, (key, value) in enumerate(self.verboseResult.items()):
            value["Power-up Mode"] = self.PowerModeCombo.currentText()
            # Fixme
            measureList = [
                "Analog Volts(V)",
                "Digital Volts(V)",
                "Analog I(A)",
                "Digital I(A)",
            ]
            for item in measureList:
                value[item] = 1.0
            self.verboseResult[key] = value

    def checkFwPar(self, pfirmwareName):
        # To be finished

        try:
            self.result = True
            FWisPresent = False
            if "CROC" in self.module.getType():
                boardtype = "RD53B"
            else:
                boardtype = "RD53A"

            # updating uri value in template xml file with correct fc7 ip address, as specified in siteSettings.py
            fc7_ip = FC7List[pfirmwareName]
            
            uricmd = "sed -i -e 's/192.168.0.50/{0}/g' {1}/Gui/CMSIT_{2}.xml".format(    
                fc7_ip, os.environ.get("GUI_dir"), boardtype
            )
            updateuri = subprocess.call([uricmd], shell=True)

            firmwareImage = firmware_image[self.module.getType()][
                os.environ.get("Ph2_ACF_VERSION")
            ]
            print("checking if firmware is on the SD card for {}".format(firmwareImage))
            fwlist = subprocess.run(
                [
                    "fpgaconfig",
                    "-c",
                    os.environ.get("GUI_dir") + "/Gui/CMSIT_{}.xml".format(boardtype),
                    "-l",
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            # fwlist = subprocess.run(["fpgaconfig","-c",os.environ.get('PH2ACF_BASE_DIR')+'/test/CMSIT_{}.xml'.format(boardtype),"-l"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            print("firmwarelist is {0}".format(fwlist.stdout.decode("UTF-8")))
            print("firmwareImage is {0}".format(firmwareImage))
            if firmwareImage in fwlist.stdout.decode("UTF-8"):
                FWisPresent = True
                print("firmware found")
            else:
                try:
                    print(
                        "Saving fw image {0} to SD card".format(
                            os.environ.get("GUI_dir")
                            + "/FirmwareImages/"
                            + firmwareImage
                        )
                    )
                    fwsave = subprocess.run(
                        [
                            "fpgaconfig",
                            "-c",
                            os.environ.get("GUI_dir") + "/Gui/CMSIT_{}.xml".format(boardtype),
                            "-f",
                            "{}".format(
                                os.environ.get("GUI_dir")
                                + "/FirmwareImages/"
                                + firmwareImage
                            ),
                            "-i",
                            "{}".format(firmwareImage),
                        ],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                    )
                    # self.fw_process.start("fpgaconfig",["-c","CMSIT.xml","-f","{}".format(os.environ.get("GUI_dir")+'/FirmwareImages/' + self.firmwareImage),"-i","{}".format(self.firmwareImage)])
                    print(fwsave.stdout.decode("UTF-8"))
                    FWisPresent = True
                except:
                    print(
                        "unable to save {0} to FC7 SD card".format(
                            os.environ.get("GUI_dir")
                            + "/FirmwareImages/"
                            + self.firmwareImage
                        )
                    )

            if FWisPresent:
                print("Loading FW image")
                fwload = subprocess.run(
                    [
                        "fpgaconfig",
                        "-c",
                        os.environ.get("GUI_dir") + "/Gui/CMSIT_{}.xml".format(boardtype),
                        "-i",
                        "{}".format(firmwareImage),
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                print(fwload.stdout.decode("UTF-8"))
                print("resetting beboard")
                fwreset = subprocess.run(
                    ["CMSITminiDAQ", "-f", os.environ.get("GUI_dir") + "/Gui/CMSIT_{}.xml".format(boardtype), "-r"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                print(fwreset.stdout.decode("UTF-8"))
                print(fwreset.stderr.decode("UTF-8"))

                print("Firmware image is now loaded")
            logging.debug("Made it to turn on LV")
            if self.master.desired_devices["lv"]:
                self.master.powering_mode = self.PowerModeCombo.currentText()

                # self.master.LVpowersupply.setCompCurrent(compcurrent = 1.05) # Fixed for different chip
                self.master.module_in_use = self.module.getType()

                self.master.instruments.lv_on(
                    None,
                    ModuleVoltageMapSLDO[self.master.module_in_use],
                    ModuleCurrentMap[self.master.module_in_use],
                )
                logging.info("Turned on LV power supply")

            # # Want to try and connect twice
            # self.Stopcount = 0
            # while self.Stopcount < 2:
            #     measurements = self.master.instruments._lv.measure(self.master.instruments._default_lv_channel)
            #     # find the set value
            #     TestVoltage = ModuleVoltageMapSLDO[self.master.module_in_use]
            #     TestCurrent = ModuleCurrentMap[self.master.module_in_use]
            #     print("Readvoltage:" + str(measurements[0]))
            #     print("Readcurrent:" + str(measurements[1]))
            #     print("TestCurrent" + str(TestCurrent))
            #     print("TestVoltage" + str(TestVoltage))

            #     # compare the difference between the Setup value vs the reading value
            #     volDiff = abs(TestVoltage - measurements[0])
            #     ampDiff = abs(TestCurrent - measurements[1])

            #     if volDiff <= 0.5 and ampDiff <= 0.5 and (self.master.instruments.status(None)["lv"]):
            #         leakageCurrent = 0.0
            #         _, measurement = self.master.instruments.hv_on(None, voltage = defaultHVsetting, delay = 0.3, step_size = -3, measure = True)
            #         leakageCurrent = measurement[-1][2]

            #         logger.debug(f"Leakage Current: {leakageCurrent}")
            #         properCurrent = ModuleCurrentMap[self.module.getType()]
            #         if (
            #             current < properCurrent + 0.2
            #             and current > properCurrent - 0.2
            #         ):
            #             self.result = True
            #             self.CheckLabel.setText(
            #                 "OK\nCurrent: {:.2f}A\nVoltage: {:.2f}V".format(
            #                     measurements[1], measurements[0]
            #                 )
            #             )
            #             self.CheckLabel.setStyleSheet("color:green")
            #         else:
            #             self.result = False
            #             self.CheckLabel.setText(
            #                 "Failed\nCurrent: {:.2f}A\nVoltage: {:.2f}V".format(
            #                     measurements[1], measurements[0]
            #                 )
            #             )
            #             self.CheckLabel.setStyleSheet("color:red")

            #     else:
            #         self.result = False
            #         self.CheckLabel.setText(
            #             "Failed\nCurrent: {:.2f}A\nVoltage: {:.2f}V".format(
            #                 measurements[1], measurements[0]
            #             )
            #         )
            #         self.CheckLabel.setStyleSheet("color:red")

            #         self.Stopcount += 1
            #         print("LV PS is off now. HV PS can't be turn on")
            #         print("attempt to turn on the LV PS again")
            #         time.sleep(2)

            #if self.master.desired_devices["hv"]:
            #    self.master.instruments.hv_on(
            #        lv_channel=None, voltage=defaultHVsetting, delay=0.3, step_size=10
            #    )

            #    logging.info("Turned on HV power supply")
            ##if not 'SLDO' in self.TestCombo.currentText():
             #   print('this should turn on hv')
            #    self.master.instruments.hv_on(
             #       lv_channel=None, voltage=defaultHVsetting, delay=0.3, step_size=10
             #   )


            return self.result
        except Exception as err:
            self.result = False
            self.CheckLabel.setText("No measurement")
            self.CheckLabel.setStyleSheet("color:red")
            # logging.error("Failed to check current")
            logging.error(err)
            return False

    def getDetails(self):
        pass

    def showDetails(self):
        self.measureFwPar()
        self.occupied()
        self.DetailPage = QtFwCheckDetails(self)
        self.DetailPage.closedSignal.connect(self.release)

    def getResult(self):
        return self.result

    def occupied(self):
        self.DetailsButton.setDisabled(True)

    def release(self):
        self.DetailsButton.setDisabled(False)


class QtStartWindow(QWidget):
    def __init__(self, master, firmware):
        super(QtStartWindow, self).__init__()
        self.master = master
        self.firmware = firmware
        self.firmwares = firmware
        self.firmwareName = firmware.getBoardName()
        self.connection = self.master.connection
        self.mainLayout = QGridLayout()
        self.setLayout(self.mainLayout)
        self.runFlag = False
        self.passCheck = False
        self.setLoginUI()
        self.createHead()
        self.createMain()
        self.createApp()
        self.occupied()

    def setLoginUI(self):
        self.setGeometry(400, 400, 400, 400)
        self.setWindowTitle("Start a new test")
        self.show()

    def createHead(self):
        self.TestBox = QGroupBox()
        testlayout = QGridLayout()
        TestLabel = QLabel("Test:")
        self.TestCombo = QComboBox()
        #self.TestList = getAllTests(self.master.connection)
        self.TestList = TestList
        self.TestCombo.addItems(self.TestList)
        TestLabel.setBuddy(self.TestCombo)

        testlayout.addWidget(TestLabel, 0, 0, 1, 1)
        testlayout.addWidget(self.TestCombo, 0, 1, 1, 1)
        self.TestBox.setLayout(testlayout)

        self.firmware.removeAllModule()

        self.BeBoardWidget = BeBoardBox(self.master,self.firmware)  # FLAG



        self.mainLayout.addWidget(self.TestBox, 0, 0)
        self.mainLayout.addWidget(self.BeBoardWidget, 1, 0)

    def createMain(self):
        self.firmwareCheckBox = QGroupBox()
        firmwarePar = QGridLayout()
        ## To be finished
        self.ModuleList = []
        for i, module in enumerate(self.BeBoardWidget.ModuleList):
            ModuleSummaryBox = SummaryBox(master=self.master, module=module)
            self.ModuleList.append(ModuleSummaryBox)
            firmwarePar.addWidget(
                ModuleSummaryBox, math.floor(i / 2), math.ceil(i % 2 / 2), 1, 1
            )
        self.BeBoardWidget.updateList()  ############FIXME:  This may not work for multiple modules at a time.
        self.firmwareCheckBox.setLayout(firmwarePar)

        self.mainLayout.addWidget(self.firmwareCheckBox, 2, 0)

    def destroyMain(self):
        self.firmwareCheckBox.deleteLater()
        self.mainLayout.removeWidget(self.firmwareCheckBox)

    def createApp(self):
        self.AppOption = QGroupBox()
        self.StartLayout = QHBoxLayout()

        self.CancelButton = QPushButton("&Cancel")
        self.CancelButton.clicked.connect(self.release)
        self.CancelButton.clicked.connect(self.closeWindow)

        self.ResetButton = QPushButton("&Reset")
        self.ResetButton.clicked.connect(self.destroyMain)
        self.ResetButton.clicked.connect(self.createMain)

        self.CheckButton = QPushButton("&Check")
        self.CheckButton.clicked.connect(self.checkFwPar)

        self.NextButton = QPushButton("&Next")
        self.NextButton.setDefault(True)
        # self.NextButton.setDisabled(True)
        self.NextButton.clicked.connect(self.openRunWindow)

        self.StartLayout.addStretch(1)
        self.StartLayout.addWidget(self.CancelButton)
        self.StartLayout.addWidget(self.ResetButton)
        self.StartLayout.addWidget(self.CheckButton)
        self.StartLayout.addWidget(self.NextButton)
        self.AppOption.setLayout(self.StartLayout)

        self.LogoGroupBox = QGroupBox("")
        self.LogoGroupBox.setCheckable(False)
        self.LogoGroupBox.setMaximumHeight(100)

        self.LogoLayout = QHBoxLayout()
        OSULogoLabel = QLabel()
        OSUimage = QImage("icons/osuicon.jpg").scaled(
            QSize(200, 60), Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        OSUpixmap = QPixmap.fromImage(OSUimage)
        OSULogoLabel.setPixmap(OSUpixmap)
        CMSLogoLabel = QLabel()
        CMSimage = QImage("icons/cmsicon.png").scaled(
            QSize(200, 60), Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        CMSpixmap = QPixmap.fromImage(CMSimage)
        CMSLogoLabel.setPixmap(CMSpixmap)
        self.LogoLayout.addWidget(OSULogoLabel)
        self.LogoLayout.addStretch(1)
        self.LogoLayout.addWidget(CMSLogoLabel)

        self.LogoGroupBox.setLayout(self.LogoLayout)

        # self.mainLayout.addWidget(self.LoginGroupBox, 0, 0)
        # self.mainLayout.addWidget(self.LogoGroupBox, 1, 0)

        self.mainLayout.addWidget(self.AppOption, 3, 0)
        self.mainLayout.addWidget(self.LogoGroupBox, 4, 0)

    def closeWindow(self):
        self.close()

    def occupied(self):
        self.master.ProcessingTest = True

    def release(self):
        self.master.ProcessingTest = False
        self.master.NewTestButton.setDisabled(False)
        self.master.LogoutButton.setDisabled(False)
        self.master.ExitButton.setDisabled(False)

    def checkFwPar(self, pfirmwareName):
        GlobalCheck = True
        for item in self.ModuleList:
            item.checkFwPar(pfirmwareName)
            GlobalCheck = GlobalCheck and item.getResult()
        self.passCheck = GlobalCheck
        return GlobalCheck

    def setupBeBoard(self):
        # Setup the BeBoard
        pass

    def openRunWindow(self):
        # if not os.access(os.environ.get('GUI_dir'),os.W_OK):
        # 	QMessageBox.warning(None, "Error",'write access to GUI_dir is {0}'.format(os.access(os.environ.get('GUI_dir'),os.W_OK)), QMessageBox.Ok)
        # 	return
        # if not os.access("{0}/test".format(os.environ.get('PH2ACF_BASE_DIR')),os.W_OK):
        # 	QMessageBox.warning(None, "Error",'write access to Ph2_ACF is {0}'.format(os.access(os.environ.get('PH2ACF_BASE_DIR'),os.W_OK)), QMessageBox.Ok)
        # 	return

        # NOTE This is not the best way to do this, we should be emitting a signal to change
        # the module type but ModuleBox is not publically accessible so we have to go through BeBoardWidget
        self.master.module_in_use = self.BeBoardWidget.getModules()[0].getType()

        for module in self.BeBoardWidget.getModules():
            if module.getSerialNumber() == "":
                QMessageBox.information(
                    None, "Error", "No valid serial number!", QMessageBox.Ok
                )
                return
            if module.getID() == "":
                QMessageBox.information(None, "Error", "No valid ID!", QMessageBox.Ok)
                return
        self.checkFwPar(self.firmwareName)
        if self.passCheck == False:
            reply = QMessageBox().question(
                None,
                "Error",
                "Front-End parameter check failed, forced to continue?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply == QMessageBox.No:
                return

        self.firmwareDescription = self.BeBoardWidget.getFirmwareDescription()
        # self.info = [self.firmware.getModuleByIndex(0).getModuleID(), str(self.TestCombo.currentText())]
        self.info = [
            self.firmware.getModuleByIndex(0).getOpticalGroupID(),
            str(self.TestCombo.currentText()),
        ]
        self.runFlag = True
        self.master.BeBoardWidget = self.BeBoardWidget
        self.master.RunNewTest = QtRunWindow(
            self.master, self.info, self.firmwareDescription
        )
        self.close()

    def closeEvent(self, event):
        if self.runFlag == True:
            event.accept()

        else:
            reply = QMessageBox.question(
                self,
                "Window Close",
                "Are you sure you want to quit the test?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )

            if reply == QMessageBox.Yes:
                event.accept()
                self.release()
                # This line was previosly commented
                try:
                    self.master.instruments.off(
                        lv_channel=None, hv_delay=0.5, hv_step_size=10
                    )

                    print("Window closed")
                except:
                    print(
                        "Waring: Incident detected while trying to turn of power supply, please check power status"
                    )
            else:
                event.ignore()
