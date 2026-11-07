#include "context000.h"

#include "context001.h"

void native_host_arm7_main_027eb22c(void)
{
    vu16 *pReg;
    u16 wd, rd;
    u32 j, err;
    u32 i;
    ;
    err = 0;
    for (i = 0; i < sizeof(native_host_arm7_data_027f74f0) / 2; i++) {
        for (j = 0; j < sizeof(native_host_arm7_data_027f7560) / sizeof(TEST_REGS); j++) {
            pReg = (vu16 *)((0x04808000) + (u32)native_host_arm7_data_027f7560[j].adrs);
            wd = native_host_arm7_data_027f74f0[i] & native_host_arm7_data_027f7560[j].mask;
            *pReg = wd;
            rd = *pReg;
            if (rd != (native_host_arm7_data_027f74f0[i] & native_host_arm7_data_027f7560[j].mask)) {
                ;
                if (err++ > 32 ) {
                    goto mac_reg_diag_end;
                }
            }
        }
    }
    for (j = 0, wd = 0x1234; j < sizeof(native_host_arm7_data_027f7560) / sizeof(TEST_REGS); j++) {
        pReg = (vu16 *)((0x04808000) + (u32)native_host_arm7_data_027f7560[j].adrs);
        *pReg = wd & native_host_arm7_data_027f7560[j].mask;
        wd += 0x1234;
    }
    for (j = 0, wd = 0x1234; j < sizeof(native_host_arm7_data_027f7560) / sizeof(TEST_REGS); j++) {
        pReg = (vu16 *)((0x04808000) + (u32)native_host_arm7_data_027f7560[j].adrs);
        rd = *pReg;
        if (rd != (wd & native_host_arm7_data_027f7560[j].mask)) {
            ;
            if (err++ > 32 ) {
                goto mac_reg_diag_end;
            }
        }
        wd += 0x1234;
    }
    for (j = 0; j < sizeof(native_host_arm7_data_027f7560) / sizeof(TEST_REGS); j++) {
        pReg = (vu16 *)((0x04808000) + (u32)native_host_arm7_data_027f7560[j].adrs);
        *pReg = 0;
        rd = *pReg;
        if (rd != 0) {
            ;
            if (err++ > 32 ) {
                goto mac_reg_diag_end;
            }
        }
    }
mac_reg_diag_end:
    if (err != 0) {
        ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config.DiagResult |= 0x0001 ;
    }
}
