class Student:
    def __init__(self, row):
        self.originalName = row[1]
        self.lowerName = self.originalName.lower()
        self.timestamp = row[0]
        self.answers = []
        self.answers = row[2:]

    def getAnswerByQuestionNumber(self, numString):
        if len(numString) > 0: num = int(numString)
        else: num = -1

        if num > 0 and num < len(self.answers) + 1: 
            return self.answers[num - 1]