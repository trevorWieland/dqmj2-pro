/* main row 0x020d1cf8: 540 bytes.
 *
 * What it does: Moves 4-register chunks between two pointers with writeback block moves (3 loads, 3 stores).
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x214 -> native_data_020dc9dc (image word 0x020dc9dc)
 *   pool +0x218 -> constant 0x51eb851f (image word 0x51eb851f)
 *   branch +0x5c -> +0x7c
 *   branch +0x78 -> +0x98
 *   branch +0x94 -> +0xa0
 *   branch +0x9c -> +0xa4
 *   branch +0xb4 -> +0xd8
 *   back edge +0xd4 -> +0xbc
 *   branch +0xf0 -> +0x168
 *   branch +0x11c -> +0x134
 *   branch +0x130 -> +0x14c
 *   branch +0x148 -> +0x154
 *   branch +0x150 -> +0x158
 *   back edge +0x164 -> +0x108
 *   branch +0x178 -> +0x198
 *   branch +0x194 -> +0x1b8
 *   branch +0x1b4 -> +0x1c0
 *   branch +0x1bc -> +0x1c4
 *   branch +0x1d4 -> +0x1f8
 *   back edge +0x1f4 -> +0x1dc
 *   test +0x3c cmp r0, #2000
 *   test +0x58 tst r8, #3
 *   test +0xb0 cmp r2, #1
 *   test +0xc0 cmp r3, #2
 *   test +0xd0 cmp r3, r2
 *   test +0xe8 cmp r8, r7
 *   test +0x15c cmp r8, r7
 *   test +0x1d0 cmp r3, #1
 *   test +0x1e0 cmp r7, #2
 *   test +0x1f0 cmp r7, r3
 *   2 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020d1cf8; the literal pool and
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

extern u8 native_data_020dc9dc[];
extern void native_fn_0209b040(void);


asm u32 native_main_020d1cf8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #80
    ldr r6, =native_data_020dc9dc
    mov r4, r0
    ldmia r6!, {r0, r1, r2, r3}
    add r5, sp, #0
    stmia r5!, {r0, r1, r2, r3}
    ldmia r6!, {r0, r1, r2, r3}
    stmia r5!, {r0, r1, r2, r3}
    ldmia r6!, {r0, r1, r2, r3}
    stmia r5!, {r0, r1, r2, r3}
    ldr r0, [r6]
    add r1, sp, #52
    str r0, [r5]
    ldrh r0, [r4]
    cmp r0, #2000
    subhs r0, r0, #2000
    strhsh r0, [r4]
    add r0, sp, #64
    blx native_fn_0209b040
    ldr r8, [sp, #0x40]
    mov lr, #0
    tst r8, #3
    bne main_020d1cf8_L7c
    ldr r0, =0x51eb851f
    mov r2, #100
    umull r0, r1, r8, r0
    mov r1, r1, lsr #5
    umull r0, r1, r2, r1
    subs r1, r8, r0
    bne main_020d1cf8_L98
main_020d1cf8_L7c:
    ldr r0, =0x51eb851f
    mov r2, #400
    umull r0, r1, r8, r0
    mov r1, r1, lsr #7
    umull r0, r1, r2, r1
    subs r1, r8, r0
    bne main_020d1cf8_La0
main_020d1cf8_L98:
    mov r5, #1
    b main_020d1cf8_La4
main_020d1cf8_La0:
    mov r5, #0
main_020d1cf8_La4:
    ldr r0, [sp, #0x44]
    mov r3, #1
    sub r2, r0, #1
    cmp r2, #1
    blo main_020d1cf8_Ld8
    add r1, sp, #0
main_020d1cf8_Lbc:
    ldr r0, [r1, r3, lsl #2]
    cmp r3, #2
    add lr, lr, r0
    add r3, r3, #1
    addeq lr, lr, r5
    cmp r3, r2
    bls main_020d1cf8_Lbc
main_020d1cf8_Ld8:
    ldrh r6, [r4]
    ldr r0, [sp, #0x48]
    mov r5, #0
    sub r7, r6, #1
    cmp r8, r7
    add lr, lr, r0
    bgt main_020d1cf8_L168
    ldr r1, =0x51eb851f
    mov r3, r5
    mov r12, #1
    mov r0, #100
    mov r10, #400
main_020d1cf8_L108:
    mov r2, r8, lsr #31
    add r5, r5, #109
    rsb r9, r2, r8, lsl #30
    adds r9, r2, r9, ror #30
    add r5, r5, #256
    bne main_020d1cf8_L134
    smull r9, r11, r1, r8
    add r11, r2, r11, asr #5
    smull r2, r9, r0, r11
    subs r11, r8, r2
    bne main_020d1cf8_L14c
main_020d1cf8_L134:
    mov r2, r8, lsr #31
    smull r9, r11, r1, r8
    add r11, r2, r11, asr #7
    smull r2, r9, r10, r11
    subs r11, r8, r2
    bne main_020d1cf8_L154
main_020d1cf8_L14c:
    mov r2, r12
    b main_020d1cf8_L158
main_020d1cf8_L154:
    mov r2, r3
main_020d1cf8_L158:
    add r8, r8, #1
    cmp r8, r7
    add r5, r5, r2
    ble main_020d1cf8_L108
main_020d1cf8_L168:
    mov r7, r6, lsr #31
    rsb r0, r7, r6, lsl #30
    adds r0, r7, r0, ror #30
    mov r0, #0
    bne main_020d1cf8_L198
    ldr r2, =0x51eb851f
    mov r3, #100
    smull r1, r8, r2, r6
    add r8, r7, r8, asr #5
    smull r1, r2, r3, r8
    subs r8, r6, r1
    bne main_020d1cf8_L1b8
main_020d1cf8_L198:
    ldr r3, =0x51eb851f
    mov r1, r6, lsr #31
    smull r2, r7, r3, r6
    add r7, r1, r7, asr #7
    mov r3, #400
    smull r1, r2, r3, r7
    subs r7, r6, r1
    bne main_020d1cf8_L1c0
main_020d1cf8_L1b8:
    mov r6, #1
    b main_020d1cf8_L1c4
main_020d1cf8_L1c0:
    mov r6, #0
main_020d1cf8_L1c4:
    ldrb r1, [r4, #0x2]
    mov r7, #1
    sub r3, r1, #1
    cmp r3, #1
    blt main_020d1cf8_L1f8
    add r2, sp, #0
main_020d1cf8_L1dc:
    ldr r1, [r2, r7, lsl #2]
    cmp r7, #2
    add r0, r0, r1
    add r7, r7, #1
    addeq r0, r0, r6
    cmp r7, r3
    ble main_020d1cf8_L1dc
main_020d1cf8_L1f8:
    ldrb r1, [r4, #0x3]
    add r0, r0, r1
    add r0, r5, r0
    sub r0, r0, lr
    rsb r0, r0, #0
    add sp, sp, #80
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
