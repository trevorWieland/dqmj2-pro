/* ov000 row 0x021e0498: 444 bytes.
 *
 * What it does: Moves 4-register chunks between two pointers with writeback block moves (10 loads, 9 stores).
 *
 * Decoded shape: chunk loop.
 *
 *   branch +0x18 -> +0x114
 *   branch +0x28 -> +0x104
 *   branch +0x40 -> +0x90
 *   branch +0x8c -> +0xf4
 *   branch +0xa8 -> +0xf4
 *   back edge +0x100 -> +0x34
 *   back edge +0x110 -> +0x20
 *   branch +0x11c -> +0x1b0
 *   branch +0x12c -> +0x1a0
 *   branch +0x144 -> +0x190
 *   back edge +0x19c -> +0x138
 *   back edge +0x1ac -> +0x124
 *   test +0x10 cmp r8, #0
 *   test +0x24 cmp r5, r8
 *   test +0x3c cmp r0, #0
 *   test +0xf8 cmp r5, r8
 *   test +0x108 cmp r4, r8
 *   test +0x114 cmp r8, #0
 *   test +0x128 cmp r10, r8
 *   test +0x140 cmp r1, r0
 *   test +0x194 cmp r10, r8
 *   test +0x1a4 cmp r7, r8
 *   9 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e0498; the literal pool and
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

extern void native_fn_021e0478(void);


asm u32 native_ov000_021e0498 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #60
    mov r8, r1
    mov r9, r0
    cmp r8, #0
    mov r4, #0
    ble ov000_021e0498_L114
    mov r6, r9
ov000_021e0498_L20:
    add r5, r4, #1
    cmp r5, r8
    bge ov000_021e0498_L104
    mov r0, #20
    mla r7, r5, r0, r9
ov000_021e0498_L34:
    ldmia r7, {r0, r1}
    bl native_fn_021e0478
    cmp r0, #0
    beq ov000_021e0498_L90
    mov r10, r6
    ldmia r10!, {r0, r1, r2, r3}
    add lr, sp, #40
    mov r12, lr
    stmia lr!, {r0, r1, r2, r3}
    ldr r0, [r10]
    mov r10, r7
    str r0, [lr]
    ldmia r10!, {r0, r1, r2, r3}
    mov lr, r6
    stmia lr!, {r0, r1, r2, r3}
    ldr r0, [r10]
    mov r10, r7
    str r0, [lr]
    ldmia r12!, {r0, r1, r2, r3}
    stmia r10!, {r0, r1, r2, r3}
    ldr r0, [r12]
    str r0, [r10]
    b ov000_021e0498_Lf4
ov000_021e0498_L90:
    ldr r3, [r6, #0x8]
    ldr r0, [r7, #0x8]
    ldr r2, [r6, #0xc]
    ldr r1, [r7, #0xc]
    subs r0, r0, r3
    sbcs r0, r1, r2
    bge ov000_021e0498_Lf4
    mov r11, r6
    ldmia r11!, {r0, r1, r2, r3}
    add r10, sp, #0
    mov r12, r10
    stmia r10!, {r0, r1, r2, r3}
    ldr r0, [r11]
    mov lr, r7
    str r0, [r10]
    ldmia lr!, {r0, r1, r2, r3}
    mov r10, r6
    stmia r10!, {r0, r1, r2, r3}
    ldr r0, [lr]
    mov lr, r7
    str r0, [r10]
    ldmia r12!, {r0, r1, r2, r3}
    stmia lr!, {r0, r1, r2, r3}
    ldr r0, [r12]
    str r0, [lr]
ov000_021e0498_Lf4:
    add r5, r5, #1
    cmp r5, r8
    add r7, r7, #20
    blt ov000_021e0498_L34
ov000_021e0498_L104:
    add r4, r4, #1
    cmp r4, r8
    add r6, r6, #20
    blt ov000_021e0498_L20
ov000_021e0498_L114:
    cmp r8, #0
    mov r7, #0
    ble ov000_021e0498_L1b0
    mov r5, r9
ov000_021e0498_L124:
    add r10, r7, #1
    cmp r10, r8
    bge ov000_021e0498_L1a0
    mov r0, #20
    mla r6, r10, r0, r9
ov000_021e0498_L138:
    ldr r1, [r5, #0x10]
    ldr r0, [r6, #0x10]
    cmp r1, r0
    bge ov000_021e0498_L190
    mov r11, r5
    ldmia r11!, {r0, r1, r2, r3}
    add r12, sp, #20
    mov r4, r12
    stmia r12!, {r0, r1, r2, r3}
    ldr r0, [r11]
    mov r11, r6
    str r0, [r12]
    ldmia r11!, {r0, r1, r2, r3}
    mov lr, r5
    stmia lr!, {r0, r1, r2, r3}
    ldr r0, [r11]
    mov r12, r6
    str r0, [lr]
    ldmia r4!, {r0, r1, r2, r3}
    stmia r12!, {r0, r1, r2, r3}
    ldr r0, [r4]
    str r0, [r12]
ov000_021e0498_L190:
    add r10, r10, #1
    cmp r10, r8
    add r6, r6, #20
    blt ov000_021e0498_L138
ov000_021e0498_L1a0:
    add r7, r7, #1
    cmp r7, r8
    add r5, r5, #20
    blt ov000_021e0498_L124
ov000_021e0498_L1b0:
    mov r0, r8
    add sp, sp, #60
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
