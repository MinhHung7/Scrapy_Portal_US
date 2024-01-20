class Event:
    def __init__(self, header='', content='', date = '', start_time='', end_time=''):
        self.header = header
        self.content = content
        self.start_time = start_time
        self.end_time = end_time
        self.date = date
    def Print(self):
        print(self.header)
        print(self.content)
        print(self.start_time)
        print(self.end_time)
        print(self.date)
        print("----------------------")
