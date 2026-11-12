/* ov000 row 0x021e5c88: 516 bytes.
 *
 * What it does: 129 instructions and 2 call(s), then a 7-entry dispatch through an inline branch table at 0x021e5cc4 (dispatch word at 0x021e5cbc)
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

extern void native_fn_021e5bcc(void);
extern void native_fn_021e5c10(void);


asm u32 native_ov000_021e5c88 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    mov r8, r0
    mov r7, r1
    mov r6, r2
    mov r5, r3
    mov r4, #0
    bl native_fn_021e5bcc
    cmp r0, #0
    bne L_021e5e84
    bl native_fn_021e5c10
    cmp r0, #0
    beq L_021e5e84
    cmp r7, #6
    addls pc, pc, r7, lsl #2
    b L_021e5e84
    dcd 0xea000005
    dcd 0xea000017
    dcd 0xea000024
    dcd 0xea000031
    dcd 0xea00003b
    dcd 0xea00004a
    dcd 0xea000057
    mov r4, #1
    strb r4, [r0]
    strb r8, [r0, #0x1]
    ldr r1, [r6]
    and r2, r7, #15
    str r1, [r0, #0x8]
    ldr r3, [r6, #0x4]
    mov r1, #4096
    str r3, [r0, #0xc]
    ldr r3, [r6, #0x8]
    str r3, [r0, #0x10]
    strb r5, [r0, #0x2]
    ldrb r3, [r0, #0x3]
    bic r3, r3, #15
    orr r2, r3, r2
    strb r2, [r0, #0x3]
    str r1, [r0, #0x14]
    str r4, [r0, #0x4]
    b L_021e5e84
    mov r4, #1
    strb r4, [r0]
    strb r8, [r0, #0x1]
    ldr r1, [r6]
    and r2, r7, #15
    str r1, [r0, #0x4]
    strb r5, [r0, #0x2]
    ldrb r3, [r0, #0x3]
    mov r1, #4096
    bic r3, r3, #15
    orr r2, r3, r2
    strb r2, [r0, #0x3]
    str r1, [r0, #0x14]
    b L_021e5e84
    mov r4, #1
    strb r4, [r0]
    strb r8, [r0, #0x1]
    ldr r1, [r6]
    and r2, r7, #15
    str r1, [r0, #0x4]
    strb r5, [r0, #0x2]
    ldrb r3, [r0, #0x3]
    mov r1, #4096
    bic r3, r3, #15
    orr r2, r3, r2
    strb r2, [r0, #0x3]
    str r1, [r0, #0x14]
    b L_021e5e84
    mov r4, #1
    strb r4, [r0]
    strb r8, [r0, #0x1]
    ldrb r3, [r0, #0x3]
    and r2, r7, #15
    mov r1, #4096
    bic r3, r3, #15
    orr r2, r3, r2
    strb r2, [r0, #0x3]
    str r1, [r0, #0x14]
    b L_021e5e84
    mov r1, #1
    strb r1, [r0]
    strb r8, [r0, #0x1]
    strb r5, [r0, #0x2]
    ldrb r3, [r0, #0x3]
    and r2, r7, #15
    mov r1, #4096
    bic r3, r3, #15
    orr r2, r3, r2
    strb r2, [r0, #0x3]
    str r1, [r0, #0x14]
    ldr r1, [r6]
    str r1, [r0, #0x18]
    ldr r1, [r6, #0x4]
    str r1, [r0, #0x1c]
    b L_021e5e84
    mov r1, #1
    strb r1, [r0]
    strb r8, [r0, #0x1]
    strb r5, [r0, #0x2]
    ldrb r3, [r0, #0x3]
    and r2, r7, #15
    mov r1, #4096
    bic r3, r3, #15
    orr r2, r3, r2
    strb r2, [r0, #0x3]
    str r1, [r0, #0x14]
    ldr r1, [r6]
    str r1, [r0, #0x18]
    b L_021e5e84
    mov r1, #1
    strb r1, [r0]
    strb r8, [r0, #0x1]
    strb r5, [r0, #0x2]
    ldrb r2, [r0, #0x3]
    and r1, r7, #15
    bic r2, r2, #15
    orr r1, r2, r1
    strb r1, [r0, #0x3]
    ldr r1, [r6]
    str r1, [r0, #0x4]
    ldrb r2, [r0, #0x3]
    ldrb r1, [r6, #0x1]
    bic r2, r2, #240
    mov r1, r1, lsl #28
    orr r1, r2, r1, lsr #24
    strb r1, [r0, #0x3]
L_021e5e84:
    mov r0, r4
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
