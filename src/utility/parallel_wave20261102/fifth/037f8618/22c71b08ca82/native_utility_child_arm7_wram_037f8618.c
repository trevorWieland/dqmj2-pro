#include "dependency000.h"
#include "dependency001.h"
#include "dependency002.h"

u32 native_utility_child_arm7_wram_037f8618(u32 nPriority)
{
    LPTASK_MAN pTaskMan = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->TaskMan;
    LPTASK_TBL pTaskTbl;
    u32 x, nTaskID, nOfstTaskID;
    x = native_utility_child_arm7_arm_037fbc50((1UL << 24) | (1UL << 4) );
    if ((nTaskID = pTaskMan->EnQ[nPriority]) != 0xFFFF ) {
        pTaskTbl = pTaskMan->TaskTbl;
        nOfstTaskID = nTaskID;
        pTaskTbl[nOfstTaskID].Flag = 0x0000 ;
        if (pTaskTbl[nOfstTaskID].NextId == 0xFFFF ) {
            pTaskMan->EnQ[nPriority] = 0xFFFF ;
            pTaskMan->DeQ[nPriority] = 0xFFFF ;
        } else {
            pTaskMan->EnQ[nPriority] = pTaskTbl[nOfstTaskID].NextId;
            pTaskTbl[nOfstTaskID].NextId = 0xFFFF ;
        }
    }
    native_utility_child_arm7_arm_037fbc8c(x);
    return nTaskID;
}
#include "dependency003.h"
