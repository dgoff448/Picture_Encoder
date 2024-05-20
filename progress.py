class Progress:
    def __init__(self, total:int, barMsg="", showFraction=False, showPercentage=False, barlength:int=20):
        self.emptyChar = "-"
        self.fullChar = "■"
        self.total = total
        self.barMsg = barMsg
        self.showFraction = showFraction
        self.showPercentage = showPercentage
        self.barLength = barlength

    def printProgress(self, current:int):
        fullCharAmt = int((self.barLength*current)//self.total)
        emptyCharAmt = self.barLength - fullCharAmt
        fraction = (f"{current} / {self.total}") if self.showFraction else ("")
        percentage =  (f"{current / self.total:.2%}") if self.showPercentage else ("")
        print(f"\033[1;33m{self.barMsg}\033[00m [\033[1;32m{''.join([self.fullChar for _ in range(fullCharAmt)])}\033[00m{''.join([self.emptyChar for _ in range(emptyCharAmt)])}]   {fraction}   {percentage}", end='\r')

    def printComplete(self, msg:str):
        print(f"\033[1;32m{msg}\033[00m                                                                          ")

    def printInProgress(self, msg:str):
        print(f"\033[1;33m{msg}\033[00m                                                                          ", end='\r')

    def printError(self, msg:str):
        print(f"\033[1;31m{msg}\033[00m                                                                          ")
