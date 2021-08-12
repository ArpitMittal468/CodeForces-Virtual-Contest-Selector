import tkinter as tk
import requests
import json
import threading

response = None
isResponeFetched = False
userFetchedData = {}
lst = []

file = open('./Data/defaultListSize.txt', 'r')
listSize = int(file.readline().strip())
file.close()
del file

def clearLogBox():
    logBox.delete('1.0', "end")

def clearOutPutBox():
    outputBox.delete('1.0', 'end')

def outputLog(string):
    clearLogBox()
    logBox.insert(tk.END, ">> "+string)


def outputResult(string):
    outputBox.insert(tk.END, string)


def contestByUser(User):
    outputLog(f"Fetching {User} Data.\n")
    if User not in userFetchedData:
        apiCallLink = f'https://codeforces.com/api/user.status?handle={User}'
        response = requests.get(apiCallLink).json()
        if response['status'] == "FAILED":
            outputLog("Load Failed\n")
            return
        
        result = response
        consetProblems = set()

        for i in result['result']:
            constestId = i['contestId']
            verdict = i['verdict']

            if verdict == 'OK':
                consetProblems.add(constestId)

        userFetchedData[User] = consetProblems.copy()

    outputLog("Load Succesfull\n")



def notGivenContest(listSize):
    global response, isResponeFetched
    st = []
    showingFor = []

    clearOutPutBox()

    for i in lst:
        if i in userFetchedData:
            st.append(userFetchedData[i])
            showingFor.append(i)
    
    
    if not isResponeFetched:
        outputLog('Loading Codeforces Contest.\n')
        response = requests.get('https://codeforces.com/api/contest.list').json()
        if response['status'] == "OK":
            isResponeFetched = True
            outputLog("Load Succesfull\n")
            contestList = []
            for i in response['result']:
                if i['phase'] == "FINISHED":
                    contestList.append({'id': i['id'], 'name': i['name']})
            response['result'] = contestList
        else:
            outputLog("Load Failed\n")
            return 
    

    j = True
    
    filt = filterBox.get('1.0', 'end').strip().lower()
    
    outputLog("Showing Result For: " +  str(showingFor)+"\n" + "Filter By: '" + filt + "'\n")

    for i in response['result']:
        if listSize  == 0:
            break
        can = True

        for k in st:
            can = can and i['id'] not in k
        
        if can and filt in i['name'].lower():
            ans = ">> " + i['name'] + "\n" + f"   https://codeforces.com/contest/{i['id']}\n\n\n"

            outputResult(ans)
            j = False
            listSize -= 1
    if j:
        outputResult("No Result Found")


def startProcess():
    global lst
    lst = handlesInputBox.get('1.0', tk.END).strip().split('\n')
    print(lst)
    
    if '' in lst:
        lst.remove('')

    if len(lst) == 0:
        outputLog("Empty User Handles.\n")
        return 
    

    for i in lst:
        contestByUser(i)
    
    filterBox.delete('1.0', 'end')
    filterBox.configure(state = 'disabled')
    
    notGivenContest(listSize)
    
    filterBox.configure(state = 'normal')


def findByFilter(x):
    threading.Thread(target=notGivenContest, args=[listSize], daemon=True).start()


def findClicked():
    threading.Thread(target=startProcess, daemon=True).start()


if __name__ == "__main__":
    mainWindow = tk.Tk()
    mainWindow.title("Virtual Contest Selector")
    mainWindow.geometry("1180x620")
    mainWindow.wm_iconbitmap('./Data/icon.ico')

    mainWindow.resizable(False, False)

    backgroundImage = tk.PhotoImage(file = "./Data/bg2.png")
    background = tk.Label(mainWindow, text="Hello", image = backgroundImage)
    background.place(x = 0, y = 0, relheight=1, relwidth=1)

    handlesInputBox = tk.Text(background, padx = 5, pady = 5, bd = 5, relief = tk.GROOVE, font = ('Courier',13, 'bold'))
    handlesInputBox.place(x = 60, y = 50, relheight = 0.4, relwidth = 0.3)

    handlesHeader = tk.Label(mainWindow, text= "USER HANDLES:", relief = tk.FLAT, font = ('Courier',10, 'bold'), bg = "#d3e4f5")
    handlesHeader.place(x = 55, y = 30, relheight = 0.03, relwidth = 0.1)

    logBox = tk.Text(background, padx = 5, pady = 5, bd = 5, relief = tk.GROOVE, bg = "black", fg = "white", font = ('Courier',10, 'bold'))
    logBox.place(y = 330 ,x = 60, relheight = 0.4, relwidth = 0.3)

    logHeader = tk.Label(mainWindow, text= "LOG WINDOW:", relief = tk.FLAT, font = ('Courier',10, 'bold'),  bg = "#b7d2ef")
    logHeader.place(y = 310 ,x = 45, relheight = 0.03, relwidth = 0.1)

    outputBox = tk.Text(background, padx = 5, pady = 5, bd = 5, relief = tk.GROOVE, font = ('Courier',12, 'bold'))
    outputBox.place(y = 50 ,x = 500, relheight = 0.7, relwidth = 0.5)

    outputHeader = tk.Label(mainWindow, text= "RESULT:", relief = tk.FLAT, font = ('Courier',10, 'bold'), bg = "#d3e4f5")
    outputHeader.place(y = 30 ,x = 470, relheight = 0.03, relwidth = 0.1)

    searchButton = tk.Button(mainWindow, text = "LOAD DATA", command = findClicked, font = ('Courier',10, 'bold'))
    searchButton.place(x = 500, y = 520, relheight = 0.1, relwidth = 0.1)

    filterBox = tk.Text(background, padx = 5, pady = 5, bd = 5, relief = tk.GROOVE, font = ('Courier',13, 'bold'))
    filterBox.place(y = 520 ,x = 700, relheight = 0.1, relwidth = 0.3)
    filterBox.configure(state = 'disabled')
    filterBox.bind('<Key>', func= findByFilter)

    filterHeader = tk.Label(mainWindow, text= "FILTER BY:", relief = tk.FLAT, font = ('Courier',10, 'bold'), bg = "#b7d2ef")
    filterHeader.place(y = 500 ,x = 685, relheight = 0.03, relwidth = 0.1)

    mainWindow.mainloop()