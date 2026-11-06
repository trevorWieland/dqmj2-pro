#include "context000.h"

void WMSP_ResetSizeVars(void)
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
