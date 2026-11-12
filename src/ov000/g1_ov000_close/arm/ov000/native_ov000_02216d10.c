/* ov000 row 0x02216d10: 348 bytes.
 *
 * What it does: 85 instructions and 14 call(s), then a 15-entry dispatch through an inline branch table at 0x02216d34 (dispatch word at 0x02216d2c)
 *
 * Carrier: mwccarm asm with dcd data runs.
 * The measured extent is code plus data inside the function. The data
 * runs are emitted as data, not decoded as instructions; every
 * instruction, branch target, pool word and table entry is read from
 * the image.
 *
 * Unknowns: the field roles, the meaning of the table entries and every callee contract are not established by byte identity; the dispatch range and the table bounds are measured.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02078b30(void);
extern void native_fn_02077858(void);
extern void native_fn_02200244(void);
extern void native_fn_020743f8(void);
extern void native_fn_0207969c(void);
extern void native_fn_022221ac(void);
extern void native_fn_021fc7e8(void);
extern void native_fn_021fec54(void);
extern void native_fn_02201d5c(void);
extern void native_fn_021fe370(void);
extern void native_fn_02217bdc(void);
extern void native_fn_02085320(void);
extern void native_fn_02216cc8(void);


asm u32 native_ov000_02216d10 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    sub sp, sp, #8
    ldr r0, [pc, #0x144]
    mov r4, #0
    ldrsb r0, [r0, #16]
    mov r5, r4
    cmp r0, #14
    addls pc, pc, r0, lsl #2
    b L_02216e18
    dcd 0xea00002b
    dcd 0xea000012
    dcd 0xea000014
    dcd 0xea00001c
    dcd 0xea000009
    dcd 0xea00001d
    dcd 0xea00000a
    dcd 0xea000030
    dcd 0xea000011
    dcd 0xea00001c
    dcd 0xea00001e
    dcd 0xea00002c
    dcd 0xea00002b
    dcd 0xea00002a
    dcd 0xea00000e
    bl native_fn_02078b30
    mov r5, r0
    b L_02216e38
    bl native_fn_02077858
    mov r5, r0
    b L_02216e38
    bl native_fn_02200244
    mov r5, r0
    b L_02216e38
    bl native_fn_020743f8
    mov r5, r0
    b L_02216e38
    bl native_fn_0207969c
    mov r5, r0
    b L_02216e38
    bl native_fn_022221ac
    mov r5, r0
    b L_02216e38
    bl native_fn_021fc7e8
    mov r5, r0
    b L_02216e38
    bl native_fn_021fec54
    mov r5, r0
    b L_02216e38
    bl native_fn_02201d5c
    mov r5, r0
    b L_02216e38
    bl native_fn_021fe370
    mov r5, r0
    b L_02216e38
    mov r3, #1
    str r3, [sp]
    sub r12, r3, #2
    mov r0, #5
    mov r1, #7
    mov r2, #32
    str r12, [sp, #0x4]
    bl native_fn_02217bdc
    mov r1, r4
    mov r2, #1
    bl native_fn_02085320
    b L_02216e38
L_02216e18:
    mov r3, #1
    str r3, [sp]
    sub r12, r3, #2
    mov r0, #5
    mov r1, #7
    mov r2, #32
    str r12, [sp, #0x4]
    bl native_fn_02217bdc
L_02216e38:
    cmp r5, #0
    beq L_02216e48
    bl native_fn_02216cc8
    b L_02216e58
L_02216e48:
    ldr r0, [pc, #0x18]
    mov r1, #6
    strb r1, [r0, #0x494]
    mov r4, #1
L_02216e58:
    mov r0, r4
    add sp, sp, #8
    ldmia sp!, {r3, r4, r5, pc}
    dcd 0x0224536c
    dcd 0x022459b4
}
