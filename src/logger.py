import syslog

PROGRAM_NAME="PicoClusterManager"

class Logger:
    def __init__(self, identity, facility=syslog.LOG_LOCAL0):
        self.identity = identity
        self.facility = facility

    # Prevent debug logs from being logged
    def hideDebug(self):
        syslog.setlogmask(syslog.LOG_UPTO(syslog.LOG_WARNING))

    # Prevent warning logs from being logged
    def hideWarning(self):
        syslog.setlogmask(syslog.LOG_UPTO(syslog.LOG_ERR))

    # Decorator function used to wrap new logging functions
    def _logFunction(func):
        def newLog(self, message):
            syslog.openlog(ident=self.identity, logoption=syslog.LOG_PERROR, facility=self.facility) # Make sure that all logs logged to the perror alongside normal syslog
            func(self, message) # type: ignore
            syslog.closelog()
        return newLog
    
    @_logFunction # type: ignore
    def logCriticalError(self, message: str):
        syslog.syslog(syslog.LOG_CRIT | self.facility, "CRITICAL - " + message)

    @_logFunction # type: ignore
    def logError(self, message: str):
        syslog.syslog(syslog.LOG_ERR | self.facility, "ERROR - " + message)

    @_logFunction # type: ignore
    def logWarning(self, message: str):
        syslog.syslog(syslog.LOG_WARNING | self.facility, "WARNING - " + message)

    @_logFunction # type: ignore
    def logDebug(self, message: str):
        syslog.syslog(syslog.LOG_DEBUG | self.facility, "DEBUG - " + message)

global globalLogger
globalLogger = Logger(PROGRAM_NAME)