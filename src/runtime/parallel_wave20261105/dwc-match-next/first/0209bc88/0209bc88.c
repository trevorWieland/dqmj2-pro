#include "context.h"
DWCState native_main_0209bc88(void)
{
    if (!stpDwcCnt) {
        return DWC_STATE_INIT;
    } else {
        return stpDwcCnt->state;
    }
}