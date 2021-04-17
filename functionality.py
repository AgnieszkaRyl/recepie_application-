import urllib3
import json, requests


class Functionality:
    def __init__(self):
        self.__url_search = 'https://api.spoonacular.com/recipes/complexSearch?apiKey='
        self.__apiKey = '2d1345d8d1ab47028856f5b4693977b5'
        self.finalUrlQuestion= ''

    def chooseDiet(self, dietType): #
        url = self.__url_search + self.__apiKey
        if dietType == '':
            self.finalUrlQuestion=url
        else:
            self.finalUrlQuestion = url + "&diet=" + dietType

    def chooseCuisine(self, cuisine):
        if cuisine == '':
            self.finalUrlQuestion=self.finalUrlQuestion
        else:
            self.finalUrlQuestion=self.finalUrlQuestion+"&cuisine=" + cuisine

    def searchByIntolerance(self,intolerances):
        if intolerances == '':
            self.finalUrlQuestion=self.finalUrlQuestion
        else:
            self.finalUrlQuestion = self.finalUrlQuestion +"&intolerances=" + intolerances

    def searchMaxCookingTime(self,maxTime):
        if maxTime == '':
            self.finalUrlQuestion=self.finalUrlQuestion
        else:
            self.finalUrlQuestion=self.finalUrlQuestion+"&maxReadyTime=" + str(maxTime)

    def serchWhatToEat(self, food):
        if food == '':
            self.finalUrlQuestion=self.finalUrlQuestion
        else:
            self.finalUrlQuestion=self.finalUrlQuestion+"&suggest&query=" + food

    def howManyRecepies(self, numberRecepies):
        if numberRecepies=='' or numberRecepies=='0':
            self.finalUrlQuestion=self.finalUrlQuestion
        else:
            self.finalUrlQuestion = self.finalUrlQuestion + "&number=" + str(numberRecepies)

    def getRecepiesListDict(self):
        http = urllib3.PoolManager()
        something = http.request('GET', self.finalUrlQuestion)
        data1 = something.data
        data_json = json.loads(data1)['results']
        return data_json

    def getRecepieList(self):
        listRecepies = self.getRecepiesListDict()
        listTitles=[]
        for elem in listRecepies:
            listTitles.append(elem['title'])
        return listTitles

    def getRecepieListDict(self):
        listRecepies = self.getRecepiesListDict()
        listTitles=[]
        for elem in listRecepies:
            listTitles.append({elem['title']:elem['id']})
        return listTitles

    def getRecepieDictById(self, id):
        url = 'https://api.spoonacular.com/recipes/' + str(id) + '/information?apiKey=' + self.__apiKey
        http = urllib3.PoolManager()
        httprequest = http.request('GET', url)
        recepieDictHttp = httprequest.data
        recepieDict = json.loads(recepieDictHttp)
        return recepieDict


    def getRecepieStepsAnalyzedById(self, id):
        url = 'https://api.spoonacular.com/recipes/' + str(id) + '/analyzedInstructions?apiKey=' + self.__apiKey
        http = urllib3.PoolManager()
        httprequest = http.request('GET', url)
        recepieDictHttp = httprequest.data
        recepieDict = json.loads(recepieDictHttp)
        listSteps=[]
        for elem in recepieDict:
            listSteps.append(elem['steps'])
        list=[]
        for elem in listSteps:
            for i in elem:
                list.append(i['step'])
        return list

    def getRecepieDictSummaryById(self,id):
        url = 'https://api.spoonacular.com/recipes/' + str(id) + '/summary?apiKey=' + self.__apiKey
        http = urllib3.PoolManager()
        httprequest = http.request('GET', url)
        recepieDictHttp = httprequest.data
        recepieDict = json.loads(recepieDictHttp)['summary']
        return recepieDict

    def getRecepieEqipmentById(self,id):
        url = 'https://api.spoonacular.com/recipes/' + str(id) + '/equipmentWidget.json?apiKey=' + self.__apiKey
        http = urllib3.PoolManager()
        httprequest = http.request('GET', url)
        recepieDictHttp = httprequest.data
        recepieDict = json.loads(recepieDictHttp)['equipment']
        namesEquipments = []
        for elem in recepieDict:
            namesEquipments.append(elem['name'])
        return namesEquipments



    def getRecepieImageAdresById(self,id):
        recepieDict = self.getRecepieDictById(id)
        return recepieDict['image']

    def getRecepieIngredientsById(self, id):
        recepieDict = self.getRecepieDictById(id)
        ingredientsListDict = recepieDict['extendedIngredients']
        ingredients = []
        for elem in ingredientsListDict:
            ingredients.append(elem['original'])
        return ingredients

    def getRecepieNutritionDictById(self, id):
        url = 'https://api.spoonacular.com/recipes/' + str(id) + '/nutritionWidget.json?apiKey=' + self.__apiKey
        http = urllib3.PoolManager()
        httprequest = http.request('GET', url)
        recepieDictHttp = httprequest.data
        recepieDictBad = json.loads(recepieDictHttp)['bad']
        recepieDictGood = json.loads(recepieDictHttp)['good']
        return recepieDictBad, recepieDictGood

    def getRecepieTitleById(self, id):
        recepieDict = self.getRecepieDictById(id)
        return recepieDict['title']


    def saveToNormalFile(self, id):
        dictWholeInformation = self.getRecepieDictById(id)
        #dictResult = {id: (dictWholeInformation['title'], dictWholeInformation['readyInMinutes'], dictWholeInformation['healthScore'])}
        file=open('przepisy.txt', 'a')
        file.write(str(id)+"\t"+str(dictWholeInformation['title'])+"\t"+str(dictWholeInformation['readyInMinutes'])+"\t"+str(dictWholeInformation['healthScore'])+"\n")

    def readNormalFile(self):
        file = open('przepisy.txt', 'r', encoding="utf8")
        for line in file:
            elem=line.split('\t')
            print(elem[0])

    def getSavedList(self):
        file = open('przepisy.txt', 'r', encoding="utf8")
        list=[]
        for line in file:
            elem = line.split('\t')
            list.append({elem[1]:elem[0]})
        return list

    def getTheHealthiestSavedRecepie(self):
        file = open('przepisy.txt', 'r', encoding="utf8")
        currentBestHealthy=0
        bestTitle=None
        for line in file:
            elem = line.split('\t')
            if currentBestHealthy<float(elem[3]):
                currentBestHealthy=float(elem[3])
                bestTitle=elem[1]
        return bestTitle

    def getTheQuickestSavedRecepie(self):
        file=open('przepisy.txt', 'r', encoding="utf8")
        currentBest = 10000000
        bestTitle=None
        for line in file:
            elem = line.split('\t')
            if currentBest > int(elem[2]):
                currentBest = int(elem[2])
                bestTitle=elem[1]
        return bestTitle

    def getLastSaved(self):
        with open('przepisy.txt', 'r', encoding="utf8") as file:
            first_line = file.readline()
            for last_line in file:
                pass

            elem=last_line.split('\t')
            title=elem[1]
        return title


if __name__ == '__main__':
    functionality=Functionality()
    #functionality.chooseDiet('')
    #print(functionality.finalUrlQuestion)
    #print(functionality.chooseCuisine('French'))
    #print(functionality.finalUrlQuestion)
    #functionality.howManyRecepies(10)
    #(functionality.getRecepiesListDict())
    #print(functionality.getRecepieListDict())
    #print(functionality.getRecepieDictById(638002))
    #(functionality.saveToFileDictIdMinutesHowhealty(716429))
    #print(functionality.openPickle())

    #functionality.readNormalFile()
    # print(functionality.getTheHealthiestRecepie())
    # print(functionality.getTheQuickestRecepie())
    #print(functionality.getSavedList())
    #functionality.chooseCuisine("italian")
    #print(functionality.finalUrlQuestion)
    #print(functionality.getLastSaved())
    print(functionality.getRecepieStepsAnalyzedById(638002))


