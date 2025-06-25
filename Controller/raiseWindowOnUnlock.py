from PyQt5.QtCore import QObject

class RaiseWindowOnUnlock(QObject):

    def __init__(self, app, dep, workers):
        super().__init__()
        self.app = app
        self.dep = dep
        self.workers = workers
        self._already_raised = False

        print("Setting up observer for screen unlock via distributed notifications...")

        center = self.dep.NSDistributedNotificationCenter.defaultCenter()
        center.addObserver_selector_name_object_(
            self,
            "screenUnlocked:",              # ← selector as str
            "com.apple.screenIsUnlocked",
            None
        )

        print("Distributed notification observer set up.")

    # -------------- handler -----------------
    def screenUnlocked_(self, _notification):   # ← renamed (no leading underscore)
        print("✅ Screen unlock notification received.")
        if self._already_raised:
            return
        self._already_raised = True
        self.dep.QTimer.singleShot(5000, self._bringDailyWordAppToFront)

    # -------------- helper ------------------
    def _bringDailyWordAppToFront(self):
        print("Inside _bringDailyWordAppToFront")
        daily_worker = self.workers.get('dailyWordApp')
        if (
            daily_worker
            and hasattr(daily_worker, "window")
            and daily_worker.window
            and daily_worker.window.isVisible()
        ):
            print("Raising and activating dailyWordApp window")
            daily_worker.window.raise_()
            daily_worker.window.activateWindow()
    
    def reset(self):
        self._already_raised = False