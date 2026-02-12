import time
from logger import globalLogger

class TimeSave:
    def __init__(self, file_path: str) -> None:
        if not file_path.endswith("/"):
            file_path += '/'

        self.currentTime = time.time()
        self.nextTime = self.currentTime + 10
        self.flipper = True
        self.file_path = file_path

    def time_loop(self) -> None:
        self.currentTime = time.time()
        if self.currentTime >= self.nextTime:
            try:
                if self.flipper:
                    globalLogger.logDebug("going to file 1")
                    with open(self.file_path + "time1.txt","w") as file:
                        file.write(str(self.currentTime))
                else:
                    globalLogger.logDebug("going to file 1")
                    with open(self.file_path + "time2.txt","w") as file:
                        file.write(str(self.currentTime))
            except Exception as e:
                file_name = "time1.txt" if self.flipper else "time2.txt"
                file = self.file_path
                if len(self.file_path) != 0 and self.file_path.endswith("/"):
                    file += file_name
                else:
                    file = file_name
                globalLogger.logError(f"Exception: {e}\nUnable to open file: " + file)

            self.flipper = self.flipper == False
            self.nextTime = self.currentTime + 10
    
    def getRecentTime(self) -> float:
        # Open File 1
        time1 = 0.0
        try:
            with open(self.file_path + "time1.txt", "r") as file1:
                time1 = float(file1.readline())
        except:
            globalLogger.logWarning("Unable to find file: " + self.file_path + "time1.txt")

        # Open File 2
        time2 = 0.0
        try:
            with open(self.file_path + "time2.txt", "r") as file1:
                time2 = float(file1.readline())
        except:
            globalLogger.logWarning("Unable to find file: " + self.file_path + "time2.txt")

        # Compare which one is greater
        return time1 if time1 > time2 else time2