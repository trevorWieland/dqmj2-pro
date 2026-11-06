#include "dependency000.h"

void native_utility_child_arm7_wram_037fbd44 (OSIrqMask intrBit, OSIrqFunction function)
{
    int i;
    OSIrqCallbackInfo * info;
    for (i = 0; i < 25 ; i++) {
        if (intrBit & 1) {
            info = ((void *)0) ;
            if (8 <= i && i <= 11 ) {
                info = &native_utility_child_arm7_data_0380594c[i - 8 ];
            } else if (3 <= i && i <= 6 )   {
                info = &native_utility_child_arm7_data_0380594c[i - 3 + 4 ];
            }
            else if (0 == i) {
                info = &native_utility_child_arm7_data_0380594c[8 ];
            }
            else {
                native_utility_child_arm7_data_03805830[i] = function;
            }
            if (info) {
                info->func = (void (*)(void *)) function;
                info->arg = 0;
                info->enable = 1 ;
            }
        }
        intrBit >>= 1;
    }
}
