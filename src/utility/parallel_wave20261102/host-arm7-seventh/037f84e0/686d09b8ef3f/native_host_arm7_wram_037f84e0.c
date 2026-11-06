#include "dependency000.h"
#include "dependency001.h"
#include "dependency002.h"

void native_host_arm7_wram_037f84e0(void *arg)
{
    LPTASK_MAN pTaskMan = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->TaskMan;
    u32 x;
    pTaskMan->NextPri = 0;
    pTaskMan->CurrTaskID = 0;
    ;
    while (1) {
        OSMessage msg;
        if (native_host_arm7_arm_037fc760(((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->pRecvMsgQueue, &msg, 0 )) {
            native_host_arm7_arm_037f8704(&msg);
        }
        x = native_host_arm7_arm_037fb928((1UL << 24) | (1UL << 4) );
        pTaskMan->TaskPri = pTaskMan->NextPri;
        if (pTaskMan->EnQ[pTaskMan->TaskPri] == 0xFFFF ) {
            ++pTaskMan->NextPri;
            native_host_arm7_arm_037fb8f0(x);
        } else {
            native_host_arm7_arm_037fb8f0(x);
            pTaskMan->CurrTaskID = (u16)native_host_arm7_arm_037f8650(pTaskMan->TaskPri);
            ;
            (*pTaskMan->TaskTbl[pTaskMan->CurrTaskID].pTaskFunc)();
            ;
            pTaskMan->CurrTaskID = 0xFFFF ;
        }
    }
}
#include "dependency003.h"
