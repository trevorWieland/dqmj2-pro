#include "dependency000.h"

void native_utility_child_arm9_main_0200fac4 (void)
{
    int i;
    OSIntrMode enabled;
    OSSystemWork * p = ((OSSystemWork *)(0x02000000 + 0x007ffc00)) ;
    enabled = native_utility_child_arm9_arm_0200a64c();
    if (!native_utility_child_arm9_data_0202cbc8) {
        native_utility_child_arm9_data_0202cbc8 = 1 ;
        p->pxiHandleChecker[PXI_PROC_ARM9 ] = 0UL;
        for (i = 0; i < PXI_MAX_FIFO_TAG; i++) {
            native_utility_child_arm9_data_0202cbcc[i] = ((void *)0) ;
        }
        (*( REGType16v *) (0x04000000 + 0x184)) =
            (0x0008 |
             0x0400 | 0x8000 | 0x4000 );
        (void)native_utility_child_arm9_thumb_02009058((1UL << 18) );
        (void)native_utility_child_arm9_thumb_0200912c((1UL << 18) , native_utility_child_arm9_thumb_0200f8dd);
        (void)native_utility_child_arm9_thumb_020090a8((1UL << 18) );
        {
            int timeout;
            s32 c;
            for (i = 0;; i++) {
                c = (*( REGType16v *) (0x04000000 + 0x180)) & 15;
                (*( REGType16v *) (0x04000000 + 0x180)) = (u16)(c << 8);
                if (c == 0 && i > 4) {
                    break;
                }
                for (timeout = 1000; ((*( REGType16v *) (0x04000000 + 0x180)) & 15) == c; timeout--) {
                    if (timeout == 0) {
                        i = 0;
                        break;
                    }
                }
            }
        }
    }
    (void)native_utility_child_arm9_arm_0200a660(enabled);
}
#include "dependency001.h"
