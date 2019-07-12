
import xmlParser
import dao
import windows


def orderModList(mods):
    for i in range(len(mods)):
        if mods[i] == "Vanilla":
            tmp = mods[0]
            mods[0] = "Vanilla"
            mods[i] = tmp

    return mods


def getXmlBlock(row):
    item = xmlParser.Item()
    item.fillFromVal(row)
    return item.getXML()


def update(dir, includedMods):
    includedMods = orderModList(includedMods)
    f = dir
    items = dao.getAllItems()
    f.write("<types>\n")
    print(includedMods)
    for mod in includedMods:
        f.write("  <!--{}--> \n".format(mod))
        for item in items:
            if item[-1] in mod:
                f.write(getXmlBlock(item))
    f.write("</types>\n")
