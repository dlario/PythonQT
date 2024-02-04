from PackageManager.Packages.ProgramBase import Commands

class KeyPressEventRegister(object):
    def keyPressEvent(self, event):
        modifiers = event.modifiers()
        currentInputAction = InputAction(name="temp", actionType=InputActionType.Keyboard, key=event.key(), modifiers=modifiers)

        actionSaveVariants = InputManager()["App.Save"]
        actionNewFileVariants = InputManager()["App.NewFile"]
        actionLoadVariants = InputManager()["App.Load"]
        actionSaveAsVariants = InputManager()["App.SaveAs"]

        if currentInputAction in actionNewFileVariants:
            shouldSave = self.shouldSave()
            if shouldSave == QMessageBox.Yes:
                self.save()
            elif shouldSave == QMessageBox.Discard:
                return

            EditorHistory().clear()
            historyTools = self._getRegisteredCommands(classNameFilters=["HistoryTool"])
            for historyTools in historyTools:
                historyTools.onClear()
            self.newFile()
            EditorHistory().saveState("New file")
            self.currentFileName = None
            self.modified = False
            self.updateLabel()
        if currentInputAction in actionSaveVariants:
            self.save()
        if currentInputAction in actionLoadVariants:
            shouldSave = self.shouldSave()
            if shouldSave == QMessageBox.Yes:
                self.save()
            elif shouldSave == QMessageBox.Discard:
                return
            self.load()
        if currentInputAction in actionSaveAsVariants:
            self.save(True)