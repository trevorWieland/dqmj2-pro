#include "context.h"
BOOL native_main_0209f47c (int profileID, int numHost)
{
    int i;
    if (!native_fn_020a3d70()) return FALSE;
    for (i = 0; i < numHost; i++) {
        if (native_fn_020a3d70()->sbPidList[i] == profileID) {
            native_fn_0209f4bc(i, numHost);
            return TRUE;
        }
    }
    return FALSE;
}
