/* ov000 row 0x022169c8: 288 bytes.
 *
 * What it does: 69 instructions and 6 call(s), then a 15-entry dispatch through an inline branch table at 0x02216a64 (dispatch word at 0x02216a5c)
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

extern void native_fn_0221576c(void);
extern void native_fn_02041814(void);
extern void native_fn_02215a8c(void);
extern void native_fn_021f85c8(void);
extern void native_fn_02048308(void);


asm u32 native_ov000_022169c8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r0, [pc, #0x108]
    mov r4, #0
    ldrsb r0, [r0]
    mov r5, r4
    cmp r0, #0
    bne L_02216a18
    bl native_fn_0221576c
    cmp r0, #0
    bne L_02216a0c
    bl native_fn_02041814
    cmp r0, #1
    beq L_02216a18
    ldr r0, [pc, #0xd8]
    mov r1, #10
    strb r1, [r0]
    b L_02216a18
L_02216a0c:
    ldr r0, [pc, #0xc8]
    mov r1, #10
    strb r1, [r0]
L_02216a18:
    ldr r0, [pc, #0xbc]
    ldrsb r0, [r0]
    cmp r0, #10
    bne L_02216a48
    bl native_fn_0221576c
    ldr r0, [pc, #0xac]
    ldr r1, [pc, #0xa4]
    mov r2, #0
    ldrsb r0, [r0, #16]
    strb r2, [r1]
    mov r5, #1
    bl native_fn_02215a8c
L_02216a48:
    cmp r5, #0
    beq L_02216ac8
    ldr r0, [pc, #0x88]
    ldrsb r0, [r0, #16]
    cmp r0, #14
    addls pc, pc, r0, lsl #2
    b L_02216ab4
    dcd 0xea00000d
    dcd 0xea000011
    dcd 0xea000010
    dcd 0xea00000f
    dcd 0xea00000e
    dcd 0xea00000d
    dcd 0xea00000c
    dcd 0xea00000b
    dcd 0xea00000a
    dcd 0xea000009
    dcd 0xea000008
    dcd 0xea000007
    dcd 0xea000006
    dcd 0xea000005
    dcd 0xea000004
    ldr r0, [pc, #0x3c]
    mov r1, #4
    strb r1, [r0, #0x494]
    bl native_fn_021f85c8
    b L_02216ac0
L_02216ab4:
    ldr r0, [pc, #0x28]
    mov r1, #4
    strb r1, [r0, #0x494]
L_02216ac0:
    bl native_fn_02048308
    mov r4, #2
L_02216ac8:
    ldr r1, [pc, #0x14]
    mov r2, #0
    mov r0, r4
    strb r2, [r1, #0x49c]
    ldmia sp!, {r3, r4, r5, pc}
    dcd 0x0224532c
    dcd 0x0224536c
    dcd 0x022459b4
}
