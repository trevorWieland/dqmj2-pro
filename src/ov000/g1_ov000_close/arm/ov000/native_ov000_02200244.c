/* ov000 row 0x02200244: 456 bytes.
 *
 * What it does: 108 instructions and 14 call(s), then a 8-entry dispatch through an inline branch table at 0x0220027c (dispatch word at 0x02200274)
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

extern void native_fn_02049ae4(void);
extern void native_fn_02049f24(void);
extern void native_fn_02049f30(void);
extern void native_fn_02049ad0(void);
extern void native_fn_02046af4(void);
extern void native_fn_02049f14(void);
extern void native_fn_02217bdc(void);
extern void native_fn_02060510(void);
extern void native_fn_020853c8(void);


asm u32 native_ov000_02200244 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, lr}
    sub sp, sp, #8
    mov r4, #0
    ldr r5, [pc, #0x19c]
    bl native_fn_02049ae4
    mov r6, r0
    bl native_fn_02049f24
    mov r7, r0
    bl native_fn_02049f30
    ldr r0, [pc, #0x188]
    ldr r1, [r0]
    cmp r1, #7
    addls pc, pc, r1, lsl #2
    b L_022003d0
    dcd 0xea000053
    dcd 0xea000005
    dcd 0xea000051
    dcd 0xea000020
    dcd 0xea00004f
    dcd 0xea000001
    dcd 0xea00004d
    dcd 0xea00004c
    cmp r1, #1
    ldreq r0, [pc, #0x154]
    ldrne r0, [pc, #0x154]
    ldr r0, [r0]
    add r0, r0, #5
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    ldr r0, [r0]
    mov r1, #255
    ldr r3, [r0, #0x4]
    mov r0, r5
    str r7, [sp]
    str r1, [sp, #0x4]
    ldrb r2, [r3, #0x5e]
    ldr r1, [r3, #0x68]
    mov r3, #0
    bl native_fn_02046af4
    mov r0, r7
    bl native_fn_02049f14
    mov r3, #1
    str r3, [sp]
    mov r0, #87
    str r0, [sp, #0x4]
    mov r0, #0
    mov r1, r0
    mov r2, #63
    bl native_fn_02217bdc
    b L_022003d4
    ldr r2, [r0, #0x8]
    ldr r8, [r0, #0xf8]
    and r3, r2, #255
    ldr r1, [pc, #0xe0]
    add r0, r8, #5
    mov r0, r0, lsl #24
    and r2, r8, #255
    add r1, r1, r3, lsl #7
    ldr r1, [r1, r2, lsl #2]
    mov r0, r0, asr #24
    mov r1, r1, lsl #16
    mov r8, r1, lsr #16
    mov r9, r4
    bl native_fn_02049ad0
    ldr r0, [r0]
    cmp r8, #8
    ldr r10, [r0, #0x4]
    blo L_02200380
    mov r0, r8
    bl native_fn_02060510
    add r0, r0, #123
    add r2, r0, #256
    add r0, r9, #1
    ldr r1, [pc, #0x94]
    mov r2, r2, lsl #1
    ldrh r1, [r1, r2]
    and r9, r0, #255
    strh r1, [r7]
L_02200380:
    add r0, r7, r9, lsl #1
    str r0, [sp]
    mov r0, #255
    str r0, [sp, #0x4]
    ldrb r2, [r10, #0x5e]
    ldr r1, [r10, #0x68]
    mov r0, r5
    mov r3, #0
    bl native_fn_02046af4
    mov r0, r7
    bl native_fn_02049f14
    mov r3, #1
    mov r2, r8
    str r3, [sp]
    mov r1, #87
    mov r0, #13
    str r1, [sp, #0x4]
    mov r1, #0
    bl native_fn_02217bdc
    b L_022003d4
L_022003d0:
    mov r4, #1
L_022003d4:
    ldr r1, [r6]
    cmp r1, #0
    beq L_022003e8
    ldr r0, [r6, #0x4]
    bl native_fn_020853c8
L_022003e8:
    mov r0, r4
    add sp, sp, #8
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
    dcd 0x021c9698
    dcd 0x02237778
    dcd 0x02237780
    dcd 0x02237960
    dcd 0x02237a54
    dcd 0x020dbc18
}
