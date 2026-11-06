#include "context000.h"

#include "context001.h"

#include "context002.h"

void MainTaskRoutine(void *arg)
{
    LPTASK_MAN pTaskMan = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->TaskMan;
    u32 x;
    pTaskMan->NextPri = 0;
    pTaskMan->CurrTaskID = 0;
    ;
    while (1) {
        OSMessage msg;
        if (OS_ReceiveMessage(((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->pRecvMsgQueue, &msg, 0 )) {
            ExecuteMessage(&msg);
        }
        x = OS_DisableIrqMask((1UL << 24) | (1UL << 4) );
        pTaskMan->TaskPri = pTaskMan->NextPri;
        if (pTaskMan->EnQ[pTaskMan->TaskPri] == 0xFFFF ) {
            ++pTaskMan->NextPri;
            OS_EnableIrqMask(x);
        } else {
            OS_EnableIrqMask(x);
            pTaskMan->CurrTaskID = (u16)DeleteTask(pTaskMan->TaskPri);
            ;
            (*pTaskMan->TaskTbl[pTaskMan->CurrTaskID].pTaskFunc)();
            ;
            pTaskMan->CurrTaskID = 0xFFFF ;
        }
    }
}

#include "context003.h"
