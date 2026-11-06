#include "context000.h"

void WMSP_SetParentMaxSize(u16 parentMaxSize)
{
    if (parentMaxSize > 0x200) {
        parentMaxSize = 0x200;
    }
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
