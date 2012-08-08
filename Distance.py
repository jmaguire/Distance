import csv
import time 
import json

class CityDistance:
    
    def fillArrays(self):
        self.fileData.next()
        for index, line in enumerate(self.fileData):
            key = line[0].strip().lower()
            self.map[key] = index
            #print line
            self.data.append(line)
        b = []    
        for line in self.fileWeights:  
            self.weights.append(line[0])
            b.append(line[2])
        print json.dumps(b)
    def __init__(self,filename):
        self.data = []
        self.weights = []
        self.fileData = csv.reader(open(filename+'.csv',"r"))
        self.fileWeights = csv.reader(open('weightsFire.csv',"r"))
        self.map = {}
        self.fillArrays()
        print json.dumps(['Palo Alto',self.weights,'Police'])
        #print self.map
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
        print key
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
            if index > 10:
                break
            if index % 5 == 0:
                string += '\n'
            string += line[0].strip() +', '  
        return string
    def array(self):
        array = []
        for index, line in enumerate(self.distances[1:]):
            if index > 100:
                break
            array.append(line[0].strip())  
        return array
    
    
if __name__ == "__main__": 
    c = CityDistance('cali')
    t1 = time.clock()
    c.distances = c.sort('Los Altos')       
    t2 = time.clock()
    print str(c)     
   # print t2-t1
    data = json.dumps(c.array())
    #print data
    #print c.array()