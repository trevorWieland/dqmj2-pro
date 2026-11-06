#include "dependency000.h"

OSIrqMask native_utility_child_arm7_wram_037fbc1c (OSIrqMask intr)
{
    BOOL ime = OS_DisableIrq();
    OSIrqMask prep = (*( REGType32v *) (0x04000000 + 0x214)) ;
    (*( REGType32v *) (0x04000000 + 0x214)) = intr;
    (void)OS_RestoreIrq(ime);
    return prep;
}
