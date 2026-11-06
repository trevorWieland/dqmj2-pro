#include "context000.h"

#include "context001.h"

void WSetStaState(u32 state)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work;
    if (pWork->STA == state) {
        return;
    }
    if (pWork->STA == 0x40 ) {
        ClearTimeOut();
    }
    switch (state) {
    case 0x00 :
        WShutdown();
        break;
    case 0x10 :
        WSetForcePowerState((0x0000 << 15) );
        WStop();
        WWakeUp();
        break;
    case 0x40 :
        if (pWork->Mode == 2 ) {
            WEnableTmpttPowerSave();
        }
        SetupPeriodicTimeOut(100 , WIntervalTimer);
        break;
    }
    pWork->STA = state;
}

#include "context002.h"
