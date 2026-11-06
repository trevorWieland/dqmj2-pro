#include "dependency000.h"

void native_utility_child_arm7_main_027e00b0(u16 parentMaxSize)
{
    WMStatus *status = WMSP_GetStatusStructure();
    status->mp_parentSize = parentMaxSize;
    status->mp_parentMaxSize = parentMaxSize;
    if (status->aid == 0) {
        u16 maxSendSize = (u16)(parentMaxSize + 4 );
        status->mp_maxSendSize = maxSendSize;
        status->mp_sendSize = maxSendSize;
    } else {
        u16 maxRecvSize = (u16)(parentMaxSize + 4 );
        status->mp_maxRecvSize = maxRecvSize;
        status->mp_recvSize = maxRecvSize;
    }
}
