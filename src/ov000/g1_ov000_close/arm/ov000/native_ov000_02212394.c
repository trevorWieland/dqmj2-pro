/* ov000 row 0x02212394: 236 bytes.
 *
 * What it does: 58 instructions; 5 call(s) to 0x02212460, 0x021dfc08, 0x02212460, +2 more; loops (back edge at +0x44); returns through pop {r4, r5, r6, r7, r8, r9, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0xe8 -> constant 0x0224157c (image word 0x0224157c)
 *   branch +0x28 -> +0xcc
 *   branch +0x34 -> +0xcc
 *   branch +0x40 -> +0xcc
 *   branch +0x4c -> +0xcc
 *   branch +0x94 -> +0xcc
 *   branch +0xa0 -> +0xdc
 *   branch +0xc8 -> +0xdc
 *   back edge +0xd8 -> +0x20
 *   test +0x24 cmp r0, #0
 *   test +0x30 cmp r1, #0
 *   test +0x3c cmp r1, #0
 *   test +0x48 cmp r0, #0
 *   test +0x98 cmp r8, #0
 *   test +0xd0 cmp r4, #24
 *   2 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02212394; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity fixes the instruction stream, not the field, block and callee semantics behind the addresses and strides it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_021dfc08(void);
extern void native_fn_021dd2a4(void);


asm u32 native_ov000_02212394 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, lr}
    sub sp, sp, #12
    mov r5, #0
    ldr r6, =0x0224157c
    mov r9, r0
    mov r8, r1
    mov r7, r2
    mov r4, r5
ov000_02212394_L20:
    ldrsh r0, [r6]
    cmp r0, #0
    ble ov000_02212394_Lcc
    ldrb r1, [r6, #0x9]
    cmp r1, #0
    beq ov000_02212394_Lcc
    ldr r1, [r6, #0x164]
    cmp r1, #0
    bne ov000_02212394_Lcc
    bl native_fn_021dfc08
    cmp r0, #0
    ble ov000_02212394_Lcc
    ldr r2, [r9, #0x4]
    ldr r1, [r6, #0x118]
    ldr lr, [r9]
    sub r3, r2, r1
    smull r1, r2, r3, r3
    ldr r3, [r6, #0x114]
    ldr r12, [r9, #0x8]
    sub lr, lr, r3
    ldr r3, [r6, #0x11c]
    smlal r1, r2, lr, lr
    sub r3, r12, r3
    smlal r1, r2, r3, r3
    mov r3, r1, lsr #12
    orr r3, r3, r2, lsl #20
    mov r1, r0, asr #31
    subs r0, r3, r0
    rscs r0, r1, r2, asr #12
    bge ov000_02212394_Lcc
    cmp r8, #0
    moveq r5, #2
    beq ov000_02212394_Ldc
    add r3, sp, #0
    mov r0, r9
    mov r2, r8
    add r1, r6, #276
    bl native_fn_021dd2a4
    add r0, sp, #0
    ldmia r0, {r0, r1, r2}
    mov r5, #1
    stmia r7, {r0, r1, r2}
    b ov000_02212394_Ldc
ov000_02212394_Lcc:
    add r4, r4, #1
    cmp r4, #24
    add r6, r6, #360
    blt ov000_02212394_L20
ov000_02212394_Ldc:
    mov r0, r5
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, r8, r9, pc}
}
