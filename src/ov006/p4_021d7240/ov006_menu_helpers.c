/*
 * ov006 packet p4-2: small menu and state helpers.
 *
 * These are the small leaf routines around the packet-1 menu code: panel
 * teardown, slot setup, one-off table accessors and tiny counters. Offsets and
 * globals are measured from the overlay image; no meaning is invented beyond
 * the observed load/store and call contract.
 */
#include "context.h"

extern void native_fn_02002c98(u32 a, u32 b, u32 c);
extern void native_fn_020bb38c(s32 value, u32 arg);
extern u32 native_fn_02063b40(u32 id);
extern u8 *native_fn_02063f04(u32 index);
extern void native_fn_02049f4c(void);
extern void native_fn_ov006_021dff30(void);
extern u8 native_data_ov006_0220f2f4[];
extern void native_fn_02004d98(u32 address, u32 b, u32 size);
extern void native_fn_0202a498(u32 a);
extern u32 native_fn_0205dc70(u32 a, u32 b, u16 c);
extern void native_fn_0205e7a8(u32 a, u32 b);
extern void native_fn_0205fa4c(u32 a, u32 b);
extern void native_fn_02064654(s32 a, u8 *b);
extern void native_fn_02065bc4(u8 *slot, u32 a, s8 b, s32 c);
extern void native_fn_02065818(u8 *a, s8 b, s8 c);
extern void native_fn_0206de44(s8 a);
extern void native_fn_0206de64(s8 a);
extern u32 native_fn_02049ad0(s8 a);
extern s32 native_fn_02062aa0(void);
extern u32 native_fn_020bb144(u32 index);

extern void native_fn_ov006_021db5b4(void);
extern void native_fn_ov006_021e9268(void);
extern void native_fn_ov006_021da3e8(s32 value);

extern u8 native_data_ov006_0220cb94[];
extern u8 native_data_ov006_0220795c[];
extern u8 native_data_ov006_0220d104[];
extern u8 native_data_ov006_0220f3b8[];
extern u8 native_data_ov006_0220f500[];
extern u8 native_data_ov006_0221c1f0[];
extern u8 native_data_ov006_02218d30[];

/* 0x021da15c: build the active-slot flag byte and the total slot value. */
void native_ov006_021da15c(void) {
    ((u8 *)*(u32 *)(native_data_ov006_0220f2f4 + 4))[2] = 0;
    ((u8 *)*(u32 *)(native_data_ov006_0220f2f4 + 4))[3] = 0;
    if (native_fn_02063b40(0x221) != 0) {
        ((u8 *)*(u32 *)(native_data_ov006_0220f2f4 + 4))[2] |= 1;
        ((u8 *)*(u32 *)(native_data_ov006_0220f2f4 + 4))[3] += *(u32 *)(native_fn_02063f04(1) + 0x10);
    }
    if (native_fn_02063b40(0x222) != 0) {
        ((u8 *)*(u32 *)(native_data_ov006_0220f2f4 + 4))[2] |= 2;
        ((u8 *)*(u32 *)(native_data_ov006_0220f2f4 + 4))[3] += *(u32 *)(native_fn_02063f04(2) + 0x10);
    }
    if (native_fn_02063b40(0x223) != 0) {
        ((u8 *)*(u32 *)(native_data_ov006_0220f2f4 + 4))[2] |= 4;
        ((u8 *)*(u32 *)(native_data_ov006_0220f2f4 + 4))[3] += *(u32 *)(native_fn_02063f04(3) + 0x10);
    }
    *(u32 *)((u8 *)*(u32 *)(native_data_ov006_0220f2f4 + 4) + 0xC) = *(u16 *)((u8 *)*(u32 *)(native_data_ov006_0220f2f4 + 4) + 6);
    *(u32 *)((u8 *)*(u32 *)(native_data_ov006_0220f2f4 + 4) + 0xC) += *(u16 *)((u8 *)*(u32 *)(native_data_ov006_0220f2f4 + 4) + 4);
    *(u32 *)((u8 *)*(u32 *)(native_data_ov006_0220f2f4 + 4) + 0xC) += *(u32 *)((u8 *)*(u32 *)(native_data_ov006_0220f2f4 + 4) + 8);
    ((u8 *)*(u32 *)(native_data_ov006_0220f2f4 + 4))[1] = 1;
    *(u32 *)((u8 *)*(u32 *)(native_data_ov006_0220f2f4 + 4) + 0xC) += ((u8 *)*(u32 *)(native_data_ov006_0220f2f4 + 4))[3];
    ((u8 *)*(u32 *)(native_data_ov006_0220f2f4 + 4))[0] = 5;
    ((u8 *)*(u32 *)(native_data_ov006_0220f2f4 + 4))[1] = 1;
    native_fn_ov006_021dff30();
}

/* 0x021da5ac: release the menu buffer and reset the display state. */
void native_ov006_021da5ac(void) {
    u32 *state = (u32 *)0x0220F33C;
    u16 *dispcnt = (u16 *)0x04000000;

    native_fn_ov006_021d7860();
    native_fn_02002c98(1, 3, 0);
    *(u16 *)0x0400000E = (u16)((*(u16 *)0x0400000E & 0x43) | 0x4884);
    native_fn_02008c58(0, (u8 *)0x06000000, 0x80000);
    native_fn_02004d98(state[2] + 8, 0, 0x18000);
    *(u32 *)dispcnt = (*(u32 *)dispcnt & ~0x1F00) | 0x1800;
    *(u16 *)0x0400000E = (u16)(*(u16 *)0x0400000E & ~3);
    *(u32 *)0x0400001C = 0;
    native_fn_020bb38c((s32)state[2], 1);
    state[2] = 0;
}

/* 0x021db638: clear the panel type and select mode 2. */
void native_ov006_021db638(void) {
    native_fn_ov006_021db5b4();
    native_fn_ov006_021d7860();
    *(s8 *)native_data_ov006_0220f3b8 = -1;
    *(u32 *)(native_data_ov006_0220f3b8 + 0x1C) = 2;
}

/* 0x021dd420: last element of an array, or 0 for a null array. */
u32 native_ov006_021dd420(u32 *array, u32 count) {
    return array != 0 ? array[count - 1] : 0;
}

/* 0x021ddf28: add to one table word and return the new value. */
u32 native_ov006_021ddf28(u32 index, u32 delta) {
    return ((u32 *)native_data_ov006_0220f500)[index] += delta;
}

/* 0x021e3f54: tail-call the current handler stored in the slot. */
u32 native_ov006_021e3f54(void) {
    return ((u32 (*)(void))*(u32 *)native_data_ov006_0220d104)();
}

/* 0x021e3f28: publish a table word, then tail-call the paired handler. */
void native_ov006_021e3f28(u32 index) {
    u32 *entry = (u32 *)(native_data_ov006_0220795c + index * 8);
    *(u32 *)native_data_ov006_0220d104 = entry[1];
    ((void (*)(void))entry[0])();
}

/* 0x021e7b64: probe one slot and report whether it was accepted. */
u32 native_ov006_021e7b64(u32 value) {
    s8 index = (s8)value;
    if (native_fn_02049ad0(index) == 0) {
        return 0;
    }
    native_fn_02049f4c();
    return 1;
}

/* 0x021e7ed8: register a 12-byte table entry with two signed parameters. */
u32 native_ov006_021e7ed8(u32 index, u32 a, u32 b) {
    native_fn_02065818((u8 *)(0x2218FC8 + index * 12), (s8)a, (s8)b);
    return 1;
}

/* 0x021eadb0: notify both handlers with the same signed selector. */
void native_ov006_021eadb0(u32 value) {
    native_fn_0206de44((s8)value);
    native_fn_0206de64((s8)value);
}

/* 0x021e91f4: publish a boolean flag. */
u32 native_ov006_021e91f4(u32 arg) {
    u32 flag = arg != 0 ? 1 : 0;
    native_fn_0205fa4c(0x2218E60, flag);
    return 1;
}

/* 0x021e92cc: resolve a nested table pointer. */
u32 native_ov006_021e92cc(u32 value) {
    s8 v = (s8)value;
    u32 *outer = (u32 *)native_fn_02049ad0(v);
    return (outer != 0 && *outer != 0) ? *(u32 *)(*outer + 4) : 0;
}

/* 0x021e6530: dispatch a packed record through the shared formatter. */
u32 native_ov006_021e6530(u8 *record) {
    if (*(u32 *)record == 0) {
        return 0x2207E84;
    }
    return native_fn_0205dc70(record[0], record[1], *(u16 *)(record + 2));
}

/* 0x021e4e04: begin the transition for the current record type. */
u32 native_ov006_021e4e04(void) {
    native_fn_ov006_021e9268();
    native_fn_0205e7a8(0xFFFFFFFF, 87);
    native_fn_ov006_021e3f28(*(u32 *)(native_data_ov006_02218d30 + 0x20) != 0 ? 17 : 15);
    return 1;
}
