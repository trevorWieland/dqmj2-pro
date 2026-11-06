#include "dependency000.h"

void native_utility_child_arm7_wram_037fbaac (void)
    {
        void (*callback) (void) =
            (void (*)(void)) native_utility_child_arm7_data_0380594c[8 ].func;
        (*(u32 *)(0x02000000 + 0x007ffc3c) )++;
        if (callback) {
            (callback) ();
        }
        OS_SetIrqCheckFlag(1UL << 0 );
    }
