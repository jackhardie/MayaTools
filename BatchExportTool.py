import pymel.core as pm
import os

selectList = None
newSelectionList = None
savePath = None
a_len = None
b_len = None
isRefresh = False


def main():
    global selectList
    global a_len
    selectList = pm.ls(sl=True)
    a_len = len(selectList)

    try:
        pm.deleteUI("ExportSelWindow")
    except Exception as e:
        print(e)

    UI = pm.window("ExportSelWindow", title="Batch Export", h=100, w=200)
    forLay = pm.formLayout()
    pText = pm.text(label="Export Path:")
    pTextF = pm.textField("ExportSelWindow")
    btnExport = pm.button(label="Export", c=exportCMD)
    btnFileDirection = pm.button(label="...", c=selectPath, w=30)
    btnCenter = pm.button(label="World Center", c=objCenter)
    btnDelHistory = pm.button(label="Delete History", c=delHistory)
    btnFreezeTransform = pm.button(label="Freeze Transform", c=objFreezeTransform)
    scrLay = pm.scrollLayout(w=250, h=120)

    for s in selectList:
        pm.nameField(o=s, w=280)

    pm.formLayout(

        forLay, e=True,
        attachForm=[
            (scrLay, "top", 5), (scrLay, "left", 5),
            (btnExport, "top", 5),
            (btnExport, "right", 5),
            (pText, "left", 5), (pText, "bottom", 5),
            (pTextF, "bottom", 5),
            (btnFileDirection, "bottom", 5), (btnFileDirection, "right", 5),
            (btnCenter, "top", 5), (btnCenter, "right", 5),
            (btnDelHistory, "right", 5),
            (btnFreezeTransform, "right", 5),
        ],
        attachControl=[
            (pTextF, "left", 3, pText), (pTextF, "right", 3, btnFileDirection),
            (btnExport, "left", 3, scrLay), (btnExport, "bottom", 3, btnFileDirection),
            (btnExport, "top", 3, btnFreezeTransform),
            (scrLay, "bottom", 3, pTextF),
            (btnCenter, "left", 3, scrLay),
            (btnDelHistory, "top", 3, btnCenter), (btnDelHistory, "left", 3, scrLay),
            (btnFreezeTransform, "top", 3, btnDelHistory), (btnFreezeTransform, "left", 3, scrLay),
        ]
    )

    pm.window(UI, e=True, w=400, h=100)
    pm.showWindow(UI)


def objCenter(*args):
    assets = pm.selected()
    for geo in assets:
        pos = pm.xform(geo, q=True, rp=True)
        v_pos = pm.dt.Vector(pos)
        pm.xform(geo, worldSpace=True, translation=-v_pos)


def delHistory(*args):
    selectList = pm.ls(sl=True)
    for s in selectList:
        pm.bakePartialHistory(selectList, query=True, prePostDeformers=True)
        pm.bakePartialHistory(selectList, prePostDeformers=True)
        pm.bakePartialHistory(selectList, preCache=True)


def objFreezeTransform(*args):
    selectList = pm.ls(sl=True)
    for obj in selectList:
        pm.makeIdentity(obj, apply=True, t=1, r=1, s=1, n=0)


def exportCMD(*args):
    global selectList
    global a_len
    selectList = pm.ls(sl=True)
    savePath = pm.textField("ExportSelWindow", q=True, text=True)
    msg = "Exported:\n    "
    if not savePath:
        pm.PopupError("Please assign the export path!")
        return
    for s in selectList:
        pm.select(s)
        print(s.name())
        filePath = savePath + "/" + s.name() + ".fbx"
        msg = msg + s.name() + "\n    "
        print(filePath)
        pm.exportSelected(filePath, force=True)
    pm.select(selectList)

    a = pm.confirmDialog(title="Finished", message=msg, button=["OK", "Open Folder"])
    if a == "Open Folder":
        os.startfile(savePath)


def selectPath(*args):
    global savePath
    savePath = pm.fileDialog2(fileFilter="*.folder", fileMode=2)

    if not savePath:
        pm.PopupError("Please assign the export path!")
        return
    if savePath:
        savePath = savePath[0]
    pm.textField("ExportSelWindow", e=True, text=savePath)


main()
