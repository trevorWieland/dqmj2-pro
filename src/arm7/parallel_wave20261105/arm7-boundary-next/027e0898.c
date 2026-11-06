#include "context000.h"

#include "context001.h"

#include "context002.h"

void native_host_arm7_main_027e0898(void *arg)
{
    WMSPWork *sys = WMSP_GetSystemWork();
    OSMessage msg;
    u16 cmd_group;
    u16 cmd_id;
    while (1 ) {
        (void)native_host_arm7_arm_037fc760(&(sys->fromWLmsgQ), &msg, 1 );
        if (msg == 0) {
            native_host_arm7_arm_037fc15c();
            return;
        }
        cmd_group = (u16)(((WlCmdReq *)msg)->header.code & 0xFF00 );
        cmd_id = (u16)(((WlCmdReq *)msg)->header.code & 0x00FF );
        ((void)0) ;
        switch (cmd_group) {
        case 0x0100 :
        case 0x0000 :
            if (cmd_id & 0x80) {
                WmspIndicate((WlCmdReq *)msg);
                continue;
            }
            break;
        }
        (void)native_host_arm7_arm_037fc6d4(&(sys->confirmQ), msg, 1 );
    }
}

#include "context003.h"

#include "context004.h"
