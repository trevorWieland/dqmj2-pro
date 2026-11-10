/*
 * ov006 packet p4-1: display bring-up for the menu system.
 *
 * The 0x04000000 block is the DS main engine: 0x04000008 holds the four
 * background control words, 0x04000010..0x0400001C the affine parameters and
 * 0x04000000 DISPCNT. 0x04060000 is the engine-A background palette and the
 * 0x06000000 block is background VRAM (0x80000 bytes are cleared here).
 */
#include "context.h"

extern void native_fn_020bb38c(s32 value, u32 arg);
extern void native_fn_ov006_021da844(void);
extern void native_fn_0204617c(u32 a, u32 b);
extern void native_fn_02003af4(void);
extern void native_fn_02002e5c(u32 value);
extern void native_fn_020030ec(u32 value);
extern void native_fn_02045400(void);
extern void native_fn_020406a8(u32 value);
extern void native_fn_02062074(u32 value);
extern void native_fn_02061238(u32 a, u32 b, u32 c);
extern void native_fn_020612ec(u32 a, u32 b, u32 c, u32 d);
extern u32 native_fn_02062a50(u32 index);
extern void native_fn_0206dcd0(void);
extern void native_fn_02062a10(void);
extern void native_fn_02061950(u32 value);
extern void native_fn_0207a9ec(u32 value);
extern void native_fn_0206157c(void);

/* 0x021da664: reset and program the display for the menu scene. */
void native_ov006_021da664(void) {
    u32 *state = (u32 *)0x0220F33C;
    u16 *bgcnt = (u16 *)0x04000008;

    if (state[2] != 0) {
        native_fn_020bb38c((s32)state[2], 1);
        state[2] = 0;
    }
    native_fn_ov006_021da844();
    native_fn_0204617c(0, 2);
    native_fn_02003af4();
    native_fn_02002e5c(9);
    native_fn_020030ec(2);
    bgcnt[0] = (u16)((bgcnt[0] & 0x43) | 4);
    bgcnt[1] = (u16)((bgcnt[1] & 0x43) | 4);
    bgcnt[2] = (u16)((bgcnt[2] & 0x43) | 0x210);
    bgcnt[3] = (u16)((bgcnt[3] & 0x43) | 0x418);
    native_fn_02008c58(0, (u8 *)0x06000000, 0x80000);
    native_fn_02045400();
    *(u32 *)0x04000000 &= ~0xE000;
    native_fn_020406a8(1);
    native_fn_02062074(1);
    native_fn_02061238(1, 2, 3);
    native_fn_020612ec(1, 1, 0x8000, 0);
    if (state[1] == 0) {
        native_fn_02062a50(0);
        native_fn_0206dcd0();
    } else {
        native_fn_02062a10();
        native_fn_0206dcd0();
    }
    native_fn_02061950(0x10);
    bgcnt[0] = (u16)((bgcnt[0] & ~3) | 3);
    bgcnt[1] = (u16)((bgcnt[1] & ~3) | 1);
    bgcnt[2] = (u16)((bgcnt[2] & ~3) | 2);
    bgcnt[3] = (u16)(bgcnt[3] & ~3);
    *(u32 *)0x04000010 = 0;
    *(u32 *)0x04000014 = 0;
    *(u32 *)0x04000018 = 0;
    *(u32 *)0x0400001C = 0;
    *(u32 *)0x04000000 = (*(u32 *)0x04000000 & ~0x1F00) | 0x1E00;
    native_fn_0207a9ec(2);
    native_fn_0206157c();
    state[1] = 0;
}
