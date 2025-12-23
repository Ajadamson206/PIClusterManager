from logger import globalLogger

globalLogger.logCriticalError("This is a crit error")
globalLogger.logError("This is a normal error")
globalLogger.logWarning("This is just a warning")
globalLogger.logDebug("Test Debug message")

globalLogger.hideDebug()

globalLogger.logCriticalError("This is a crit error")
globalLogger.logError("This is a normal error")
globalLogger.logWarning("This is just a warning")
globalLogger.logDebug("Test Debug message")

globalLogger.hideWarning()

globalLogger.logCriticalError("This is a crit error")
globalLogger.logError("This is a normal error")
globalLogger.logWarning("This is just a warning")
globalLogger.logDebug("Test Debug message")
