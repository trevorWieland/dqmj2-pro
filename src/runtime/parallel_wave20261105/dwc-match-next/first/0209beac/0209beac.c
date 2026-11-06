#include "context.h"
u32 native_main_0209beac(u8 * aidList, int aidListLen)
{
    u32 bitmap = 0;
    int i;

    for (i = 0; i < aidListLen; i++) {
        bitmap |= 1u << aidList[i];
    }

    return bitmap;
}