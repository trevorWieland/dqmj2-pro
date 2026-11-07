#include "context.h"
s32 native_main_020a4144 (u16 type)
{
    s32 size;

    switch (type) {
    case DWC_SEND_TYPE_MATCH_SYN:
    case DWC_SEND_TYPE_MATCH_SYN_ACK:
    case DWC_SEND_TYPE_MATCH_ACK:
        size = sizeof(DWCTransportHeader) + DWC_MATCH_SYN_DATA_BODY_SIZE;
        break;
    default:
        size = sizeof(DWCTransportHeader);
        break;
    }

    return size;
}
