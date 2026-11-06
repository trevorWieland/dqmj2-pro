#include "dependency000.h"

void native_utility_child_arm7_main_027e1fb8(void *arg)
{
    WMSPWork *sys = WMSP_GetSystemWork();
    OSMessage msg;
    u16 cmd_group;
    u16 cmd_id;
    while (1 ) {
        (void)native_utility_child_arm7_arm_037fcc2c(&(sys->fromWLmsgQ), &msg, 1 );
        if (msg == 0) {
            native_utility_child_arm7_arm_037fc5c0();
            return;
        }
        cmd_group = (u16)(((WlCmdReq *)msg)->header.code & 0xFF00 );
        cmd_id = (u16)(((WlCmdReq *)msg)->header.code & 0x00FF );
        ((void)0) ;
        switch (cmd_group) {
        case 0x0100 :
        case 0x0000 :
            if (cmd_id & 0x80) {
                native_utility_child_arm7_arm_027e1e6c((WlCmdReq *)msg);
                continue;
            }
            break;
        }
        (void)native_utility_child_arm7_arm_037fcccc(&(sys->confirmQ), msg, 1 );
    }
}
#include "dependency001.h"
