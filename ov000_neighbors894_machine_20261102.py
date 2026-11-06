import ov000_neighbors892_machine_20261102 as B
from ov000_neighbors892_machine_20261102 import ENTRY, FIND, SP


class Machine(B.Machine):
    def __init__(self, main, overlay, images, profile):
        super().__init__(main, overlay, images, profile)
        self.callSites = []

    def code(self, u, pc, size, unused):
        if pc == FIND and self.top != FIND:
            self.callSites.append(dict(target=hex(pc), callerReturnPc=hex(u.reg_read(B.R.UC_ARM_REG_LR))))
        super().code(u, pc, size, unused)

    def run(self, start, top=ENTRY):
        result = super().run(start, top)
        result['callSites'] = self.callSites
        return result
