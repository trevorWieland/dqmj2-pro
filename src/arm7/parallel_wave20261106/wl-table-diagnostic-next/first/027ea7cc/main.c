#include "context000.h"

#include "context001.h"

#include "context002.h"

void native_host_arm7_main_027ea7cc(void)
{
    u32 eep_adrs, num, reg, bytes, adrs, i, j;
    LPRF_CONFIG pRf = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Rf;
    u32 data;
    for (i = data = 0; i < sizeof(native_host_arm7_data_027f72ec) / 2; i++) {
        native_host_arm7_arm_027f4e1c((u32)(&((LPFLASH_TABLE)0x002a)->macTxRxRegs[i]) , 2, (u8 *)&data);
        *(vu16 *)((0x04808000) + native_host_arm7_data_027f72ec[i]) = data;
    }
    {
        reg = (0x0000 << 14) | (((u32)pRf->Bits >> 7) * (0x0001 << 8) );
        reg |= pRf->Bits & 0x7F;
        *(vu16 *)(0x04808000 + 0x184) = (u16)reg;
        eep_adrs = (u32)(&((LPFLASH_TABLE)0x002a)->rfInit_channelDependData) ;
        bytes = (u32)(((pRf->Bits & 0x7F) + 7) / 8);
        num = pRf->InitNum;
        if (pRf->Id == 3 ) {
            native_host_arm7_arm_027f4e1c((u32)(&((LPFLASH_TABLE)0x002a)->rfInit_channelDependData.MM3156Tbl.init[0]) + pRf->InitNum, 1, (u8 *)&pRf->BbpCnt);
            for (i = j = 0; i < num; i++, eep_adrs++) {
                reg = 0;
                native_host_arm7_arm_027f4e1c(eep_adrs, 1, (u8 *)&reg);
                reg |= ((i << 8) + (5 << 16));
                native_host_arm7_arm_027ea62c(reg);
            }
        } else {
            for (reg = 0; num > 0; num--, eep_adrs += bytes) {
                native_host_arm7_arm_027f4e1c(eep_adrs, bytes, (u8 *)&reg);
                native_host_arm7_arm_027ea62c(reg);
                if (pRf->Id == 2 ) {
                    adrs = reg >> 18;
                    if (adrs == 9) {
                        pRf->BkReg = reg & ~(0x1F << 10);
                    }
                }
            }
        }
    }
}

u32 WaitLoop_RfAccess(void);


void native_host_arm7_arm_027ea62c(u32 data)
{
    *(vu16 *)(0x04808000 + 0x17E) = (u16)data;
    *(vu16 *)(0x04808000 + 0x17C) = (u16)(data >> 16);

    WaitLoop_RfAccess();
}