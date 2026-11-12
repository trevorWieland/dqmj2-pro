/* main row 0x020a51e4: 284 bytes.
 *
 * What it does: Writes 2 blocks of 2 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x10c -> constant 0x0000ffff (image word 0x0000ffff)
 *   pool +0x110 -> constant 0x00ffffff (image word 0x00ffffff)
 *   pool +0x114 -> native_data_020dc524 (image word 0x020dc524)
 *   pool +0x118 -> native_data_020dc51c (image word 0x020dc51c)
 *   back edge +0x6c -> +0x60
 *   back edge +0x90 -> +0x78
 *   back edge +0xb2 -> +0xa4
 *   back edge +0xf0 -> +0xe4
 *   test +0x6a cmp r5, #0x6
 *   test +0x8e cmp r4, #0x5
 *   test +0xb0 cmp r5, #0x5
 *   test +0xee cmp r2, #0x6
 *   0 block transfer(s), 17 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020a51e4; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 14 of 284 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_020dc524[];
extern void native_fn_02008e0c(void);
extern u8 native_data_020dc51c[];


asm u32 native_main_020a51e4 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x18
    add r4, r0, #0x0
    str r2, [sp, #0x4]
    add r0, r1, #0x0
    mov r5, #0x0
    add r1, r3, #0x0
    add r3, r5, #0x0
    ldr r2, =0x0000ffff
    add r6, r4, #0x0
    and r3, r5
    and r6, r2
    lsr r2, r6, #0x5
    lsl r4, r3, #0x1b
    orr r4, r2
    lsl r2, r6, #0x1b
    str r2, [sp]
    ldr r2, =0x00ffffff
    add r6, r0, #0x0
    and r6, r2
    lsr r0, r6, #0x1d
    lsl r2, r3, #0x3
    orr r2, r0
    mov r0, #0x3
    and r0, r1
    mov r12, r0
    ldr r0, [sp, #0x4]
    lsl r7, r6, #0x3
    mov r1, #0x1
    add r6, r0, #0x0
    and r6, r1
    lsr r0, r6, #0x1e
    lsl r1, r3, #0x2
    orr r1, r0
    orr r1, r3
    orr r1, r2
    orr r1, r4
    lsl r0, r6, #0x2
    mov r3, r12
    orr r0, r3
    add r2, r7, #0x0
    orr r2, r0
    ldr r0, [sp]
    str r1, [sp, #0x14]
    orr r0, r2
    str r0, [sp, #0x10]
    add r2, sp, #0x10
    mov r0, #0xd6
main_020a51e4_L60:
    ldrb r1, [r2, #0]
    add r5, r5, #0x1
    eor r1, r0
    strb r1, [r2, #0]
    add r2, r2, #0x1
    cmp r5, #0x6
    blt main_020a51e4_L60
    mov r5, #0xf
    ldr r0, =native_data_020dc524
    mov r4, #0x0
    add r3, sp, #0x10
    add r6, r5, #0x0
main_020a51e4_L78:
    ldrb r2, [r3, #0]
    add r4, r4, #0x1
    asr r1, r2, #0x4
    and r1, r5
    ldrb r1, [r0, r1]
    and r2, r6
    ldrb r2, [r0, r2]
    lsl r1, r1, #0x4
    orr r1, r2
    strb r1, [r3, #0]
    add r3, r3, #0x1
    cmp r4, #0x5
    blt main_020a51e4_L78
    add r0, sp, #0x10
    add r1, sp, #0x8
    mov r2, #0x8
    blx native_fn_02008e0c
    ldr r4, =native_data_020dc51c
    mov r5, #0x0
    add r3, sp, #0x8
    add r1, sp, #0x10
main_020a51e4_La4:
    ldrb r2, [r3, #0]
    ldrb r0, [r4, #0]
    add r5, r5, #0x1
    add r3, r3, #0x1
    add r4, r4, #0x1
    strb r2, [r1, r0]
    cmp r5, #0x5
    blt main_020a51e4_La4
    mov r2, #0x0
    add r4, sp, #0x8
    strb r2, [r4, #0xf]
    strb r2, [r4, #0xe]
    ldrb r3, [r4, #0xd]
    mov r0, #0x7
    and r0, r3
    strb r0, [r4, #0xd]
    ldr r5, [sp, #0x10]
    ldr r3, [sp, #0x14]
    lsr r0, r5, #0x1f
    lsl r3, r3, #0x1
    orr r3, r0
    lsl r0, r5, #0x1
    str r0, [sp, #0x10]
    str r3, [sp, #0x14]
    ldrb r3, [r4, #0xd]
    ldrb r0, [r4, #0x8]
    asr r5, r3, #0x3
    mov r3, #0x1
    and r3, r5
    orr r0, r3
    strb r0, [r4, #0x8]
    mov r0, #0x67
main_020a51e4_Le4:
    ldrb r3, [r1, #0]
    add r2, r2, #0x1
    eor r3, r0
    strb r3, [r1, #0]
    add r1, r1, #0x1
    cmp r2, #0x6
    blt main_020a51e4_Le4
    mov r0, #0x0
    add r1, sp, #0x8
    strb r0, [r1, #0xf]
    strb r0, [r1, #0xe]
    ldrb r2, [r1, #0xd]
    mov r0, #0x7
    and r0, r2
    strb r0, [r1, #0xd]
    ldr r0, [sp, #0x10]
    ldr r1, [sp, #0x14]
    add sp, #0x18
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
