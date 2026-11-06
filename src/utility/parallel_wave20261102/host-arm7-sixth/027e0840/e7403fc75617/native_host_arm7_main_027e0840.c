#include "dependency000.h"

void native_host_arm7_main_027e0840(u16 parentSize)
{
    WMStatus *status = WMSP_GetStatusStructure();
    status->mp_parentSize = parentSize;
    if (status->aid == 0) {
        u16 sendSize = (u16)(parentSize + 4 );
        status->mp_sendSize = sendSize;
    } else {
        u16 recvSize = (u16)(parentSize + 4 );
        status->mp_recvSize = recvSize;
    }
}
