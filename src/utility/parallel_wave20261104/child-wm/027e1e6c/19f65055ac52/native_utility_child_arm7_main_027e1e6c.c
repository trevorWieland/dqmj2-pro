#include "dependency000.h"
#include "dependency001.h"

void native_utility_child_arm7_main_027e1e6c(WlCmdReq *req)
{
    if (((void *)0) == WMSP_GetSystemWork()->wm7buf) {
        return;
    }
    if (WM_STATE_STOP == WMSP_GetStatusStructure()->state) {
        return;
    }
    switch (req->header.code) {
    case (0x0000 | 0x84) :
        native_utility_child_arm7_arm_027e091c(req);
        break;
    case (0x0000 | 0x85) :
        native_utility_child_arm7_arm_027e0950(req);
        break;
    case (0x0000 | 0x86) :
        native_utility_child_arm7_arm_027e0c18(req);
        break;
    case (0x0000 | 0x87) :
        native_utility_child_arm7_arm_027e0da0(req);
        break;
    case (0x0000 | 0x88) :
        native_utility_child_arm7_arm_027e0dd4(req);
        break;
    case (0x0000 | 0x8B) :
        native_utility_child_arm7_arm_027e1c2c(req);
        break;
    case (0x0000 | 0x8C) :
        native_utility_child_arm7_arm_027e1ddc(req);
        break;
    case (0x0000 | 0x8D) :
        native_utility_child_arm7_arm_027e1c78(req);
        break;
    case (0x0100 | 0x80) :
        native_utility_child_arm7_arm_027e0f40(req);
        break;
    case (0x0100 | 0x82) :
        native_utility_child_arm7_arm_027e13e4(req);
        break;
    case (0x0100 | 0x84) :
        native_utility_child_arm7_arm_027e18c4(req);
        break;
    case (0x0100 | 0x85) :
        native_utility_child_arm7_arm_027e10d4(req);
        break;
    case (0x0100 | 0x86) :
        native_utility_child_arm7_arm_027e0e08(req);
        break;
    default:
        native_utility_child_arm7_arm_027e1e28(req);
    }
    native_utility_child_arm7_arm_027e1e2c(req);
}
#include "dependency002.h"
