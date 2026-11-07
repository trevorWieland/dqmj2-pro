#include "context.h"
u16 native_main_020a4114 (const DWCTransportHeader * message)
{
    DWCTransportHeader header;

    MI_CpuCopy8(message, (u8 *) &header, sizeof(DWCTransportHeader));

    if ((memcmp(header.magicStrings, native_data_020e02d0, DWC_MAGIC_STRINGS_LEN) == 0)) {
        return header.type;
    }

    return DWC_SEND_TYPE_INVALID;
}
