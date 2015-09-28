from AppKit import *
import os
import datetime
from lib.baseObjects import CallbackWrapper
import vanilla.dialogs as dialogs
from mojo.UI import CurrentFontWindow

class SaveCopyMenu(object):

    def __init__(self):        
        title = "Save Copy..."
        mainMenu = NSApp().mainMenu()
        fileMenu = mainMenu.itemWithTitle_("File")

        if not fileMenu:
            return

        fileMenu = fileMenu.submenu()

        if fileMenu.itemWithTitle_(title):
            return

        index = fileMenu.indexOfItemWithTitle_("Save")
        self.target = CallbackWrapper(self.callback)

        newItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(title, "action:", "s")
        modifier = NSCommandKeyMask | NSControlKeyMask
        newItem.setKeyEquivalentModifierMask_(modifier)
        newItem.setTarget_(self.target)

        fileMenu.insertItem_atIndex_(newItem, index+1)

    def callback(self, sender):
        w = CurrentFontWindow()
        if w:
            f = CurrentFont()
            fileName = None
            if f.path:
                fileName, ext = os.path.splitext(os.path.basename(f.path))
                stamp = datetime.datetime.now().strftime("(%Y%m%d_%H%M%S)")
                fileName = "%s-%s%s" % (fileName, stamp, ext)

            dialogs.putFile(title="Save a Copy as..", fileName=fileName, fileTypes=["ufo"], parentWindow=w.window(), resultCallback=self.saveCopy)
                
    def saveCopy(self, path):
        f = CurrentFont().copy()
        f.save(path)


SaveCopyMenu()


