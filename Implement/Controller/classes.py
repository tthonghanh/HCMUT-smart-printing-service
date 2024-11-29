# Classes

class PrintingView:
    def showProgress(self):
        pass

    def displayQuota(self):
        pass

    def confirmPrinting(self):
        pass

    def onPrint(self):
        pass

    def onChoosePrinter(self):
        pass

    def showPrinterList(self):
        pass

    def onPayment(self):
        pass

    def showNewBalance(self):
        pass

    def displayPrintingHistory(self):
        pass

    def onSettingProperties(self):
        pass

    def onUpload(self):
        pass

    def displayError(self):
        pass

    def previewDocument(self):
        pass


class PrintController:
    def choosePrinter(self):
        pass

    def specifyPrintingProperties(self):
        pass

    def confirmPrinting(self):
        pass

    def printDocument(self):
        pass

    def checkUserQuota(self):
        pass

    def logPrintingAction(self):
        pass

    def confirmPrintJob(self):
        pass

    def requestMorePages(self):
        pass

    def checkBalance(self):
        pass

    def uploadDocument(self):
        pass

    def validateDocument(self):
        pass


class Printer:
    def __init__(self, printerID, status, location):
        self.printerID = printerID
        self.status = status
        self.location = location

    def printDocument(self):
        pass

    def checkPrinterStatus(self):
        pass


class PrintJob:
    def __init__(self, jobID, studentID, printerID, documentID, status, config, startTime, endTime):
        self.jobID = jobID
        self.studentID = studentID
        self.printerID = printerID
        self.documentID = documentID
        self.status = status
        self.config = config
        self.startTime = startTime
        self.endTime = endTime

    def startPrintJob(self):
        pass

    def cancelPrintJob(self):
        pass

    def logPrintJobInfo(self):
        pass


class UserAccount:
    def __init__(self, name, email, balance):
        self.name = name
        self.email = email
        self.balance = balance

    def uploadDocument(self):
        pass

    def choosePrinter(self):
        pass

    def specifyPrintProperties(self):
        pass

    def payForMoreQuota(self):
        pass

    def checkBalance(self):
        return self.balance


class StudentAccount(UserAccount):
    def __init__(self, name, email, balance, studentId):
        super().__init__(name, email, balance)
        self.studentId = studentId


class Payment:
    def __init__(self, paymentID, amount, transactionStatus, paymentInfo):
        self.paymentID = paymentID
        self.amount = amount
        self.transactionStatus = transactionStatus
        self.paymentInfo = paymentInfo

    def logPayment(self):
        pass

    def processPayment(self):
        pass

    def refundPayment(self):
        pass


class Document:
    def __init__(self, documentID, fileName, fileSize, fileType):
        self.documentID = documentID
        self.fileName = fileName
        self.fileSize = fileSize
        self.fileType = fileType

    def validateDocument(self):
        pass

    def previewDocument(self):
        pass


class ConfigFile:
    def __init__(self, paperSize, totalPages, isDoubleSided, numberOfCopies):
        self.paperSize = paperSize
        self.totalPages = totalPages
        self.isDoubleSided = isDoubleSided
        self.numberOfCopies = numberOfCopies

    def setProperty(self):
        pass

    def getProperty(self):
        pass
