class Progress:
    def __init__(self, total:int, showFraction=False, showPercentage=False, barlength:int=20):
        self.emptyChar = "-"
        self.fullChar = "■"
        self.total = total
        self.showFraction = showFraction
        self.showPercentage = showPercentage
        self.barLength = barlength

    def printProgress(self, current:int):
        fullCharAmt = int((self.barLength*current)//self.total)
        emptyCharAmt = self.barLength - fullCharAmt
        fraction = (f"{current} / {self.total}") if self.showFraction else ("")
        percentage =  (f"{current / self.total:.2%}") if self.showPercentage else ("")
        print(f" [\033[1;32m{''.join([self.fullChar for _ in range(fullCharAmt)])}\033[00m{''.join([self.emptyChar for _ in range(emptyCharAmt)])}]   {fraction}   {percentage}", end='\r')

    def printComplete(self, msg:str):
        print(f"\033[1;32m{msg}\033[00m                                                                          ")

    def printError(self, msg:str):
        print(f"\033[1;31m{msg}\033[00m                                                                          ")
