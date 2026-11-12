/* main row 0x020a9fc0: 168 bytes.
 *
 * What it does: Writes 4 blocks of 2 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0xa0 -> native_data_020e042c (image word 0x020e042c)
 *   pool +0xa4 -> native_data_020e043c (image word 0x020e043c)
 *   branch +0x0c -> +0x14
 *   branch +0x12 -> +0x1a
 *   branch +0x1c -> +0x26
 *   branch +0x24 -> +0x2c
 *   branch +0x2e -> +0x38
 *   branch +0x36 -> +0x3e
 *   branch +0x42 -> +0x50
 *   branch +0x58 -> +0x78
 *   test +0x0a cmp r5, #0x0
 *   test +0x10 cmp r6, #0x0
 *   test +0x1a cmp r4, #0x0
 *   test +0x22 cmp r1, #0x0
 *   test +0x2c cmp r2, #0x0
 *   test +0x34 cmp r1, #0x0
 *   test +0x40 cmp r3, #0x0
 *   test +0x56 cmp r1, #0x0
 *   4 block transfer(s), 9 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020a9fc0; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 10 of 168 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_020e042c[];
extern void native_fn_020b2c88(void);
extern u8 native_data_020e043c[];
extern void native_fn_020ad144(void);


asm u32 native_main_020a9fc0 (register u32 a0)
{
    push {r4, r5, r6, r7, lr}
    sub sp, #0x44
    add r5, r0, #0x0
    add r4, r1, #0x0
    add r7, r3, #0x0
    cmp r5, #0x0
    beq main_020a9fc0_L14
    ldr r6, [r5, #0]
    cmp r6, #0x0
    bne main_020a9fc0_L1a
main_020a9fc0_L14:
    add sp, #0x44
    mov r0, #0x2
    pop {r4, r5, r6, r7, pc}
main_020a9fc0_L1a:
    cmp r4, #0x0
    beq main_020a9fc0_L26
    mov r1, #0x0
    ldrsb r1, [r4, r1]
    cmp r1, #0x0
    bne main_020a9fc0_L2c
main_020a9fc0_L26:
    add sp, #0x44
    mov r0, #0x2
    pop {r4, r5, r6, r7, pc}
main_020a9fc0_L2c:
    cmp r2, #0x0
    beq main_020a9fc0_L38
    mov r1, #0x0
    ldrsb r1, [r2, r1]
    cmp r1, #0x0
    bne main_020a9fc0_L3e
main_020a9fc0_L38:
    add sp, #0x44
    mov r0, #0x2
    pop {r4, r5, r6, r7, pc}
main_020a9fc0_L3e:
    ldr r3, [sp, #0x5c]
    cmp r3, #0x0
    bne main_020a9fc0_L50
    ldr r1, =native_data_020e042c
    bl native_fn_020b2c88
    add sp, #0x44
    mov r0, #0x2
    pop {r4, r5, r6, r7, pc}
main_020a9fc0_L50:
    mov r1, #0x42
    lsl r1, r1, #0x2
    ldr r1, [r6, r1]
    cmp r1, #0x0
    beq main_020a9fc0_L78
    add r4, sp, #0x24
    mov r0, #0x0
    add r2, r4, #0x0
    add r1, r0, #0x0
    stmia r2!, {r0, r1}
    stmia r2!, {r0, r1}
    stmia r2!, {r0, r1}
    stmia r2!, {r0, r1}
    ldr r2, [sp, #0x60]
    add r0, r5, #0x0
    add r1, r4, #0x0
    blx r3
    add sp, #0x44
    mov r0, #0x0
    pop {r4, r5, r6, r7, pc}
main_020a9fc0_L78:
    ldr r1, =native_data_020e043c
    str r1, [sp]
    str r4, [sp, #0x4]
    str r2, [sp, #0x8]
    mov r2, #0x0
    str r2, [sp, #0xc]
    str r7, [sp, #0x10]
    str r2, [sp, #0x14]
    ldr r2, [sp, #0x58]
    str r2, [sp, #0x18]
    str r3, [sp, #0x1c]
    ldr r2, [sp, #0x60]
    add r3, r1, #0x0
    str r2, [sp, #0x20]
    add r2, r1, #0x0
    bl native_fn_020ad144
    add sp, #0x44
    pop {r4, r5, r6, r7, pc}
    mov r8, r8
}
