#include "context000.h"

#include "context001.h"

#include "context002.h"

u32 DeleteTask(u32 nPriority)
{
    LPTASK_MAN pTaskMan = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->TaskMan;
    LPTASK_TBL pTaskTbl;
    u32 x, nTaskID, nOfstTaskID;
    x = OS_DisableIrqMask((1UL << 24) | (1UL << 4) );
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
    OS_EnableIrqMask(x);
    return nTaskID;
}

#include "context003.h"
