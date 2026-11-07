#include "context000.h"

#include "context001.h"

#include "context002.h"

u16 native_host_arm7_main_027e990c(u16 channel, u32 bDirect)
{
#pragma unused(bDirect)
    u32 reg;
    u32 bkpwr;
    u32 flash_adrs, i, adrs;
    void (*pFlashReadFunc)(u32 adrs, u32 size, u8 *pBuf);
    if (bDirect) {
        pFlashReadFunc = native_host_arm7_arm_027f4e7c;
    } else {
        pFlashReadFunc = native_host_arm7_arm_027f4e1c;
    }
    if (CheckEnableChannel(channel) == 0) {
        return 0x05 ;
    }
    bkpwr = *(vu16 *)((0x04808000) + 0x040) ;
    *(vu16 *)((0x04808000) + 0x040) = ((0x0001 << 0) | (0x0001 << 15)) ;
    while (1) {
        u32 ps, st;
        ps = *(vu16 *)((0x04808000) + 0x03C) >> 8;
        st = *(vu16 *)(0x04808000 + 0x214) ;
        if ((ps == 2) && ((st == 0) || (st == 9))) {
            break;
        }
    }
    ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work.CurrChannel = channel;
    switch (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Rf.Id) {
    case 5 :
    case 2 :
        reg = 0;
        (*pFlashReadFunc)((u32)(&((LPFLASH_TABLE)0x002a)->rfInit_channelDependData.RF2958Tbl.ch_Reg[channel - 1][0]) , 3, (u8 *)&reg);
        native_host_arm7_arm_027ea62c(reg);
        (*pFlashReadFunc)((u32)(&((LPFLASH_TABLE)0x002a)->rfInit_channelDependData.RF2958Tbl.ch_Reg[channel - 1][3]) , 3, (u8 *)&reg);
        native_host_arm7_arm_027ea62c(reg);
        reg = 0;
        if (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Rf.BkReg & 0x10000) {
            if ((((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Rf.BkReg & 0x08000) == 0) {
                (*pFlashReadFunc)((u32)(&((LPFLASH_TABLE)0x002a)->rfInit_channelDependData.RF2958Tbl.ch_PwrRF[channel - 1]) , 1, (u8 *)&reg);
                reg = ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Rf.BkReg | ((reg & 0x1F) << 10);
                native_host_arm7_arm_027ea62c(reg);
            }
        } else {
            (*pFlashReadFunc)((u32)(&((LPFLASH_TABLE)0x002a)->rfInit_channelDependData.RF2958Tbl.ch_PwrBB[channel - 1]) , 1, (u8 *)&reg);
            native_host_arm7_arm_027ea5fc(30, reg);
        }
        break;
    case 3 :
        flash_adrs = (u32)(&((LPFLASH_TABLE)0x002a)->rfInit_channelDependData.MM3156Tbl.init[0]) + ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Rf.InitNum + 1;
        for (i = 0; i < ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Rf.BbpCnt; i++) {
            adrs = reg = 0;
            (*pFlashReadFunc)(flash_adrs, 1, (u8 *)&adrs);
            (*pFlashReadFunc)(flash_adrs + channel, 1, (u8 *)&reg);
            native_host_arm7_arm_027ea5fc(adrs, reg);
            flash_adrs += 15;
        }
        for (i = 0; i < ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Rf.ChanNum; i++) {
            reg = 0;
            (*pFlashReadFunc)(flash_adrs, 1, (u8 *)&reg);
            reg <<= 8;
            (*pFlashReadFunc)(flash_adrs + channel, 1, (u8 *)&reg);
            reg |= (5 << 16);
            native_host_arm7_arm_027ea62c(reg);
            flash_adrs += 15;
        }
        break;
    }
    *(vu16 *)((0x04808000) + 0x040) = bkpwr;
    *(vu16 *)((0x04808000) + 0x048) = 3;
    return 0;
}

#include "context003.h"
