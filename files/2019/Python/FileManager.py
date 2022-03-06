import os
import ast

class File:
    def __init__(self,filename):
        self.filename = filename

    def Save(self,dict):
        file = open(self.filename,"w")
        file.write(str(dict))
        file.close

    def Retrieve(self):
        try:
            file = open(self.filename,"r")
            dict = ast.literal_eval(file.read())
            file.close
        except:
            dict = {}
        return dict

    def Count(self):
        try:
            file = open(self.filename,"r")
            dict = ast.literal_eval(file.read())

            count = 0
            for x in dict:
                count = count + 1
            file.close
            
            return count
        except:
            return 0

        
