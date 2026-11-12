/* ov000 row 0x021d95a0: 196 bytes.
 *
 * What it does: 44 instructions; 10 call(s) to 0x021d95e8, 0x020297e0, 0x02029950, +7 more; loops (back edge at +0x20); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 5 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xb0 -> constant 0x0223042c (image word 0x0223042c)
 *   pool +0xb4 -> constant 0x022304ec (image word 0x022304ec)
 *   pool +0xb8 -> constant 0x02230488 (image word 0x02230488)
 *   pool +0xbc -> constant 0x022304e4 (image word 0x022304e4)
 *   pool +0xc0 -> constant 0x022304e8 (image word 0x022304e8)
 *   branch +0x14 -> +0x48
 *   back edge +0x44 -> +0x1c
 *   branch +0x54 -> +0xa8
 *   branch +0x74 -> +0x8c
 *   back edge +0xa4 -> +0x68
 *   test +0x10 cmp r0, #0
 *   test +0x3c cmp r5, r0
 *   test +0x50 cmp r0, #0
 *   test +0x70 cmp r0, #0
 *   test +0x94 cmp r4, r0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021d95a0; the literal pool and
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

extern void native_fn_020297e0(void);
extern void native_fn_02029950(void);
extern void native_fn_02028dac(void);
extern void native_fn_02041128(void);
extern void native_fn_0204122c(void);


asm u32 native_ov000_021d95a0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    ldr r4, =0x0223042c
    mov r5, #0
    ldr r0, [r4, #0x58]
    cmp r0, #0
    ble ov000_021d95a0_L48
    ldr r6, =0x022304ec
ov000_021d95a0_L1c:
    mov r0, r6
    bl native_fn_020297e0
    mov r0, r6
    bl native_fn_02029950
    mov r0, r6
    bl native_fn_02028dac
    ldr r0, [r4, #0x58]
    add r5, r5, #1
    cmp r5, r0
    add r6, r6, #372
    blt ov000_021d95a0_L1c
ov000_021d95a0_L48:
    mov r4, #0
    mov r6, r4
    cmp r0, #0
    ble ov000_021d95a0_La8
    ldr r7, =0x02230488
    ldr r8, =0x022304e4
    ldr r9, =0x022304e8
    ldr r5, =0x0223042c
ov000_021d95a0_L68:
    mov r0, r7
    bl native_fn_02041128
    cmp r0, #0
    beq ov000_021d95a0_L8c
    mov r0, r8
    bl native_fn_0204122c
    mov r0, r9
    bl native_fn_0204122c
    add r6, r6, #1
ov000_021d95a0_L8c:
    ldr r0, [r5, #0x58]
    add r4, r4, #1
    cmp r4, r0
    add r7, r7, #372
    add r8, r8, #372
    add r9, r9, #372
    blt ov000_021d95a0_L68
ov000_021d95a0_La8:
    mov r0, r6
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
