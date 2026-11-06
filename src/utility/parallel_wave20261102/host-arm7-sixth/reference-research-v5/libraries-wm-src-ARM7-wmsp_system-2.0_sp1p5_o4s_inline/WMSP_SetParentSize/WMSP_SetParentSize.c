#include "context000.h"

void WMSP_SetParentSize(u16 parentSize)
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
