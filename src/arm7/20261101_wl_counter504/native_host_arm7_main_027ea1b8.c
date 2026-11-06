#include "wl_complete_types.h"

void native_host_arm7_main_027ea1b8(void)
{
    WlCounter *pCounter = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Counter;
    u16 *pMRegCounter = (u16 *)((0x04808000) + 0x1B0) ;
    u16 tmp;
    tmp = *pMRegCounter++;
    pCounter->rx.plcpErr += (u32)LoadLow(&tmp);
    tmp = *pMRegCounter++;
    pCounter->rx.lengthErr += (u32)LoadHigh(&tmp);
    pCounter->rx.rateErr += (u32)LoadLow(&tmp);
    tmp = *pMRegCounter++;
    pCounter->rx.pathErr += (u32)LoadHigh(&tmp);
    pCounter->rx.bufOvfErr += (u32)LoadLow(&tmp);
    tmp = *pMRegCounter++;
    pCounter->rx.fcsOk += (u32)LoadHigh(&tmp);
    pCounter->rx.fcsErr += (u32)LoadLow(&tmp);
    tmp = *pMRegCounter++;
    pCounter->rx.fcErr += (u32)LoadLow(&tmp);
    tmp = *pMRegCounter++;
    pCounter->rx.rts += (u32)LoadLow(&tmp);
    tmp = *pMRegCounter++;
    pCounter->rx.wep += (u32)LoadHigh(&tmp);
    pCounter->rx.icvErr += (u32)LoadLow(&tmp);
    tmp = *pMRegCounter++;
    pCounter->rx.duplicateErr += (u32)LoadLow(&tmp);
    pCounter->rx.mpDuplicateErr += (u32)LoadHigh(&tmp);
    tmp = *pMRegCounter++;
    pCounter->tx.ackErr += (u32)LoadLow(&tmp);
    pMRegCounter += (0xE / 2);
    tmp = *pMRegCounter++;
    pCounter->multiPoll.keyResponseErr[0] += (u32)LoadHigh(&tmp);
    tmp = *pMRegCounter++;
    pCounter->multiPoll.keyResponseErr[1] += (u32)LoadLow(&tmp);
    pCounter->multiPoll.keyResponseErr[2] += (u32)LoadHigh(&tmp);
    tmp = *pMRegCounter++;
    pCounter->multiPoll.keyResponseErr[3] += (u32)LoadLow(&tmp);
    pCounter->multiPoll.keyResponseErr[4] += (u32)LoadHigh(&tmp);
    tmp = *pMRegCounter++;
    pCounter->multiPoll.keyResponseErr[5] += (u32)LoadLow(&tmp);
    pCounter->multiPoll.keyResponseErr[6] += (u32)LoadHigh(&tmp);
    tmp = *pMRegCounter++;
    pCounter->multiPoll.keyResponseErr[7] += (u32)LoadLow(&tmp);
    pCounter->multiPoll.keyResponseErr[8] += (u32)LoadHigh(&tmp);
    tmp = *pMRegCounter++;
    pCounter->multiPoll.keyResponseErr[9] += (u32)LoadLow(&tmp);
    pCounter->multiPoll.keyResponseErr[10] += (u32)LoadHigh(&tmp);
    tmp = *pMRegCounter++;
    pCounter->multiPoll.keyResponseErr[11] += (u32)LoadLow(&tmp);
    pCounter->multiPoll.keyResponseErr[12] += (u32)LoadHigh(&tmp);
    tmp = *pMRegCounter++;
    pCounter->multiPoll.keyResponseErr[13] += (u32)LoadLow(&tmp);
    pCounter->multiPoll.keyResponseErr[14] += (u32)LoadHigh(&tmp);
}
