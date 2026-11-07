#include "context000.h"

#include "context001.h"

void native_host_arm7_main_027eb55c(void)
{
    u16 *BBPDiagSkipAdrs;
    u32 adrs, i, err;
    u16 w8, r8;
    u32 j;
    u16 bit;
    ;
    err = 0;
    if (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Rf.Id == 5 ) {
        BBPDiagSkipAdrs = (u16 *)native_host_arm7_data_027f74f6;
    } else
        BBPDiagSkipAdrs = (u16 *)native_host_arm7_data_027f7528;
    for (adrs = 0; adrs < 105 ; adrs++) {
        if (native_host_arm7_arm_027ea5fc(adrs, 0x0FF) == -1) {
            ;
            err = 1;
            goto bbp_diag_end;
        }
    }
    w8 = 0x00FF;
    for (i = adrs = 0; adrs < 105 ; adrs++) {
        if (adrs == BBPDiagSkipAdrs[i]) {
            i++;
            continue;
        }
        r8 = native_host_arm7_arm_027ea5d0(adrs);
        if (r8 != w8) {
            ;
            if (err++ > 32 ) {
                goto bbp_diag_end;
            }
        }
    }
    for (adrs = 0; adrs < 105 ; adrs++) {
        native_host_arm7_arm_027ea5fc(adrs, 0x00);
    }
    w8 = 0x00;
    for (i = adrs = 0; adrs < 105 ; adrs++) {
        if (adrs == BBPDiagSkipAdrs[i]) {
            i++;
            continue;
        }
        r8 = native_host_arm7_arm_027ea5d0(adrs);
        if (r8 != w8) {
            ;
            if (err++ > 32 ) {
                goto bbp_diag_end;
            }
        }
    }
    w8 = 0x55;
    for (adrs = 0; adrs < 105 ; adrs++, w8 = ~w8) {
        native_host_arm7_arm_027ea5fc(adrs, w8);
    }
    w8 = 0x55;
    for (i = adrs = 0; adrs < 105 ; adrs++, w8 = (~w8 & 0x00FF)) {
        if (adrs == BBPDiagSkipAdrs[i]) {
            i++;
            continue;
        }
        r8 = native_host_arm7_arm_027ea5d0(adrs);
        if (r8 != w8) {
            ;
            if (err++ > 32 ) {
                goto bbp_diag_end;
            }
        }
    }
    w8 = 0x0FF;
    for (adrs = 0; adrs < 105 ; adrs++, w8--) {
        native_host_arm7_arm_027ea5fc(adrs, w8);
    }
    w8 = 0x0FF;
    for (i = adrs = 0; adrs < 105 ; adrs++, w8--) {
        if (adrs == BBPDiagSkipAdrs[i]) {
            i++;
            continue;
        }
        r8 = native_host_arm7_arm_027ea5d0(adrs);
        if (r8 != w8) {
            ;
            if (err++ > 32 ) {
                goto bbp_diag_end;
            }
        }
    }
    for (i = adrs = 0; adrs < 105 ; adrs++) {
        if (adrs == BBPDiagSkipAdrs[i]) {
            i++;
            continue;
        }
        bit = 1;
        for (j = 0; j < 9; bit = (bit << 1) & 0x00FF, j++) {
            native_host_arm7_arm_027ea5fc(adrs, (u32)bit);
            r8 = native_host_arm7_arm_027ea5d0(adrs);
            if (r8 != bit) {
                ;
                if (err++ > 32 ) {
                    goto bbp_diag_end;
                }
            }
        }
    }
bbp_diag_end:
    if (err > 32 ) {
        ;
    }
    if (err != 0) {
        ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config.DiagResult |= 0x0008 ;
    } else {
        ;
    }
}
