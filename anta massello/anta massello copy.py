#Author-
#Description-

# Author-aa
# Description-

import adsk.core
import adsk.fusion
import adsk.cam
import traceback
import os
import math
from .utils import *           # libreria comune ai vari script
# from .maniglie import *    # definizione dei profili
# Globals
_app = adsk.core.Application.cast(None)
_ui = adsk.core.UserInterface.cast(None)
_units = ''
_pos = 0
_alt = adsk.core.ValueCommandInput.cast(None)
_larg = adsk.core.ValueCommandInput.cast(None)
_sps = adsk.core.ValueCommandInput.cast(None)
_massello = adsk.core.ValueCommandInput.cast(None)
_pannello = adsk.core.ValueCommandInput.cast(None)
_cava = adsk.core.ValueCommandInput.cast(None)
_maniglia = adsk.core.DropDownCommandInput.cast(None)
_doppio = adsk.core.DropDownCommandInput.cast(None)


# _des = adsk.core.StringValueCommandInput.cast(None)
# _peso = adsk.core.TextBoxCommandInput.cast(None)
_errMessage = adsk.core.TextBoxCommandInput.cast(None)
_handlers = []
maniglie = {}


# ---------------------------- Loader -------------------------------------------------

def run(context):
    try:
        global _app, _ui, profili
        _app = adsk.core.Application.get()
        _ui = _app.userInterface

#        maniglie = loadposman()

        cmdDef = _ui.commandDefinitions.itemById('myAnta')
        if not cmdDef:
            cmdDef = _ui.commandDefinitions.addButtonDefinition(
                'myAnta', 'Anta Massello', 'Crea anta Massello', 'res')
        onCommandCreated = ProfileCommandCreatedHandler()
        cmdDef.commandCreated.add(onCommandCreated)
        _handlers.append(onCommandCreated)

        cmdDef.execute()

        adsk.autoTerminate(False)
    except:
        if _ui:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


class ProfileCommandDestroyHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            eventArgs = adsk.core.CommandEventArgs.cast(args)
            adsk.terminate()
        except:
            if _ui:
                _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


class ProfileCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            eventArgs = adsk.core.CommandCreatedEventArgs.cast(args)

            # Verify that a Fusion design is active.
            design = adsk.fusion.Design.cast(_app.activeProduct)
            if not design:
                _ui.messageBox('Un disegno deve essere attivo')
                return()
            global _units,_alt,_larg,_sps,_massello,_pannello,_doppio,_maniglia,_cava, _errMessage
            _units = design.unitsManager.defaultLengthUnits
            # impostazione dei valori e defaults
            alt = getattr(design, 'alt', "450")
            larg = getattr(design, 'larg', "600")
            sps = getattr(design, 'sps', "20")
            massello = getattr(design, 'massello', "50")
            pannello= getattr(design, 'pannello', "8")
            cava=getattr(design,'cava',5)
            
            cmd = eventArgs.command
            cmd.isExecutedWhenPreEmpted = False
            inputs = cmd.commandInputs
            _alt = inputs.addValueInput(
                'alt', 'altezza', "mm", adsk.core.ValueInput.createByReal(float(alt)))
            _larg = inputs.addValueInput(
                'larg', 'larghezza', "mm", adsk.core.ValueInput.createByReal(float(larg)))
            _sps = inputs.addValueInput(
                'sps', 'spessore', "mm", adsk.core.ValueInput.createByReal(float(sps)))
            _massello = inputs.addValueInput(
                'massello', 'massello', "mm", adsk.core.ValueInput.createByReal(float(massello)))
            _pannello = inputs.addValueInput(
                'pannello', 'pannello', "mm", adsk.core.ValueInput.createByReal(float(pannello)))
            _cava = inputs.addValueInput(
                'cava', 'cava', "mm", adsk.core.ValueInput.createByReal(float(cava)))
                
                
#    
#            _t0 = inputs.addDropDownCommandInput('t0', 'Tipo Profilo', adsk.core.DropDownStyles.TextListDropDownStyle)
'''
            _maniglia = inputs.addDropDownCommandInput(
                'maniglia', 'pos maniglia', adsk.core.DropDownStyles.TextListDropDownStyle)
           

            
            kk = []
            for x in profili.keys():
                kk.append(x)
            kk.sort()
            _maniglia.listItems.clear()
            for x in kk:
                _maniglia.listItems.add(x, x == maniglia)
 '''           
            _doppio = inputs.addDropDownCommandInput(
                'doppio', 'Anta doppia', adsk.core.DropDownStyles.TextListDropDownStyle)
            _doppio.listItems.add("no", True)
            _doppio.listItems.add("si", False)
            _errMessage = inputs.addTextBoxCommandInput(
                'errMessage', '', '', 2, True)
            _errMessage.isFullWidth = True

            onInputChanged = ProfileCommandInputChangedHandler()
            cmd.inputChanged.add(onInputChanged)
    
            _handlers.append(onInputChanged)

            onExecute = ProfileCommandExecuteHandler()
            cmd.execute.add(onExecute)
            _handlers.append(onExecute)

            onDestroy = ProfileCommandDestroyHandler()
            cmd.destroy.add(onDestroy)
            _handlers.append(onDestroy)
        except:
            if _ui:
                _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


# ---- eventi di validazione

class ProfileCommandInputChangedHandler(adsk.core.InputChangedEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            eventArgs = adsk.core.InputChangedEventArgs.cast(args)
            changedInput = eventArgs.input
'''
            global _a2, _b2, _doppio
            if changedInput.id == 'doppio':
                vis = _doppio.selectedItem.name != 'no'
                _a2.isVisible = vis
                _b2.isVisible = vis
'''
        except:
            if _ui:
                _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


class ProfileCommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            global _alt,_larg,_sps,_massello,_pannello,_doppio,_maniglia,_cava, _app,_errMessage
            eventArgs = adsk.core.CommandEventArgs.cast(args)
            design = adsk.fusion.Design.cast(_app.activeProduct)
            attrs = design.attributes

            # variabili input
            alt = _alt.value
            larg = _larg.value
            sps = _sps.value
            massello = _massello.value
            pannello = _pannello.value
            cava = _cava.value
            
            doppio = _doppio.selectedItem.name
            maniglia = _tipo.selectedItem.name
            
        
            setattr(design, "alt", str(alt))
            setattr(design, "larg", str(larg))
            setattr(design, "sps", str(sps))
            setattr(design, "massello", str(massello))
            setattr(design, "pannello", str(pannello))
            setattr(design, "cava", str(cava))
            
            '''
            profilo = profili[tprofilo]
            if profilo:
                comp = draw(design, lung, profilo, a1, a2, b1, b2, modo)

                # zoom and fit
                if comp:
                    camera_ = _app.activeViewport.camera
                    camera_.isFitView = True
                    _app.activeViewport.camera = camera_
            '''
        except:
            if _ui:
                _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def draw(design, lung, tipo, a1, a2, b1, b2, modo):
    unitsMgr = design.unitsManager
    occs = design.rootComponent.occurrences

    return
'''
    tp = tipo.tipo
    py = unitsMgr.evaluateExpression(str(tipo.l), "mm")
    px = unitsMgr.evaluateExpression(str(tipo.a), "mm")
    sp = unitsMgr.evaluateExpression(str(tipo.sp), "mm")
    spacing = unitsMgr.evaluateExpression("20", "mm")
    subh=unitsMgr.evaluateExpression("-200", "mm")
    pos = float(getattr(design, 'pos', "0"))
    setattr(design, "pos", str(pos-px-spacing))

    mat = adsk.core.Matrix3D.create()
    mat.translation = adsk.core.Vector3D.create(0, subh, pos)
    newOcc = occs.addNewComponent(mat)
    newComp = adsk.fusion.Component.cast(newOcc.component)

    if modo == 'no':
        a2 = b2 = 0

    sketches = newComp.sketches
    sk = sketches.add(newComp.yZConstructionPlane)
    sk.name = "profilo"

    name = "p"+str(lung)+" "+tipo.name()
    if a1:
        name = name+" a1="+todegstr(a1)
        if a2:
            name = name+"/"+todegstr(a2)
    if b1:
        name = name+" b1="+todegstr(b1)
        if b2:
            name = name+"/"+todegstr(b2)
    newComp.name = name

    # profilo a l
    lines = sk.sketchCurves.sketchLines
    if tp == 'l':
        l1 = lines.addByTwoPoints(adsk.core.Point3D.create(
            0, 0, 0), adsk.core.Point3D.create(px, 0, 0))
        l2 = lines.addByTwoPoints(
            l1.endSketchPoint, adsk.core.Point3D.create(px, sp, 0))
        l3 = lines.addByTwoPoints(
            l2.endSketchPoint, adsk.core.Point3D.create(sp, sp, 0))
        l4 = lines.addByTwoPoints(
            l3.endSketchPoint, adsk.core.Point3D.create(sp, py, 0))
        l5 = lines.addByTwoPoints(
            l4.endSketchPoint, adsk.core.Point3D.create(0, py, 0))
        l6 = lines.addByTwoPoints(
            l5.endSketchPoint, adsk.core.Point3D.create(0, 0, 0))
        # arc = sk.sketchCurves.sketchArcs.addFillet(
        #    l1, l1.startSketchPoint.geometry, l6, l6.endSketchPoint.geometry, sp*0.6)
    elif tp == 's' or tp == "q" or tp == "r":
        l1 = lines.addByTwoPoints(adsk.core.Point3D.create(
            0, 0, 0), adsk.core.Point3D.create(px, 0, 0))
        l2 = lines.addByTwoPoints(
            l1.endSketchPoint, adsk.core.Point3D.create(px, py, 0))
        l3 = lines.addByTwoPoints(
            l2.endSketchPoint, adsk.core.Point3D.create(0, py, 0))
        l4 = lines.addByTwoPoints(
            l3.endSketchPoint, adsk.core.Point3D.create(0, 0, 0))
        if sp:
            '''
            arc = sk.sketchCurves.sketchArcs.addFillet(
                l1, l1.startSketchPoint.geometry, l2, l2.endSketchPoint.geometry, sp*0.6)
            arc = sk.sketchCurves.sketchArcs.addFillet(
                l2, l2.startSketchPoint.geometry, l3, l3.endSketchPoint.geometry, sp*0.6)
            arc = sk.sketchCurves.sketchArcs.addFillet(
                l3, l3.startSketchPoint.geometry, l4, l4.endSketchPoint.geometry, sp*0.6)
            arc = sk.sketchCurves.sketchArcs.addFillet(
                l4, l4.startSketchPoint.geometry, l1, l1.endSketchPoint.geometry, sp*0.6)
            '''
            l1 = lines.addByTwoPoints(adsk.core.Point3D.create(
                sp, sp, 0), adsk.core.Point3D.create(px-sp, sp, 0))
            l2 = lines.addByTwoPoints(
                l1.endSketchPoint, adsk.core.Point3D.create(px-sp, py-sp, 0))
            l3 = lines.addByTwoPoints(
                l2.endSketchPoint, adsk.core.Point3D.create(sp, py-sp, 0))
            l4 = lines.addByTwoPoints(
                l3.endSketchPoint, adsk.core.Point3D.create(sp, sp, 0))
    elif tp == 'c':
        circles = sk.sketchCurves.sketchCircles
        circle1 = circles.addByCenterRadius(
            adsk.core.Point3D.create(px/2, px/2, 0), px/2)
        if sp:
            circle2 = circles.addByCenterRadius(
                adsk.core.Point3D.create(px/2, px/2, 0), px/2-sp)

    prof = sk.profiles.item(0)
    extrudes = newComp.features.extrudeFeatures
    extrude = extrudes.addSimple(prof, adsk.core.ValueInput.createByReal(
        lung), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    lastIndex = extrude.timelineObject.index
    body = extrude.bodies.item(0)
    body.name = "elemento"

    if modo != 'collineare':
        if a1:
            sk = sketches.add(newComp.xYConstructionPlane)
            sk.name = "taglio1"
            lines = sk.sketchCurves.sketchLines
            if (a1 < 0):
                p2 = py*math.tan(-a1)
                createtriag(lines, 0, 0, p2, 0, 0, py)
            else:
                p2 = py*math.tan(a1)
                createtriag(lines, 0, 0, p2, py, 0, py)

            prof = sk.profiles.item(0)
            dist = adsk.core.ValueInput.createByReal(py)

            extrude = extrudes.createInput(
                prof, adsk.fusion.FeatureOperations.CutFeatureOperation)
            extrude.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(
                dist), adsk.fusion.ExtentDirections.NegativeExtentDirection)
            extrude = extrudes.add(extrude)
            lastIndex = extrude.timelineObject.index
        if a2:
            sk = sketches.add(newComp.xZConstructionPlane)
            sk.name = "taglio2"
            lines = sk.sketchCurves.sketchLines
            if (a2 < 0):
                p2 = px*math.tan(-a2)
                createtriag(lines, 0, 0, p2, 0, 0, px)
            else:
                p2 = px*math.tan(a2)
                createtriag(lines, 0, 0, p2, px, 0, px)

            prof = sk.profiles.item(0)
            dist = adsk.core.ValueInput.createByReal(py)

            extrude = extrudes.createInput(
                prof, adsk.fusion.FeatureOperations.CutFeatureOperation)
            extrude.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(
                dist), adsk.fusion.ExtentDirections.PositiveExtentDirection)
            extrude = extrudes.add(extrude)
            lastIndex = extrude.timelineObject.index

        if b1:
            sk = sketches.add(newComp.xYConstructionPlane)
            sk.name = "taglio3"
            lines = sk.sketchCurves.sketchLines
            if (b1 < 0):
                p2 = py*math.tan(-b1)
                l1 = lines.addByTwoPoints(adsk.core.Point3D.create(
                    lung, 0, 0), adsk.core.Point3D.create(lung-p2, 0, 0))
                l2 = lines.addByTwoPoints(
                    l1.endSketchPoint, adsk.core.Point3D.create(lung, py, 0))
                l3 = lines.addByTwoPoints(
                    l2.endSketchPoint, adsk.core.Point3D.create(lung, 0, 0))
            else:
                p2 = py*math.tan(b1)
                l1 = lines.addByTwoPoints(adsk.core.Point3D.create(
                    lung, 0, 0), adsk.core.Point3D.create(lung-p2, py, 0))
                l2 = lines.addByTwoPoints(
                    l1.endSketchPoint, adsk.core.Point3D.create(lung, py, 0))
                l3 = lines.addByTwoPoints(
                    l2.endSketchPoint, adsk.core.Point3D.create(lung, 0, 0))

            prof = sk.profiles.item(0)
            dist = adsk.core.ValueInput.createByReal(px)

            extrude = extrudes.createInput(
                prof, adsk.fusion.FeatureOperations.CutFeatureOperation)
            extrude.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(
                dist), adsk.fusion.ExtentDirections.NegativeExtentDirection)
            extrude = extrudes.add(extrude)
            lastIndex = extrude.timelineObject.index
        if b2:
            sk = sketches.add(newComp.xZConstructionPlane)
            sk.name = "taglio4"
            lines = sk.sketchCurves.sketchLines
            if (b2 < 0):
                p2 = px*math.tan(-b2)
                l1 = lines.addByTwoPoints(adsk.core.Point3D.create(
                    lung, 0, 0), adsk.core.Point3D.create(lung-p2, 0, 0))
                l2 = lines.addByTwoPoints(
                    l1.endSketchPoint, adsk.core.Point3D.create(lung, px, 0))
                l3 = lines.addByTwoPoints(
                    l2.endSketchPoint, adsk.core.Point3D.create(lung, 0, 0))
            else:
                p2 = px*math.tan(b2)
                l1 = lines.addByTwoPoints(adsk.core.Point3D.create(
                    lung, 0, 0), adsk.core.Point3D.create(lung-p2, px, 0))
                l2 = lines.addByTwoPoints(
                    l1.endSketchPoint, adsk.core.Point3D.create(lung, px, 0))
                l3 = lines.addByTwoPoints(
                    l2.endSketchPoint, adsk.core.Point3D.create(lung, 0, 0))

            prof = sk.profiles.item(0)
            dist = adsk.core.ValueInput.createByReal(py)

            extrude = extrudes.createInput(
                prof, adsk.fusion.FeatureOperations.CutFeatureOperation)
            extrude.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(
                dist), adsk.fusion.ExtentDirections.PositiveExtentDirection)
            extrude = extrudes.add(extrude)
            lastIndex = extrude.timelineObject.index
    else:
        # modo collineare
        if a1 > 0 and a1 < 80:
            sk = sketches.add(newComp.xYConstructionPlane)
            sk.name = "taglio1"
            lines = sk.sketchCurves.sketchLines
            p2 = py/2*math.tan(a1)
            l1 = lines.addByTwoPoints(adsk.core.Point3D.create(
                0, 0, 0), adsk.core.Point3D.create(p2, 0, 0))
            l2 = lines.addByTwoPoints(
                l1.endSketchPoint, adsk.core.Point3D.create(0, py/2, 0))
            l3 = lines.addByTwoPoints(
                l2.endSketchPoint, adsk.core.Point3D.create(0, 0, 0))
            prof = sk.profiles.item(0)
            dist = adsk.core.ValueInput.createByReal(px)
            extrude = extrudes.createInput(
                prof, adsk.fusion.FeatureOperations.CutFeatureOperation)
            extrude.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(
                dist), adsk.fusion.ExtentDirections.NegativeExtentDirection)
            extrude = extrudes.add(extrude)
            lastIndex = extrude.timelineObject.index
        if a2 > 0 and a2 < 80:
            sk = sketches.add(newComp.xYConstructionPlane)
            sk.name = "taglio2"
            lines = sk.sketchCurves.sketchLines
            p2 = py/2*math.tan(a2)
            l1 = lines.addByTwoPoints(adsk.core.Point3D.create(
                0, py/2, 0), adsk.core.Point3D.create(p2, py, 0))
            l2 = lines.addByTwoPoints(
                l1.endSketchPoint, adsk.core.Point3D.create(0, py, 0))
            l3 = lines.addByTwoPoints(
                l2.endSketchPoint, adsk.core.Point3D.create(0, py/2, 0))
            prof = sk.profiles.item(0)
            dist = adsk.core.ValueInput.createByReal(px)
            extrude = extrudes.createInput(
                prof, adsk.fusion.FeatureOperations.CutFeatureOperation)
            extrude.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(
                dist), adsk.fusion.ExtentDirections.NegativeExtentDirection)
            extrude = extrudes.add(extrude)
            lastIndex = extrude.timelineObject.index

        if b1 > 0 and b1 < 80:
            sk = sketches.add(newComp.xYConstructionPlane)
            sk.name = "taglio3"
            lines = sk.sketchCurves.sketchLines
            p2 = py/2*math.tan(b1)
            l1 = lines.addByTwoPoints(adsk.core.Point3D.create(
                lung, 0, 0), adsk.core.Point3D.create(lung-p2, 0, 0))
            l2 = lines.addByTwoPoints(
                l1.endSketchPoint, adsk.core.Point3D.create(lung, py/2, 0))
            l3 = lines.addByTwoPoints(
                l2.endSketchPoint, adsk.core.Point3D.create(lung, 0, 0))
            prof = sk.profiles.item(0)
            dist = adsk.core.ValueInput.createByReal(px)
            extrude = extrudes.createInput(
                prof, adsk.fusion.FeatureOperations.CutFeatureOperation)
            extrude.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(
                dist), adsk.fusion.ExtentDirections.NegativeExtentDirection)
            extrude = extrudes.add(extrude)
            lastIndex = extrude.timelineObject.index
        if b2 > 0 and b2 < 80:
            sk = sketches.add(newComp.xYConstructionPlane)
            sk.name = "taglio4"
            lines = sk.sketchCurves.sketchLines
            p2 = py/2*math.tan(b2)
            l1 = lines.addByTwoPoints(adsk.core.Point3D.create(
                lung, py/2, 0), adsk.core.Point3D.create(lung, py, 0))
            l2 = lines.addByTwoPoints(
                l1.endSketchPoint, adsk.core.Point3D.create(lung-p2, py, 0))
            l3 = lines.addByTwoPoints(
                l2.endSketchPoint, adsk.core.Point3D.create(lung, py/2, 0))
            prof = sk.profiles.item(0)
            dist = adsk.core.ValueInput.createByReal(px)
            extrude = extrudes.createInput(
                prof, adsk.fusion.FeatureOperations.CutFeatureOperation)
            extrude.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(
                dist), adsk.fusion.ExtentDirections.NegativeExtentDirection)
            extrude = extrudes.add(extrude)
            lastIndex = extrude.timelineObject.index

    # Group everything
    timelineGroups = design.timeline.timelineGroups
    newOccIndex = newOcc.timelineObject.index
    timelineGroup = timelineGroups.add(newOccIndex, lastIndex)
    timelineGroup.name = "profilo"

    return newComp


def createtriag(lines, ax, ay, bx, by, cx, cy):
    l1 = lines.addByTwoPoints(adsk.core.Point3D.create(
        ax, ay, 0), adsk.core.Point3D.create(bx, by, 0))
    l2 = lines.addByTwoPoints(
        l1.endSketchPoint, adsk.core.Point3D.create(cx, cy, 0))
    l3 = lines.addByTwoPoints(
        l2.endSketchPoint, adsk.core.Point3D.create(ax, ay, 0))
    return



def cuttriag(extrudes,sk,dd,neg=true):
    prof = sk.profiles.item(0)
    dist = adsk.core.ValueInput.createByReal(dd)
    extrude = extrudes.createInput(prof, adsk.fusion.FeatureOperations.CutFeatureOperation)
    if neg:
        extrude.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(dist), adsk.fusion.ExtentDirections.NegativeExtentDirection)
    else:
        extrude.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(dist), adsk.fusion.ExtentDirections.PositiveExtentDirection)
    extrude = extrudes.add(extrude) 
    return extrude.timelineObject.index
'''
