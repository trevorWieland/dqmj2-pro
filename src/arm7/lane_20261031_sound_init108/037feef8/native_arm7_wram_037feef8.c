#include "native_sound_init_types.h"
static void SND_CreateThread(u32 priority)
{
    OS_CreateThread(&sThread,
        SndThread,
        NULL,
        &sThreadStack[sizeof(sThreadStack)],
        sizeof(sThreadStack),
        priority);
    OS_WakeupThreadDirect(&sThread);
}

void native_arm7_wram_037feef8(u32 priority)
{
    if (sInitialized == 0)
    {
        sInitialized = 1;
        SND_CommandInit();
        SND_CreateThread(priority);
    }
}
