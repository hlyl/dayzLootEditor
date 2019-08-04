from tkinter import *

import dao
import windows
from categories import traderCatSwitcher
from exportTrader import createTrader


class TraderEditor(object):
    def __init__(self, root):
        self.window = Toplevel(root)
        self.window.wm_title("Trader")
        self.window.grab_set()

        self.traderVal = []

        self.main = Frame(self.window)
        self.main.grid()

        self.createSubTypes()
        self.createTraderEditor(self.window, 0, 1, [])
        self.createTraderSetting(self.window, 1, 1)
        self.subTypeListbox.bind("<<ListboxSelect>>", self.fillTraderWindow)

        windows.center(self.window)

    def createSubTypes(self):
        subtypesFrame = Frame(self.main)
        subtypesFrame.grid()
        self.subTypeListbox = Listbox(subtypesFrame, width=35, height=30, exportselection=False)
        self.subTypeListbox.grid(sticky="ns")
        subTypes = dao.getSubtypes()
        for subType in sorted(subTypes):
            if subType == "":
                subType = "UNASSIGNED"
            self.subTypeListbox.insert(END, subType)

    def createTraderEditor(self, root, row, column, rows):
        self.drawEditor(root, row, column, self.setTraderCat(rows))

    def setTraderCat(self, rows):
        for i in range(len(rows)):
            if rows[i][2] == "":
                rows[i][2] = traderCatSwitcher(rows[i][1])

        return rows

    def drawEditor(self, root, row, column, rows):
        height = 480
        width = 400
        self.frame = Frame(root, height=height, width=width, bg="#EBEBEB")
        self.frame.grid(row=row, column=column, sticky="nw", pady=20)
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

        self.canv = Canvas(self.frame, height=height, width=width, bg="#EBEBEB")
        self.canv.grid(row=0, column=0, sticky="nsew")

        self.canvFrame = Frame(self.canv, height=height, width=width, bg="#EBEBEB")
        self.canv.create_window(0, 0, window=self.canvFrame, anchor='nw')

        for item in rows:
            self.traderRow(self.canvFrame, *item)

        scrl = Scrollbar(self.frame, orient=VERTICAL)
        scrl.config(command=self.canv.yview)
        self.canv.config(yscrollcommand=scrl.set)
        scrl.grid(row=0, column=1, sticky="ns")

        root.rowconfigure(row, weight=1)
        root.columnconfigure(column, weight=1)

        self.canvFrame.bind("<Configure>", self.update_scrollregion)

    def createTraderSetting(self, root, row, column):
        radioFrame = Frame(root)
        radioFrame.grid(row=row, column=column, sticky="w", pady=5)

        MODES = [("Use Rarity", "rar"), ("Use Nominal", "nom")]
        self.v = StringVar()
        self.v.set("rar")

        Radiobutton(radioFrame, text=MODES[0][0], variable=self.v, value=MODES[0][1]).grid(row=0, column=0)
        Radiobutton(radioFrame, text=MODES[1][0], variable=self.v, value=MODES[1][1]).grid(row=0, column=1)

        frame = Frame(root)
        frame.grid(row=row+1, column=column, sticky="w", pady=5)

        self.createPriceBlock(frame, "Buy Price", 0, 0)
        self.createPriceBlock(frame, "Sell Price", 0, 1)
        buttonFrame = Frame(root)
        buttonFrame.grid(row=row+2, column=column, sticky="w", pady=5)

        Button(buttonFrame, text="Update Changes", command=self.update).grid(row=0, column=0)
        Button(buttonFrame, text="Copy to Clipboard", command=self.createTrader).grid(row=0, column=1, padx=5)

    def createPriceBlock(self, parent, name, row, column):
        buyPrice = LabelFrame(parent, text=name)
        buyPrice.grid(row=row, column=column, padx=10)

        self.createLabel(buyPrice, "Minimal:", 0, 0, "w")
        self.createLabel(buyPrice, "Maximal:", 1, 0, "w")
        self.min = IntVar()
        self.min.set(0)
        Entry(buyPrice, textvariable=self.min).grid(row=0, column=1, padx=5, pady=5)
        self.max = IntVar()
        self.max.set(0)
        Entry(buyPrice, textvariable=self.max).grid(row=1, column=1, padx=5, pady=5)

    def update_scrollregion(self, event):
        self.canv.configure(scrollregion=self.canv.bbox("all"))

    def traderRow(self, parent, name, subtype, traderCat, buyPrice, sellPrice, rarity, nominal, exclude):
        frame = Frame(parent)
        frame.grid(padx=10, pady=10, sticky="w")

        doExclude = IntVar()
        doExclude.set(exclude)

        nameVar = StringVar()
        nameVar.set(name)

        traderCatVar = StringVar()
        traderCatVar.set(traderCat)

        buyPriceVar = StringVar()
        buyPriceVar.set(buyPrice)

        sellPriceVar = StringVar()
        sellPriceVar.set(sellPrice)

        xpad = 10

        Checkbutton(frame, variable=doExclude).grid(row=0, column=0)
        nameEntry = Entry(frame, textvariable=nameVar, width=25)
        nameEntry.grid(row=0, column=1, padx=xpad)
        traderCatEntry = Entry(frame, textvariable=traderCatVar, width=3)
        traderCatEntry.grid(row=0, column=2, padx=xpad)
        buyPriceEntry = Entry(frame, textvariable=buyPriceVar, width=8)
        buyPriceEntry.grid(row=0, column=3, padx=xpad)
        sellPriceEntry = Entry(frame, textvariable=sellPriceVar, width=8)
        sellPriceEntry.grid(row=0, column=4, padx=xpad)

        self.traderVal.append(([traderCatEntry, buyPriceEntry, sellPriceEntry, doExclude], [rarity, name]))

    def clearTraderWindow(self):
        self.frame.grid_forget()

        self.traderVal = []

    def fillTraderWindow(self, event):
        self.clearTraderWindow()
        selSubtype = self.subTypeListbox.get(ANCHOR)
        selSubtype = "" if selSubtype == "UNASSIGNED" else selSubtype

        itemsOfSubtype = dao.getSubtypeForTrader(selSubtype)

        self.createTraderEditor(self.window, 0, 1, itemsOfSubtype)

    def createLabel(self, root, text, row, column, sticky="w", px=5, py=5):
        Label(root, text=text).grid(row=row, column=column, sticky=sticky, padx=px, pady=py)

    # traderCat, buyprice, sellprice, traderExclude, rarity, name
    def createValues(self):
        values = []
        for i in range(len(self.traderVal)):
            item = []
            for entry in self.traderVal[i][0]:
                item.append(entry.get())
            item.append(self.traderVal[i][1][-2])
            item.append(self.traderVal[i][1][-1])
            values.append(item)
        return values

    def update(self):
        values = self.createValues()
        dao.setSubtypeForTrader(values)

    def createTrader(self):
        subtype = self.subTypeListbox.get(ANCHOR)
        items = self.createValues()
        newItems = []
        for item in items:
            newItem = [item[5], item[0], item[1], item[2], item[3]]
            newItems.append(newItem)
        # name, traderCat, buyPrice, sellPrice
        createTrader(self.window, subtype, newItems)


def testWindow():
    window = Tk()
    TraderEditor(window)
    window.mainloop()
