#include "context000.h"

#include "context001.h"

void native_host_arm7_main_027eb3d0(void)
{
    u32 i, err;
    u16 *p16;
    u16 w16, r16;
    ;
    err = 0;
    p16 = (u16 *)(0x04800000 + 0x4000) ;
    w16 = 0xFFFF;
    for (i = 0; i < 0x00002000 ; i += 2) {
        *p16++ = w16--;
    }
    p16 = (u16 *)(0x04800000 + 0x4000) ;
    w16 = 0xFFFF;
    for (i = 0; i < 0x00002000 ; i += 2, p16++, w16--) {
        r16 = *p16;
        if (r16 != w16) {
            ;
            if (err++ > 32 ) {
                goto mac_diag_end;
            }
        }
    }
    p16 = (u16 *)(0x04800000 + 0x4000) ;
    w16 = 0x5A5A;
    for (i = 0; i < 0x00002000 ; i += 2, w16 = ~w16) {
        *p16++ = w16;
    }
    p16 = (u16 *)(0x04800000 + 0x4000) ;
    w16 = 0x5A5A;
    for (i = 0; i < 0x00002000 ; i += 2, p16++, w16 = ~w16) {
        r16 = *p16;
        if (r16 != w16) {
            ;
            if (err++ > 32 ) {
                goto mac_diag_end;
            }
        }
    }
    p16 = (u16 *)(0x04800000 + 0x4000) ;
    w16 = 0xA5A5;
    for (i = 0; i < 0x00002000 ; i += 2, w16 = ~w16) {
        *p16++ = w16;
    }
    p16 = (u16 *)(0x04800000 + 0x4000) ;
    w16 = 0xA5A5;
    for (i = 0; i < 0x00002000 ; i += 2, p16++, w16 = ~w16) {
        r16 = *p16;
        if (r16 != w16) {
            ;
            if (err++ > 32 ) {
                goto mac_diag_end;
            }
        }
    }
mac_diag_end:
    if (err > 32 ) {
        ;
    }
    if (err != 0) {
        ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config.DiagResult |= 0x0002 ;
    } else {
        ;
    }
}
