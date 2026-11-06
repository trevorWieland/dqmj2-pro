#include "dependency000.h"

void native_utility_child_arm7_main_027e0100(void)
{
    WMStatus *status = WMSP_GetStatusStructure();
    status->mp_sendSize = 0;
    status->mp_recvSize = 0;
    status->mp_parentSize = 0;
    status->mp_childSize = 0;
    status->mp_maxSendSize = 0;
    status->mp_maxRecvSize = 0;
    status->mp_parentMaxSize = 0;
    status->mp_childMaxSize = 0;
}
