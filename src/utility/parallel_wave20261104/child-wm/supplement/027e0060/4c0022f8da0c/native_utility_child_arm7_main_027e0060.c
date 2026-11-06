#include "dependency000.h"

void native_utility_child_arm7_main_027e0060(u16 childMaxSize)
{
    WMStatus *status = WMSP_GetStatusStructure();
    status->mp_childMaxSize = childMaxSize;
    status->mp_childSize = childMaxSize;
    if (status->aid == 0) {
        u16 maxRecvSize = (u16)(childMaxSize + 2 );
        status->mp_maxRecvSize = maxRecvSize;
        status->mp_recvSize = maxRecvSize;
    } else {
        u16 maxSendSize = (u16)(childMaxSize + 2 );
        status->mp_maxSendSize = maxSendSize;
        status->mp_sendSize = maxSendSize;
    }
}
