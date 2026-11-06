#include "context000.h"

void WMSP_SetChildSize(u16 childSize)
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
