#include "context000.h"

#include "context001.h"

#include "context002.h"

void AddTask(s32 nPriority, u32 nTaskID)
{
    LPTASK_MAN pTaskMan = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->TaskMan;
    LPTASK_TBL pTaskTbl;
    u32 x;
    ;
    pTaskTbl = pTaskMan->TaskTbl;
    x = OS_DisableIrqMask((1UL << 24) | (1UL << 4) );
    if (pTaskTbl[nTaskID].Flag == 0x0000 ) {
        pTaskTbl[nTaskID].Flag = 0x0001 ;
        pTaskTbl[nTaskID].NextId = 0xFFFF ;
        if (pTaskMan->DeQ[nPriority] == 0xFFFF ) {
            pTaskMan->EnQ[nPriority] = (u16)nTaskID;
        } else {
            pTaskMan->TaskTbl[pTaskMan->DeQ[nPriority]].NextId = (u16)nTaskID;
        }
        pTaskMan->DeQ[nPriority] = (u16)nTaskID;
        if (nPriority < pTaskMan->NextPri) {
            pTaskMan->NextPri = (u16)nPriority;
        }
    }
    OS_EnableIrqMask(x);
    if ((nPriority != 3 ) && (pTaskMan->TaskPri == 3 )) {
        OS_SendMessage(((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->pRecvMsgQueue, 0 , 0 );
    }
}

#include "context003.h"
