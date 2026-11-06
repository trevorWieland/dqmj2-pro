#include "dependency000.h"

void native_host_arm7_main_027e086c(u16 childSize)
{
    WMStatus *status = WMSP_GetStatusStructure();
    status->mp_childSize = childSize;
    if (status->aid == 0) {
        u16 recvSize = (u16)(childSize + 2 );
        status->mp_recvSize = recvSize;
    } else {
        u16 sendSize = (u16)(childSize + 2 );
        status->mp_sendSize = sendSize;
    }
}
