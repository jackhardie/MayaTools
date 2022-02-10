import maya.cmds as cmds

SUFFIXES = {
    "mesh": "geo",
    "joint": "jnt",
    "camera": None,
    "ambientLight": "lgt"
}

DEFAULT_SUFFIX = "grp"


def rename(selection=False):
    """
    This function will rename any objects to have the correct suffix
    Args:
        selection:whether or not we use the current selection

    Returns:
        A list of all the objects we operated on
    """
    # This function cannot run if there is no selection and no objects
    objects = cmds.ls(selection=selection, dag=True, long=True)

    if selection and not objects:
        raise RuntimeError("No object selected!")

    objects.sort(key=len, reverse=True)

    for obj in objects:
        shortName = obj.split("|")[-1]

        children = cmds.listRelatives(obj, children=True, fullPath=True) or []

        if len(children) == 1:
            child = children[0]
            objType = cmds.objectType(child)
        else:
            objType = cmds.objectType(obj)

        suffix = SUFFIXES.get(objType, DEFAULT_SUFFIX)

        if not suffix:
            continue

        if obj.endswith(suffix):
            continue

        newName = "%s_%s" % (shortName, suffix)

        cmds.rename(obj, newName)

        index = objects.index(obj)
        objects[index] = obj.replace(shortName, newName)

    return objects
