import maya.cmds as cmds
import math

class MayaOperations:
    '''
    Class containing static methods for Maya operations to be performed by the tool.
    '''
    @staticmethod
    def circleAroundMesh(*args):
        '''
        Long ass(didn't clean it :]) method to do the following:
        - Create a camera and chnge the view to the camera created
        - Rotate the camera around the mesh at steps of 45 degrees
        - Create 2 frames for each angle and 2 frames for each reference image
        - The reference images are visible only when they are needed
        - Everything gets keyframed except the switch between wireframe and smoothShaded (sigh)
        '''
        selectedMesh = cmds.optionMenu('meshMenu', query=True, value=True)
        selectedMesh = selectedMesh[:len(selectedMesh) - 5] # why do they add 'Shape' to the end :/
        
        if not cmds.objExists(selectedMesh):
            cmds.warning('Selected object does not exist. Please select a valid mesh.')
            return

        cameraName = 'ShowcaseCamera'
        if not cmds.objExists(cameraName):
            cameraName = cmds.camera(name=cameraName)[0]
            
            panel = cmds.getPanel(withFocus=True)
            if panel and 'modelPanel' in panel:
                cmds.lookThru(panel, cameraName)          
            else:
                modelPanels = cmds.getPanel(type='modelPanel')            
                for modelPanel in modelPanels:                
                    cmds.lookThru(modelPanel, cameraName)

        cameraDistance = cmds.floatSliderGrp('cameraDistanceSlider', query=True, value=True) / 100 # hardcoded to look fine
        cameraPitch = cmds.intSliderGrp('cameraPitchSlider', query=True, value=True) / 4

        meshPosition = cmds.xform(selectedMesh, query=True, translation=True, worldSpace=True)

        tempObjects = cmds.ls(geometry=True) + cmds.ls(type='imagePlane')
        allObjects = [obj.replace('Shape', '') for obj in tempObjects] # again with the 'Shape' :/
        
        objectsToHide = []
        
        for i in range (len(allObjects)):
            if allObjects[i] != selectedMesh and cmds.listRelatives(allObjects[i], parent=True) is None and cmds.getAttr(allObjects[i] + '.visibility'):
                objectsToHide.append(allObjects[i])
                cmds.setAttr(allObjects[i] + '.visibility', 0)            
                if cmds.objectType(tempObjects[i]) == 'imagePlane': # check if object is a mesh then use cmds.hide(obj) 
                    objectsToHide.remove(allObjects[i])             # else if it is an imagePlane use cmds.setAttr(obj + '.visibility', 0), also keyframe the visibility for the imagePlane
                    objectsToHide.append(tempObjects[i])
                    cmds.setKeyframe(tempObjects[i], attribute = 'visibility', time=0)

        referenceImages = {} # dictionary to hold the reference images and their angles

        if cmds.checkBox('checkboxRef0', query=True, value=True): # added checkboxes just in case artist don't want to use reference images
            referenceImages[0] = cmds.optionMenu('imagePlaneMenu0', query=True, value=True).replace('Shape', '')
        if cmds.checkBox('checkboxRef90', query=True, value=True):
            referenceImages[90] = cmds.optionMenu('imagePlaneMenu90', query=True, value=True).replace('Shape', '')
        if cmds.checkBox('checkboxRef270', query=True, value=True): 
            referenceImages[270] = cmds.optionMenu('imagePlaneMenu270', query=True, value=True).replace('Shape', '')     

        frame = -1 # starts with 0 in maya
        for angle in range(0, 361, 45): 
            x = meshPosition[0] + 25 * math.cos(math.radians(angle)) # circles around the mesh
            z = meshPosition[2] + 25 * math.sin(math.radians(angle)) # again hardcoded to look fine
            cmds.move(x, meshPosition[1] * ((cameraPitch) + 1), z, cameraName) 

            cmds.viewLookAt(cameraName, pos=meshPosition) # both these functions arelifesaver, imagine doing this manually 
            cmds.viewFit(cameraName, f= 1 / cameraDistance)

            for i in range(2): # 2 frames for each angle
                frame += 1
                cmds.setKeyframe(cameraName, time=frame) 
           
            if angle in referenceImages and cmds.checkBox('checkboxRef' + str(angle), query=True, value=True): # ref images for 0, 90 and 270
                refImage = referenceImages[angle]
                if cmds.objExists(refImage):
                    frame += 1
                    cmds.setAttr(refImage + '.visibility', 1)                
                    cmds.viewFit(cameraName, f=1 / cameraDistance)   
                    cmds.setKeyframe(refImage, attribute='visibility', value=1, time=frame)  
                    cmds.setKeyframe(cameraName, time=frame)  
                    
                    frame += 1
                    cmds.setKeyframe(cameraName, time=frame)
                    cmds.setKeyframe(refImage, attribute='visibility', value=1, time=frame)
                    
                cmds.setAttr(refImage + '.visibility', 0)
                cmds.setKeyframe(refImage, attribute='visibility', value=0, time=frame + 1)

        cmds.playbackOptions(min=0, max=frame)

        for obj in objectsToHide: # clean up
            cmds.setAttr(obj + '.visibility', 1)
            if cmds.objectType(obj) == 'imagePlane':
                cmds.setKeyframe(obj, attribute='visibility', value=1, time=frame) 
                
    # scriptJobId = None

    # @staticmethod
    # def createDisplayModeScriptJob():
    #     '''
    #     Toggles the display mode on every frame change ON.
    #     Subscribes the changeDisplayModeOnFrameChange function to the timeChanged event.
    #     Somehow doesn't work when animation is playing, but works when scrubbing the timeline.
    #     so ig it's fine? 
    #     '''
    #     if MayaOperations.scriptJobId is None: # subscribing the cjangeDisplayModeOnFrameChange function to the timeChanged event
    #         MayaOperations.scriptJobId = cmds.scriptJob(event=['timeChanged', MayaOperations.changeDisplayModeOnFrameChange], killWithScene=False) 
           
    # @staticmethod
    # def killDisplayModeScriptJob():
    #     '''
    #     Toggles the display mode on every frame change OFF.
    #     Kills the script job responsible for the toggling.
    #     '''
    #     if MayaOperations.scriptJobId is not None:
    #         cmds.scriptJob(kill=MayaOperations.scriptJobId, force=True)
    #         MayaOperations.scriptJobId = None

    @staticmethod
    def changeDisplayModeOnFrameChange():
        '''
        Hax to change the display mode on every frame change.
        This function listens to the timeChanged event and changes the display mode to wireframe or smoothShaded.
        '''
        currentFrame = cmds.currentTime(query=True)
        displayMode = ''
        
        if currentFrame % 2 == 0:        
            displayMode = 'smoothShaded'        
        else:        
            displayMode = 'wireframe'
            
        modelPanels = [panel for panel in cmds.getPanel(all=True) if cmds.getPanel(typeOf=panel) == 'modelPanel']
        
        for panel in modelPanels:
            cmds.modelEditor(panel, edit=True, displayAppearance=displayMode)

class ShowcaseToolUI:
    '''
    Class that creates the UI for the tool.
    '''
    def __init__(self):
        '''
        Initializes the class and creates the UI.
        '''
        self.createUI()

    def createUI(self): 
        '''
        Creates and displays the UI.
        '''     
        if cmds.window('ShowcaseToolUI', exists=True):
            cmds.deleteUI('ShowcaseToolUI')

        window = cmds.window('ShowcaseToolUI', title='Model Showcase', widthHeight=(400,300), sizeable=True)
        self.form = cmds.formLayout()

        self.createComponents()
        self.createFormLayout() # using form layout, better than manually positioning everything for the scope of this tool

        cmds.showWindow('ShowcaseToolUI')

    def createComponents(self):
        '''
        Creates all the components of the tool.
        '''
        self.createModelSelection()
        self.createReferenceSelection()
        self.createCameraSettingsSliders()
        self.createShowcaseButton()
        # self.createToggleDisplayModeButton()        

    def createModelSelection(self):
        '''
        Drop-down menu for selecting the model to showcase.
        '''
        self.textModel = cmds.text(label='Model:')
        self.meshMenu = cmds.optionMenu('meshMenu', width=150)
        for mesh in cmds.ls(geometry=True):
            cmds.menuItem(label=mesh)

    def createReferenceSelection(self):
        '''
        Drop-down menus for selecting the reference images to show.
        They enable selectively if the artist wants to use reference images as part of the showcase.
        '''
        self.checkboxRef0 = cmds.checkBox('checkboxRef0', label='', changeCommand=lambda x: self.toggleRefImage(x, self.textRef0, self.imagePlaneMenu0)) 
        self.textRef0 = cmds.text(label='Reference 0:', enable=False)
        self.imagePlaneMenu0 = cmds.optionMenu('imagePlaneMenu0', width=150, enable=False)
        
        self.checkboxRef90 = cmds.checkBox('checkboxRef90', label='', changeCommand=lambda x: self.toggleRefImage(x, self.textRef90, self.imagePlaneMenu90))
        self.textRef90 = cmds.text(label='Reference 90:', enable=False)
        self.imagePlaneMenu90 = cmds.optionMenu('imagePlaneMenu90', width=150, enable=False)
        
        self.checkboxRef270 = cmds.checkBox('checkboxRef270', label='', changeCommand=lambda x: self.toggleRefImage(x, self.textRef270, self.imagePlaneMenu270))
        self.textRef270 = cmds.text(label='Reference 270:', enable=False)
        self.imagePlaneMenu270 = cmds.optionMenu('imagePlaneMenu270', width=150, enable=False)

        for imagePlane in cmds.ls(type='imagePlane'):
            cmds.menuItem(label=imagePlane, parent='imagePlaneMenu0')
            cmds.menuItem(label=imagePlane, parent='imagePlaneMenu90')
            cmds.menuItem(label=imagePlane, parent='imagePlaneMenu270')

    def createCameraSettingsSliders(self):
        '''
        Sliders for setting the camera distance and pitch.
        '''
        self.sliderCameraDistance = cmds.floatSliderGrp('cameraDistanceSlider', label='Camera Distance:', field=True, minValue=100, maxValue=500.0, fieldMinValue=100, fieldMaxValue=500, value=150, width=300)
        self.sliderCameraPitch = cmds.intSliderGrp('cameraPitchSlider', label='Camera Pitch:', field=True, minValue=-80, maxValue=80, fieldMinValue=-80, fieldMaxValue=80, value=0, width=300)

    def createShowcaseButton(self):
        '''
        Button for executing the showcase.
        '''
        self.btnShowcase = cmds.button(label='Showcase', command= MayaOperations.circleAroundMesh, width=100)

    # def createToggleDisplayModeButton(self):
    #     '''
    #     Button for toggling the display mode.
    #     '''
    #     self.btnToggleDisplayMode = cmds.button(label='Toggle Display Mode: OFF', command=self.toggleDisplayModeScriptJob, width=150)

    def createFormLayout(self):
        '''
        Lifesaving layout by Maya to arrange the components in the UI.
        '''
        cmds.formLayout(self.form, edit=True, attachForm=[
            (self.textModel, 'top', 5), (self.textModel, 'left', 5),
            (self.meshMenu, 'top', 5), (self.meshMenu, 'left', 110),
            (self.checkboxRef0, 'top', 38), (self.checkboxRef0, 'left', 270),
            (self.textRef0, 'top', 35), (self.textRef0, 'left', 5),
            (self.imagePlaneMenu0, 'top', 35), (self.imagePlaneMenu0, 'left', 110),
            (self.checkboxRef90, 'top', 68), (self.checkboxRef90, 'left', 270),
            (self.textRef90, 'top', 65), (self.textRef90, 'left', 5),
            (self.imagePlaneMenu90, 'top', 65), (self.imagePlaneMenu90, 'left', 110),
            (self.checkboxRef270, 'top', 98), (self.checkboxRef270, 'left', 270),
            (self.textRef270, 'top', 95), (self.textRef270, 'left', 5),
            (self.imagePlaneMenu270, 'top', 95), (self.imagePlaneMenu270, 'left', 110),
            (self.sliderCameraDistance, 'top', 125),
            (self.sliderCameraPitch, 'top', 155),
            (self.btnShowcase, 'bottom', 5), (self.btnShowcase, 'right', 5)# ,
            # (self.btnToggleDisplayMode, 'bottom', 5), (self.btnToggleDisplayMode, 'left', 5)
        ])           
        
    def toggleRefImage(self, state, textLabel, dropdownMenu):
        '''
        Enable/Disable the reference image drop-down menu.
        '''
        cmds.text(textLabel, edit=True, enable=state)
        cmds.optionMenu(dropdownMenu, edit=True, enable=state)

    # def toggleDisplayModeScriptJob(self, *args):
    #     if MayaOperations.scriptJobId is None:
    #         MayaOperations.createDisplayModeScriptJob()
    #         cmds.button(self.btnToggleDisplayMode, edit=True, label='Toggle Display Mode: ON')
    #     else:
    #         MayaOperations.killDisplayModeScriptJob()
    #         cmds.button(self.btnToggleDisplayMode, edit=True, label='Toggle Display Mode: OFF') 

def main():
    '''
    Run everything.
    '''
    ui = ShowcaseToolUI()
    cmds.scriptJob(event=['timeChanged', MayaOperations.changeDisplayModeOnFrameChange], killWithScene=False) # subscribing the cjangeDisplayModeOnFrameChange function to the timeChanged event
                                               
main()