/* ov000 row 0x021ee0a4: 196 bytes.
 *
 * What it does: Writes 2 blocks of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   back edge +0x38 -> +0x2c
 *   branch +0x5c -> +0x88
 *   branch +0x6c -> +0x88
 *   back edge +0x84 -> +0x64
 *   back edge +0xb8 -> +0xa0
 *   test +0x40 cmp r5, #0
 *   test +0x54 cmp r6, #0
 *   test +0x68 cmp r10, #0
 *   test +0x80 cmp r9, r6
 *   test +0x8c cmp r4, #0
 *   test +0xa8 cmp r1, #0
 *   test +0xb4 cmp r3, r4
 *   2 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021ee0a4; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02084808(void);


asm u32 native_ov000_021ee0a4 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, lr}
    sub sp, sp, #1024
    mov r7, r0
    mov r0, #0
    mov r6, r1
    mov r5, r2
    add r8, sp, #0
    mov r1, r0
    mov r2, r0
    mov r3, r0
    mov r4, #32
ov000_021ee0a4_L2c:
    stmia r8!, {r0, r1, r2, r3}
    stmia r8!, {r0, r1, r2, r3}
    subs r4, r4, #1
    bne ov000_021ee0a4_L2c
    bl native_fn_02084808
    cmp r5, #0
    mov r4, r0
    addeq sp, sp, #1024
    moveq r0, #0
    ldmeqia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
    cmp r6, #0
    mov r9, #0
    ble ov000_021ee0a4_L88
    add r8, sp, #0
ov000_021ee0a4_L64:
    ldr r10, [r7, r9, lsl #2]
    cmp r10, #0
    beq ov000_021ee0a4_L88
    mov r0, r10
    blx r5
    add r9, r9, #1
    str r10, [r8, r0, lsl #2]
    cmp r9, r6
    blt ov000_021ee0a4_L64
ov000_021ee0a4_L88:
    mov r0, #0
    cmp r4, #0
    addls sp, sp, #1024
    mov r3, r0
    ldmlsia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
    add r2, sp, #0
ov000_021ee0a4_La0:
    ldr r1, [r2, r3, lsl #2]
    add r3, r3, #1
    cmp r1, #0
    strne r1, [r7, r0, lsl #2]
    addne r0, r0, #1
    cmp r3, r4
    blo ov000_021ee0a4_La0
    add sp, sp, #1024
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
}
