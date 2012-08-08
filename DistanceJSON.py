import csv
import time 
import json
import argparse


class CityDistance:
    
    def fillArrays(self,measure):
        self.fileData.next()
        for index, line in enumerate(self.fileData):
            key = line[0].strip().lower()
            self.map[key] = index
            #print line
            self.data.append(line)
        
            
        #Import Has Department File
        hasDepartments = csv.reader(open('HasDepartment.csv',"r"))
       
        #Find index of measure
        line = hasDepartments.next()
        measure = measure.lower().strip()
        for index, word in enumerate(line):
            key = word.lower().strip()
            if(measure == key):
                self.hasDepartmentsIndex = index - 1 #city name is not part of bitvector
                break
            
        #Grab boolean value at index of measure
        #1 means measure is present. 0 means measure is not.
        for line in hasDepartments:  
            key = line[0].lower().strip()
            value = line[1:][self.hasDepartmentsIndex]
            self.hasDepartments[key] = value
    
    def __init__(self,filename,weights,measure):
        self.data = []
        self.weights = []
        self.fileData = csv.reader(open(filename+'.csv',"r"))
        self.map = {}
        self.hasDepartmentsIndex = -1; 
        self.hasDepartments = {};
        self.fillArrays(measure)
        self.weights = weights
        self.target = None;
        
    def distToTarget(self,city):
        distance = 0
        for index in range(len(city)):
           
            item1 = city[index].strip()
            item2 = self.target[index].strip()
            if item1.isalpha() or len(item1) == 0:
                item1 = 0.0
            if item2.isalpha() or len(item2) == 0:
                item2 = 0.0
            distance += abs(float(item1)-float(item2))*float(self.weights[index])
        #print distance
        return distance

    def compare(self,x,y):
        d = x[1] - y[1]
        if d > 0:
            return 1
        if d < 0:
            return -1
        return 0
    
    def sort(self,city):
        key = city.strip().lower()
        self.targetCity = key;
        self.target = self.data[self.map[key]];
        self.target = self.target[1:]
        
        # create array of distances to target
        self.distances = []
        
        for line in self.data:
            temp = []
            temp.append(line[0])
            temp.append(self.distToTarget(line[1:]))
            self.distances.append(temp)
        return sorted(self.distances, cmp = lambda x,y: self.compare(x,y))
    
    def __str__(self):
        string = ''
        for index, line in enumerate(self.distances):
            if index > 100:
                break
            if index % 5 == 0:
                string += '\n'
            string += line[0].strip() +', '  
        return string
    
    #old function. not called
    def array(self):
        array = []
        for index, line in enumerate(self.distances[1:]):
            if index > 10:
                break
            array.append(line[0].strip())  
        return array
    
    def arrayCheckMeasure(self):
        array = []
        for index, line in enumerate(self.distances[1:]):
            if len(array) > 10: #breaks when 10 values have been added
                break
            key = line[0].lower().strip();
            index =self.hasDepartmentsIndex;
            try:
                hasDepartmentCurrent = self.hasDepartments[key]
                hasDepartmentTarget =  self.hasDepartments[self.targetCity]
                if(int(hasDepartmentCurrent)*int(hasDepartmentTarget) == 1):
                    array.append(line[0].strip())
            except KeyError:
                array.append(line[0].strip())
        return array
def main():
    '''
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description = '[City Name, [Weights], Category]')
    parser.add_argument('data', nargs = '+')
    results = parser.parse_args()
    array = json.loads(results.data[0])
    '''
    array = ["Palo Alto", ["0.00013", "0.53", "0.0013", "0", "0", "10", "45", "0", "20", "0", "45", "0", "0", "8", "0", "0", "0", "20", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "1.00E-05", "0", "0", "0", "0", "0", "0.0001", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0.016694763", "3.983611711", "0.292674953", "0.06375498", "0.027857514", "0.00212019", "0.009566184", "0.00334694", "0.019994171", "0.37973949", "0"],'Airports']
    city = str(array[0])
    weights = array[1]
    measure = str(array[2])
    c = CityDistance('cali',weights,measure)
    c.distances = c.sort(city)       
    #data = json.dumps(c.array())
    print json.dumps(c.arrayCheckMeasure())
    
if __name__ == "__main__": 
    main()    

