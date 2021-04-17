import urllib3
import json, requests
from functionality import Functionality
import tkinter as tk
from tkinter import *
from urllib.request import urlopen, Request
import io
from PIL import Image, ImageTk
from tkinter import messagebox, filedialog, font


class ImageToShow:
    def __init__(self):
        self.image = None
        self.imageIconPath = 'icons/ok_image.png'


image_to_show = ImageToShow()


class MainGui():
    def __init__(self, root):
        self.root = root
        root.title('Recepie application')

        root.geometry("450x400")
        myFont = font.Font(size=30)
        Grid.columnconfigure(root, 0, weight=1)
        Grid.columnconfigure(root, 1, weight=1, minsize=200)
        ##################################
        self.dietLebel = Label(root, text="Your recepie")
        self.dietLebel['font'] = myFont
        self.dietLebel.grid(column=0, row=0, sticky="e", padx=(5, 0), pady=(0, 10))

        self.imgOk = PhotoImage(file=r'icons/ok-icon.png')
        self.labelWithImage = Label(root, image=self.imgOk)
        self.labelWithImage.grid(column=1, row=0, sticky="w", padx=(0, 5), pady=(0, 10))

        self.dietLebel = Label(root, text="Choose your diet:")
        self.dietLebel.grid(column=0, row=1, sticky="w", padx=(5, 0))

        self.clickedDiet = StringVar()
        self.clickedDiet.set("none")
        self.dietChoose = OptionMenu(root, self.clickedDiet, "none", "paleo", "vegetarian", "katogenic", "vegan",
                                     "pescetarian",
                                     "primal").grid(row=2, column=0, columnspan=2, padx=5, sticky='we')

        self.cusineLabel = Label(root, text="Choose cuisine:")
        self.cusineLabel.grid(column=0, row=3, sticky="w", padx=(5, 0))
        self.clickedCuisine = StringVar()
        self.clickedCuisine.set("none")
        self.cuisineChoose = OptionMenu(root, self.clickedCuisine, "none", "chinese", "greek", "irish", "thai",
                                        "british",
                                        "mexican").grid(row=4,
                                                        column=0,
                                                        columnspan=2,
                                                        sticky='we', padx=5)
        self.intoleranceLabel = Label(root, text="Intolerances:")
        self.intoleranceLabel.grid(row=5, column=0, sticky="w", padx=(5, 0))

        self.ifNuts = StringVar()
        self.ifEggs = StringVar()
        self.ifGluten = StringVar()
        self.ifDairy = StringVar()
        self.ifGrain = StringVar()
        self.ifSeafood = StringVar()
        self.checkbox1 = Checkbutton(root, text="Nuts", variable=self.ifNuts, onvalue=",+nuts", offvalue="")
        self.checkbox1.grid(row=6, column=0, sticky="w", padx=(5, 0))

        self.checkbox2 = Checkbutton(root, text="Egg", variable=self.ifEggs, onvalue=",+egg", offvalue="")
        self.checkbox2.grid(row=7, column=0, sticky="w", padx=(5, 0))

        self.checkbox3 = Checkbutton(root, text="Gluten", variable=self.ifGluten, onvalue=",+gluten", offvalue="")
        self.checkbox3.grid(row=6, column=1, sticky="w")

        self.checkbox4 = Checkbutton(root, text="Dairy", variable=self.ifDairy, onvalue=",+dairy", offvalue="")
        self.checkbox4.grid(row=7, column=1, sticky="w")

        self.checkbox5 = Checkbutton(root, text="Grain", variable=self.ifGrain, onvalue=",+grain", offvalue="")
        self.checkbox5.grid(row=8, column=0, sticky="w", padx=(5, 0))

        self.checkbox6 = Checkbutton(root, text="Seafood", variable=self.ifSeafood, onvalue=",+seafood", offvalue="")
        self.checkbox6.grid(row=8, column=1, sticky="w")

        self.timeLabel = Label(root, text="Max time of cooking (in minutes):")
        self.timeLabel.grid(column=0, row=9, sticky="w", padx=(5, 0))
        self.timeEntry = Entry(root)
        self.timeEntry.grid(column=1, row=9, sticky="we", padx=(0, 5))

        self.foodLabel = Label(root, text="What would you like to eat?:")
        self.foodLabel.grid(column=0, row=10, sticky="w", padx=(5, 0))
        self.foodEntry = Entry(root)
        self.foodEntry.grid(column=1, row=10, sticky="we", padx=(0, 5))

        self.numberLabel = Label(root, text="How many recepies?:")
        self.numberLabel.grid(column=0, row=11, sticky="w", padx=(5, 0))
        self.numberEntry = Entry(root)
        self.numberEntry.grid(column=1, row=11, sticky="we", padx=(0, 5))

        def processData():
            functionality = Functionality()

            intolerances = self.ifNuts.get() + self.ifEggs.get() + self.ifGluten.get() + self.ifDairy.get() + self.ifGrain.get() + self.ifSeafood.get()

            if self.clickedDiet.get() == 'none':
                diet = ''
            else:
                diet = self.clickedDiet.get()
            if self.clickedCuisine.get() == 'none':
                cuisine = ''
            else:
                cuisine = self.clickedCuisine.get()
            intolerance = intolerances
            time = self.timeEntry.get()
            food = self.foodEntry.get()
            number = self.numberEntry.get()

            functionality.chooseDiet(diet)
            functionality.chooseCuisine(cuisine)
            functionality.searchByIntolerance(intolerance)
            functionality.searchMaxCookingTime(time)
            functionality.howManyRecepies(number)
            functionality.serchWhatToEat(food)
            resultBox = functionality.getRecepieList()

            if not resultBox:
                messagebox.showinfo("Sorry", "Sorry we do not have this kind of recepies, try different combination")

            else:
                windowList = tk.Toplevel()
                windowList.geometry("400x300")

                frameTitle = Frame(windowList, width=400, height=50)
                frameTitle.pack()
                ######################
                myFont = font.Font(size=20)

                foundRecepiesLabel = Label(frameTitle, text="Found recepies:")
                foundRecepiesLabel['font'] = myFont
                foundRecepiesLabel.grid(column=0, row=0, columnspan=2, sticky="we", padx=(5, 0), pady=(0, 5))


                ############################
                frameListBox = Frame(windowList, width=400, height=0)

                scrollbar = Scrollbar(frameListBox, orient="vertical")

                listBox = Listbox(frameListBox, yscrollcommand=scrollbar.set)
                scrollbar.pack(side=RIGHT, fill=Y)
                frameListBox.pack()
                listBox.pack()
                #############################
                # listBox=Listbox(windowList)
                # listBox.pack()

                dictListRowId = []
                max_len = 0
                for elem in functionality.getRecepieListDict():
                    for idElem, titleElem in elem.items():
                        listBox.insert(END, idElem)
                        index = listBox.get(0, END).index(idElem)
                        dictListRowId.append({str(index): (str(idElem), titleElem)})
                        if len(idElem) > max_len:
                            max_len = len(idElem)

                listBox.configure(width=max_len)
                scrollbar.config(command=listBox.yview)

                def getIdSelectedItem():
                    name = listBox.get(listBox.curselection())
                    id_item = None
                    for elem in dictListRowId:
                        for elementList, value in elem.items():
                            if value[0] == name:
                                id_item = value[1]
                    openRecepieWindow(id_item)

                frameButtons=Frame(windowList)
                frameButtons.pack()
                buttonGoToRecepie = Button(frameButtons, text="select", command=getIdSelectedItem)
                buttonGoToRecepie.grid(column=0, row=0)
                buttonHelpList= Button(frameButtons, text="help", command=openHelpForListBox)
                buttonHelpList.grid(column=1, row=0)

                label = Label(windowList, text='')
                label.pack()

        buttonShowRecepies = Button(root, text="get recepies", command=processData)
        buttonShowRecepies.grid(column=1, row=12, sticky="we", padx=(0, 5), pady=(2, 0))

        buttonSavedRecepies = Button(root, text="get saved recepies", command=showRecepiesSaved)
        buttonSavedRecepies.grid(column=0, row=12, sticky="we", padx=(5, 0), pady=(2, 0))

        buttonHelp = Button(root, text="help", command=openHelp)
        buttonHelp.grid(column=1, row=13, padx=(0, 5), sticky="we", pady=(2, 0))


def showRecepiesSaved():
    functionality=Functionality()
    windowSaved=tk.Toplevel()
    windowSaved.geometry('400x300')

    frameTitle = Frame(windowSaved, width=400, height=50)
    frameTitle.pack()
    ######################
    myFont = font.Font(size=20)

    savedLebel = Label(frameTitle, text="Your saved recepies:")
    savedLebel['font'] = myFont
    savedLebel.grid(column=0, row=0, columnspan=2,sticky="we", padx=(5, 5), pady=(0, 10))

    ######################
    frameListBox=Frame(windowSaved, width=400, height=0)

    scrollbar = Scrollbar(frameListBox, orient="vertical")

    listBox = Listbox(frameListBox, yscrollcommand = scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)
    frameListBox.pack()
    listBox.pack()

    dictListRowId = []
    max_len=0
    for elem in functionality.getSavedList():
        for idElem, titleElem in elem.items():
            listBox.insert(END, idElem)
            index = listBox.get(0, END).index(idElem)
            dictListRowId.append({str(index): (str(idElem), titleElem)})
            if len(idElem)>max_len:
                max_len=len(idElem)

    listBox.configure(width=max_len)
    scrollbar.config(command=listBox.yview)

    def getIdSelectedItem():
        name = listBox.get(listBox.curselection())
        id_item = None
        for elem in dictListRowId:
            for elementList, value in elem.items():
                if value[0] == name:
                    id_item = value[1]
        openRecepieWindow(id_item)


    frameForInformation=Frame(windowSaved)
    frameForInformation.pack()

    buttonChose = Button(frameForInformation, text="select", command=getIdSelectedItem)
    buttonChose.grid(column=2, row=0, sticky='we')

    buttonHelp = Button(frameForInformation, text="help", command=openHelpForSavedWindow)
    buttonHelp.grid(column=3, row=0, sticky='we')

    labelInfo=Label(frameForInformation, text="Get the name of recepie : ")
    labelInfo.grid(column=0, row=1)

    recepieWanted = StringVar()
    labelRecepie = Label(frameForInformation, textvariable=recepieWanted).grid(column=0, row=2, columnspan=4)

    def guickLabelUpdate():
        recepieWanted.set(functionality.getTheQuickestSavedRecepie())
    def healthyLabelUpdate():
        recepieWanted.set(functionality.getTheHealthiestSavedRecepie())
    def lastLabelUpdate():
        recepieWanted.set(functionality.getLastSaved())

    buttonTime=Button(frameForInformation, text="the quickest", command=guickLabelUpdate).grid(column=1, row=1)
    buttonHealty=Button(frameForInformation, text="the healthiest", command=healthyLabelUpdate).grid(column=2, row=1)
    buttonLast=Button(frameForInformation, text="the last added", command=lastLabelUpdate).grid(column=3, row=1)

    windowSaved.mainloop()

def openNutritionRecepie(id):
    nutritionWindow = tk.Toplevel()

    myFont = font.Font(size=30)
    labelTitleNutrition = Label(nutritionWindow, text="Nutrition")
    labelTitleNutrition['font'] = myFont
    labelTitleNutrition.grid(row=0, column=0, sticky='we', padx=10)


    functionality = Functionality()
    nutritientsTuple = functionality.getRecepieNutritionDictById(id)  # tuple(bad, good)  do tupli kuła jak do listy[1]
    bad = nutritientsTuple[0]
    listOfBad = []
    for everyDict in bad:
        listOfBad.append(
            everyDict['title'] + ": " + str(everyDict['amount']) + ", daily percent need: " + str(
                everyDict['percentOfDailyNeeds']) + "%")
    good = nutritientsTuple[1]
    for everyDict in good:
        listOfBad.append(
            everyDict['title'] + ": " + str(everyDict['amount']) + ", daily percent need: " + str(
                everyDict['percentOfDailyNeeds']) + "%")
    separator = '\n'
    ingredients = separator.join(listOfBad)
    ingredientsLabel = Label(nutritionWindow, text=ingredients)
    ingredientsLabel.grid(column=0, row=1, sticky="we", padx=10)
    nutritionWindow.title("Nutrition")
    nutritionWindow.mainloop()

def openSummaryRecepie(id):
    summaryWindow = tk.Toplevel()
    functionality = Functionality()

    titleLabel = Label(summaryWindow, text="Summary:")
    titleLabel.config(font=("Courier", 30))
    titleLabel.pack(padx=5, pady=5)

    listSummary = functionality.getRecepieDictSummaryById(id)
    listSummaryToPrint = listSummary.replace("<b>", " ").replace("</b>", " ")
    newString = re.sub('<[^>]+>', '', listSummaryToPrint)
    summaryLabel = Label(summaryWindow, text=newString, wraplength=400)
    summaryLabel.pack(fill=BOTH, expand=1, padx=15, pady=(0, 15))
    summaryWindow.title("Summary")
    summaryWindow.mainloop()


def openHelp():
    winowHelp = tk.Toplevel()
    titleLabel = Label(winowHelp, text="Help")
    titleLabel.config(font=15)
    titleLabel.grid(column=0, row=0, padx=5, pady=5, sticky='w')

    firstParagraphLabel = Label(winowHelp, text=" This app is made to find the best recepie for you.")
    firstParagraphLabel.grid(row=1, column=0, padx=5, pady=10, sticky='w')

    secondParagraphLabel = Label(winowHelp,
                                 text="In first window you can choose your diet, cuisine, intolerances, maximum time of prepering dish, how many recepies you want and kind of food you want",
                                 wraplength=400)
    secondParagraphLabel.grid(row=2, column=0, padx=5, pady=10, sticky='w')

    firstInputLabel = Label(winowHelp,
                            text="If you want to choose diet, click on drop-down list under the words 'Choose your diet', you will see list of available diets. If you do not want any diet leave 'none'",
                            wraplength=400)
    firstInputLabel.grid(row=3, column=0, padx=5, pady=10, sticky='w')

    secondInputLabel = Label(winowHelp,
                             text="If you want to choose cuisine, click on drop-down list under the words 'Choose cuisine', you will see kind of available diets. If you do not want any diet leave 'none'",
                             wraplength=400)
    secondInputLabel.grid(row=3, column=0, padx=5, pady=10, sticky='w')

    thirdInputLabel = Label(winowHelp,
                            text="If you have any food intolerances, select them by clicking. Recepies will not include any of them",
                            wraplength=400)
    thirdInputLabel.grid(row=4, column=0, padx=5, pady=10, sticky='w')

    fourthInputLabel = Label(winowHelp,
                             text="If you want to set time of cooking fill the box next to word 'max time of cooking'",
                             wraplength=400)
    fourthInputLabel.grid(row=5, column=0, padx=5, pady=10, sticky='w')

    fifthInputLabel = Label(winowHelp,
                            text="If you know what would you like to eat you can write it in next box for example: chicken, soup",
                            wraplength=400)
    fifthInputLabel.grid(row=6, column=0, padx=5, pady=10, sticky='w')

    sixthInputLabel = Label(winowHelp,
                            text="You can set how many recepis you want in last input",
                            wraplength=400)
    sixthInputLabel.grid(row=7, column=0, padx=5, pady=10, sticky='w')

    informationLabel = Label(winowHelp,
                             text="IMPORTANT!\nThis app has limited list of recepies if your search is too complex the list might be shortened or will not appear, try to change your preferences then",
                             wraplength=400)
    informationLabel.grid(row=8, column=0, padx=5, pady=10, sticky='w')

def openHelpForListBox():
    winowHelp = tk.Toplevel()
    titleLabel = Label(winowHelp, text="Help")
    titleLabel.config(font=15)
    titleLabel.grid(column=0, row=0, padx=5, pady=5, sticky='w')

    whatToDoLabel = Label(winowHelp,
                          text="This window has your every recepie according to your preferences. If you want to open recepie, click on which you want and click button 'select'",
                          wraplength=250)
    whatToDoLabel.grid(column=0, row=1, padx=5, pady=5, sticky='w')

def openHelpForRecepieWindow():
    winowHelp = tk.Toplevel()
    titleLabel = Label(winowHelp, text="Help")
    titleLabel.config(font=15)
    titleLabel.grid(column=0, row=0, padx=5, pady=5, sticky='w')

    whatToDoLabel = Label(winowHelp,
                          text="In this window you see a recepie, you can save it by clicking on 'save recepie', then you can see it by clicking in first window in button 'get saved recepies'.\n If you click nutrition you will see window with nutrition for this recepie. By clicking in summary you will see summary of this recepie.",
                          wraplength=250)
    whatToDoLabel.grid(column=0, row=1, padx=5, pady=5, sticky='w')


def openHelpForSavedWindow():
    winowHelp = tk.Toplevel()
    titleLabel = Label(winowHelp, text="Help")
    titleLabel.config(font=15)
    titleLabel.grid(column=0, row=0, padx=5, pady=5, sticky='w')

    whatToDoLabel = Label(winowHelp,
                          text="This window has your every saved recepie. If you want to open recepie, click on which you want and click button 'select'",
                          wraplength=400)
    whatToDoLabel.grid(column=0, row=1, padx=5, pady=5, sticky='w')

    informationLabel = Label(winowHelp,
                             text="Next buttons are made to show you the title of your saved the quickest or the healtiest or last saved recepie. The title of recepie will occure right under the buttons"
                             , wraplength=400)
    informationLabel.grid(column=0, row=2, padx=5, pady=5, sticky='w')


def openRecepieWindow(id):
    windowRecepie = tk.Toplevel()
    functionality = Functionality()

    Grid.columnconfigure(windowRecepie, 0, weight=1)
    Grid.columnconfigure(windowRecepie, 1, weight=1)
    frameLeft = Frame(windowRecepie)
    frameLeft.grid(row=2, column=0)

    title = Label(frameLeft, text=functionality.getRecepieTitleById(id),  wraplength=300)
    title.config(font=( 15))
    title.grid(column=0, row=0, padx=(10, 5), pady=5, sticky='we')

    titleLabelFrameLeft = Label(frameLeft, text="Ingredients:", wraplength=300)
    titleLabelFrameLeft.config(font= 12)
    titleLabelFrameLeft.grid(column=0, row=1, padx=(10,5), pady=5, sticky='we')
    #
    frameRight = Frame(windowRecepie)
    frameRight.grid(row=2, column=1, padx=(10,5), pady=5)

    list = functionality.getRecepieIngredientsById(id)

    separator = '\n'
    ingredients = separator.join(list)
    ingredientsLabel = Label(frameLeft, text=ingredients, wraplength=300)
    ingredientsLabel.grid(column=0, row=2, padx=5, pady=5, sticky='w')

    frameBottom = Frame(windowRecepie, width=450, height=200)
    frameBottom.grid(row=3, column=0, columnspan=2)
    titleLabelFrameBottom = Label(frameBottom, text="Instructions:")
    titleLabelFrameBottom.config(font=12)
    titleLabelFrameBottom.grid(column=0, columnspan=2, row=0, padx=10, pady=(5, 15), sticky='we')

    listSummary = functionality.getRecepieStepsAnalyzedById(id)
    separator = ''
    steps = separator.join(listSummary)
    instructionsLabel = Label(frameBottom, text=steps, wraplength=500)
    instructionsLabel.grid(column=0, columnspan=2, row=1, padx=5, pady=5, stick='we')

    ####################

    imageRecepie = functionality.getRecepieImageAdresById(id)
    displayImages(imageRecepie, frameRight, 200, 200)

    ####################

    def saveAndInform(id):
        messagebox.showinfo("Information", "New record saved")
        functionality.saveToNormalFile(id)

    toolbar = Frame(windowRecepie, bd=1, relief=RAISED)
    toolbar.config(bg="beige")

    buttonSaveQuestion = Button(toolbar, text="Summary",
                                command=lambda: openSummaryRecepie(id))  # , command=lambda: openSummaryRecepie(id)
    buttonSaveQuestion.pack(side=tk.LEFT, padx=2, pady=2)
    buttonManageQuestions = Button(toolbar, text="Nutrition", command=lambda: openNutritionRecepie(
        id))  # , command=lambda: openNutritionRecepie(id)
    buttonManageQuestions.pack(side=tk.LEFT, padx=2, pady=2)
    buttonShowQuestions = Button(toolbar, text="Save Recepie", command=lambda: saveAndInform(id))
    buttonShowQuestions.pack(side=tk.LEFT, padx=2, pady=2)
    buttonHelp=Button(toolbar, text="help", command=openHelpForRecepieWindow)
    buttonHelp.pack(side=tk.LEFT, padx=2, pady=2)
    buttonExit = Button(toolbar, text="Exit application", command=windowRecepie.quit)
    buttonExit.pack(side=tk.LEFT, padx=2, pady=2)

    toolbar.grid(column=0, columnspan=2, row=0, sticky="we", pady=(0, 5))

    windowRecepie.title("Choosen Recepie")
    #windowRecepie.geometry("600x500")


def displayImages(url_request_image, root, destination_image_box_height, destination_image_box_width):
    request = Request(url_request_image, headers={'User-Agent': 'Mozilla/5.0'})
    image_bytes = urlopen(request).read()
    data_stream = io.BytesIO(image_bytes)

    pil_image = Image.open(data_stream)

    original_image_width, original_image_height = pil_image.size

    pil_image_resized = resize(original_image_width, original_image_height, destination_image_box_width,
                               destination_image_box_height,
                               pil_image)

    # Convert PIL image object to Tkinter's PhotoImage object
    image_to_show.image = ImageTk.PhotoImage(pil_image_resized)

    # fill frame with image
    wiki_image_canvas = tk.Label(root, image=image_to_show.image, width=destination_image_box_width,
                                 height=destination_image_box_height)
    wiki_image_canvas.configure(background="white")
    wiki_image_canvas.pack(padx=5, pady=5)


def resize(original_image_width, original_image_height, destination_image_box_width, destination_image_box_height,
           pil_image):
    f1 = 1.0 * destination_image_box_width / original_image_width
    f2 = 1.0 * destination_image_box_height / original_image_height
    factor = min([f1, f2])
    new_image_width = int(original_image_width * factor)
    new_image_height = int(original_image_height * factor)
    return pil_image.resize((new_image_width, new_image_height), Image.ANTIALIAS)




if __name__ == '__main__':
    root = Tk()
    my_gui = MainGui(root)
    root.mainloop()
