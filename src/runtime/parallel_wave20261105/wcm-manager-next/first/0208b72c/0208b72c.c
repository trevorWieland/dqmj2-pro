#include "context.h"
BOOL native_main_0208b72c (u8 * a, u8 * b)
{
    s32 i;
    for (i = 0; i < WCM_BSSID_SIZE; i++) {
        if (a[i] != b[i]) {
            return FALSE;
        }
    }
    return TRUE;
}
