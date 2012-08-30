
import heapq
import json
import os
import argparse

## dis version is soo much nicer mannnn
class CityDistance:
    
    #Example Inputs
    ## metricMap = [('Population, 2010 ',.00007),('Area', .3),('Violent crime',.02),('Median value of owner-occupied housing units, 2006-2010 ',.0005)]
    ## spendingMap = [('Expenditure','Transportation','Public Transit',.005),('Expenditure','Public Safety', 'Fire',.0000003),('Revenue','Fines and Forfeitures','Other Fines, Forfeitures, and Penalties',.000002)] 
    ##
    def __init__(self,metricScalingValues,spendingScalingValues):
        
        self.benchmarkMap = self.importBenchmarks('benchmarkData.json')
        self.spendingMap = self.importSpending('./json')

        self.target = None;
        

        citiesScaledMetricsMap = self.collectAndScaleMetrics(metricScalingValues)
        #
        ##If no spending tuples just use the metric data
        #
        if len(spendingScalingValues) == 0:
            self.Map = citiesScaledMetricsMap
        #
        ## Else merge metric data into spending data
        #
        else:
            citiesScaledSpendingMap = self.collectAndScaleSpending(spendingScalingValues)
            self.Map = self.mergeMaps(citiesScaledSpendingMap,citiesScaledMetricsMap)
   
    #
    ## Function: importBenchmarks    
    ## Purpose: Read benchmarks json into a dict
    #
    def importBenchmarks(self,filename):
        benchmarkMap = {}
        fp = open(filename)
        for line in fp:
            benchmarkData = json.loads(line)
            city = benchmarkData['CityName']
            benchmarkMap[city] = benchmarkData
        fp.close()
        return benchmarkMap   
    
    #
    ## Function: importSpending
    ## Read all individual SCO json files into a single map
    #
    def importSpending(self,folder):
        spendingMap = {}
        for d, ds, files in os.walk(folder):
            for filename in files:
                path = os.path.join(folder,filename)
                fp = open(path)
                for line in fp:
                    cityData = json.loads(line)
                    city = cityData['CityName']
                    spendingMap[city] = cityData
                fp.close()
        return spendingMap
    
    #    
    ## Function: collectAndScaleMetrics
    ## Uses metricMap to extract the requested metric values, scale them according to
    ## the scaling factor, and add them to a map where the key is the city name and the values
    ## are the vector of amounts
    ## Example for metricMap: [('Population, 2010 ',.00007),('Area', .3),('Violent crime',.02),('Median value of owner-occupied housing units, 2006-2010 ',.0005)]
    #
            
    def collectAndScaleMetrics(self,metricScalingValues):
        
        metricsMap = {}
        #add metrics
        for city in self.benchmarkMap:
            cityVector = []
            
            for metricName,scaleValue in metricScalingValues.iteritems():
                value = 0
                try:
                    metricValue = self.benchmarkMap[city][metricName]
                    if len(metricValue) == 0:
                        metricValue = 0
                    value = float(metricValue)*float(scaleValue)
                except KeyError:
                    pass
                cityVector.append(value)
            metricsMap[city] = cityVector
        return metricsMap
    
    #
    ## Function: collectAndScaleSpending
    ## Uses spendingMap to extract the requested spending amounts, scale them according to
    ## the scaling factor and add them to a map where the key is the city name and the values
    ## are the vector of amounts
    ## Example for spendingMap: [('Expenditure','Transportation','Public Transit',.005),('Expenditure','Public Safety', 'Fire',.0000003)]
    #
    def collectAndScaleSpending(self,spendingScalingValues):        
    
        def average(valueMap):
            total = 0
            numValues = 0
            for val in valueMap.itervalues():
                total += float(val)
                numValues += 1
            return total/numValues
        
        def categoryEmpty(categoryMap):
            subcategoryCount = 0
            for value in categoryMap.itervalues():
                subcategoryCount += len(value)
            return subcategoryCount == 0
        
        citySpendingMap = {}
        
        #add spendingData
        for city in self.spendingMap:
            cityVector = []
            for spendingNames,scaleValue in spendingScalingValues.iteritems():
                spendingNames = spendingNames.split(':')
                
                spendingType,category,subcategory = spendingNames[0],spendingNames[1],spendingNames[2]
             

                value = 0
                
                #
                ## If all subcategories in this category are empty declare the category not found
                #
                
                try:
                    noCategory = categoryEmpty(self.spendingMap[city][city][spendingType][category])
                except KeyError:
                    noCategory = True
                    
                try:
                    values = self.spendingMap[city][city][spendingType][category][subcategory]['Amount']
                    
                    if len(values) == 0:
                        value = 0
                    else:
                        value = average(values)
                    value = value*float(scaleValue)
                except KeyError:
                    pass
               
                #
                ## Sets value to -1 so the distance code knows to nuke it,
                #
                
                if noCategory:
                    cityVector.append(-1)
                else:
                    cityVector.append(value)    
            
            citySpendingMap[city] = cityVector
        
        return citySpendingMap       
    
    #
    ## Function: mergeMaps
    ## Get spendingMap and metricMap. The keys are city names and the values are lists of scaled numbers
    ## This code combines the two lists of scaled numbers
    #
    def mergeMaps(self,spendingMap,metricMap):
        
        def getLength(mapIn):
            for value in mapIn.itervalues():
                return len(value)  
        #
        ## For every city in the spendingMap, append the metric values
        #
        for city in spendingMap.iterkeys():
            if city in metricMap:
                spendingMap[city] = spendingMap[city] + metricMap[city]
            else:
                spendingMap[city] = spendingMap[city] + getLength(metricMap)*[0]         
       
        #
        ## For now we are ignoring cities that appear ONLY in the metric data
        #
        
        '''
        for city in map2.iterkeys():
            if city not in map2:
                map1[city] = getLength(map1)*[0]  + map2[city]
        
        for key, item in map1.iteritems():
            print key, item,len(item)
        '''
        
        return spendingMap     
    
    #
    ## Function: distanceBetweenVectors 
    ## Takes two vectors of numbers. Finds distance
    #    
    def distanceBetweenVectors(self,vector1,vector2):
        distance = 0
        for index in range(len(vector1)):
            item1 = vector1[index]
            item2 = vector2[index]        
            
            #
            ## If Spending Category was not present, value was assigned to -1 instead of 0
            ## NUKE IT
            #
            
            if (item1 == -1) or (item2 == -1):
                distance += 50
            else:
                distance += abs(float(item1)-float(item2))
        return distance

    #
    ## Function: sort 
    ## Sorts cities by distance to input 'city'
    #
    def sort(self,city):

        targetVector = self.Map[city]
 
        # create array of distances to target
        self.distances = []
        self.distances = []
        for city,vector in self.Map.iteritems():
            heapq.heappush(self.distances, (self.distanceBetweenVectors(targetVector,vector),city))   
        return self.distances
    
    #
    ## Function: toJson
    ## Append first numCities cities to an array and return a JSON version of that array
    #
    
    def toJson(self,numCities):
        array = []
        while (numCities >= 0):
            array.append(heapq.heappop(self.distances)[1])
            numCities -= 1
        return json.dumps(array)

def main():
    '''
    parser = argparse.ArgumentParser(description = '[City Name, [Weights], Category]')
    parser.add_argument('data', nargs = '+')
    results = parser.parse_args()

    city = results.data[0]
    arg1 = json.loads(results.data[1])
    
    ##user can opt not to include spendingMap.. If so only metric values are used 
    try:
        arg2 = json.loads(results.data[2])
    except IndexError:
        arg2 = []
    metricMap,spendingMap = arg1,arg2
    '''
    city = 'Palo Alto'
    metricScalingValues = {'Population: 2010 ':.00007,'Area': .3,'Violent crime':.02,'Median value of owner-occupied housing units: 2006-2010 ':.0005}
    spendingScalingValues = {'Expenditure:Transportation:Public Transit':.005,'Expenditure:Public Safety:Fire':.0000003,'Revenue:Fines and Forfeitures:Other Fines: Forfeitures: and Penalties':.000002} 
    print metricScalingValues['Population: 2010 ']
    print spendingScalingValues['Expenditure:Transportation:Public Transit']
    '''
    metricMap = [('Population, 2010 ',.00007),('Area', .3),('Violent crime',.02),('Median value of owner-occupied housing units, 2006-2010 ',.0005)]
    spendingMap = [('Expenditure','Transportation','Public Transit',.005),('Expenditure','Public Safety', 'Fire',.0000003),('Revenue','Fines and Forfeitures','Other Fines, Forfeitures, and Penalties',.000002)] 
    '''
    
    c = CityDistance(metricScalingValues,spendingScalingValues)
    c.distances = c.sort(city)  
    print c.toJson(10)
    
if __name__ == "__main__": 
    main()    

