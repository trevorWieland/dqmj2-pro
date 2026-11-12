/* ov000 row 0x021ed1e0: 340 bytes.
 *
 * What it does: 82 instructions and 8 call(s), then a 5-entry dispatch through an inline branch table at 0x021ed204 (dispatch word at 0x021ed1fc)
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

extern void native_fn_02049ad0(void);
extern void native_fn_02065d88(void);
extern void native_fn_02066a6c(void);
extern void native_fn_02046af4(void);
extern void native_fn_020c4870(void);
extern void native_fn_020c48d0(void);
extern void native_fn_020c48e8(void);
extern void native_fn_021ef11c(void);


asm u32 native_ov000_021ed1e0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    sub sp, sp, #72
    ldr r0, [pc, #0x138]
    mov r5, #0
    ldr r1, [r0, #0x4]
    ldrsb r0, [r1, #32]
    cmp r0, #4
    addls pc, pc, r0, lsl #2
    b L_021ed31c
    dcd 0xea000044
    dcd 0xea000002
    dcd 0xea000001
    dcd 0xea000041
    dcd 0xea000040
    ldrb r0, [r1, #0x101]
    cmp r0, #0
    bne L_021ed31c
    ldr r6, [pc, #0x100]
    add r1, sp, #8
    mov r0, #8
L_021ed230:
    strh r5, [r1]
    strh r5, [r1, #2]
    strh r5, [r1, #4]
    strh r5, [r1, #6]
    add r1, r1, #8
    subs r0, r0, #1
    bne L_021ed230
    ldr r0, [pc, #0xd4]
    ldr r4, [r0, #0x4]
    ldr r1, [r4, #0x10]
    ldr r0, [r4, #0x14]
    sub r0, r1, r0
    add r0, r0, #2
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    ldr r0, [r0]
    ldr r0, [r0, #0x4]
    ldr r7, [r0, #0x68]
    cmp r7, #0
    beq L_021ed31c
    ldr r0, [pc, #0x9c]
    ldr r1, [r4, #0x10]
    ldr r0, [r0, #0x4]
    add r0, r0, r1, lsl #2
    ldr r0, [r0, #0x104]
    mov r0, r0, lsl #16
    mov r4, r0, lsr #16
    mov r0, r4
    bl native_fn_02065d88
    ldrb r0, [r0, #0x24]
    bl native_fn_02066a6c
    add r0, r0, #123
    add r1, r0, #256
    mov r2, #0
    ldr r0, [pc, #0x6c]
    mov r1, r1, lsl #1
    ldrh r1, [r0, r1]
    add r5, sp, #10
    mov r0, r6
    strh r1, [sp, #8]
    str r5, [sp]
    mov r5, #255
    mov r1, r7
    mov r3, r2
    str r5, [sp, #0x4]
    bl native_fn_02046af4
    add r0, sp, #8
    mov r1, #32
    bl native_fn_020c4870
    mov r2, r4
    mov r0, #14
    mov r1, #0
    bl native_fn_020c48d0
    mov r0, #87
    bl native_fn_020c48e8
    mov r0, #0
    bl native_fn_021ef11c
    mov r5, #1
L_021ed31c:
    mov r0, r5
    add sp, sp, #72
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
    dcd 0x02236bc4
    dcd 0x021c9698
    dcd 0x020dbc18
}
