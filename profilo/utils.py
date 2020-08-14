import adsk.core, adsk.fusion, adsk.cam, traceback,os
import math

_grname="ago"

def toint(n):
  try:
    return int(n)
  except:
    return 0


def todegstr(ang):
    return str(int(math.degrees(ang)*10)/10)


def getattr(design,name,defval):
    global _grname
    tm = design.attributes.itemByName(_grname, name)            
    if tm:
        return tm.value
    else:
        return defval

def setattr(design,name,value):
    design.attributes.add(_grname,name,value)

def getCommandInputValue(commandInput, unitType):
    try:
        valCommandInput = adsk.core.ValueCommandInput.cast(commandInput)
        if not valCommandInput:
            return (False, 0)

        # Verify that the expression is valid.
        design = adsk.fusion.Design.cast(_app.activeProduct)
        unitsMgr = design.unitsManager
        
        if unitsMgr.isValidExpression(valCommandInput.expression, unitType):
            value = unitsMgr.evaluateExpression(valCommandInput.expression, unitType)
            return (True, value)
        else:
            return (False, 0)
    except:
        if _ui:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
