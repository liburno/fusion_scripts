#Author-
#Description-
import adsk.core
import adsk.fusion
import adsk.cam
import traceback
import os
import math
from .utils import *           # libreria comune ai vari script

_app = adsk.core.Application.cast(None)
_ui = adsk.core.UserInterface.cast(None)
_units = ''
_pos = 0
_alt = adsk.core.ValueCommandInput.cast(None)


_errMessage = adsk.core.TextBoxCommandInput.cast(None)
_handlers = []
maniglie = {}


def run(context):
   
    try:
        global _app, _ui
        _app = adsk.core.Application.get()
        _ui = _app.userInterface

        # _ui.messageBox('Hello script 3a')

        cmdDef = _ui.commandDefinitions.itemById('myAnta')
        if not cmdDef:
            cmdDef = _ui.commandDefinitions.addButtonDefinition(
                'myAnta', 'Anta', 'Crea una anta', 'res')
        
        
        onCommandCreated = Create()
        cmdDef.commandCreated.add(onCommandCreated)
        _handlers.append(onCommandCreated)
        cmdDef.execute()
        adsk.autoTerminate(False)
    except:
        if _ui:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


class Destroy(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        global _ui
        try:
            eventArgs = adsk.core.CommandEventArgs.cast(args)
            adsk.terminate()
        except:
            if _ui:
                _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


class Create(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        global _ui
        try:
            eventArgs = adsk.core.CommandCreatedEventArgs.cast(args)
            # Verify that a Fusion design is active.
            design = adsk.fusion.Design.cast(_app.activeProduct)
            if not design:
                _ui.messageBox('Un disegno deve essere attivo')
                return
            
            cmd = eventArgs.command
            cmd.isExecutedWhenPreEmpted = False
           
            global _units,_alt, _errMessage
            _units = design.unitsManager.defaultLengthUnits
            alt = getattr(design, 'alt', "450")
            
            inputs = cmd.commandInputs
            _alt = inputs.addValueInput(
                'alt', 'altezza', "mm", adsk.core.ValueInput.createByReal(float(alt)))
            _errMessage = inputs.addTextBoxCommandInput(
                'errMessage', '', '', 2, True)
            _errMessage.isFullWidth = True
            
            
            onInputChanged = InputChanged()
            cmd.inputChanged.add(onInputChanged)
            _handlers.append(onInputChanged)
            
            onExecute = Execute()
            cmd.execute.add(onExecute)
            _handlers.append(onExecute)
            
            onDestroy = Destroy()
            cmd.destroy.add(onDestroy)
            _handlers.append(onDestroy)
        except:
            if _ui:
                _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


class InputChanged(adsk.core.InputChangedEventHandler):
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


class Execute(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        global _ui, _alt, _app,_errMessage
        try:
            eventArgs = adsk.core.CommandEventArgs.cast(args)
            design = adsk.fusion.Design.cast(_app.activeProduct)
            attrs = design.attributes

            # variabili input
            alt = _alt.value
            _ui.messageBox(str(alt))
            '''
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


def draw(design, alt):
    unitsMgr = design.unitsManager
    occs = design.rootComponent.occurrences

    return