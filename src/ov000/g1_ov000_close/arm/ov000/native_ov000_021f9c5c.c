/* ov000 row 0x021f9c5c: 128 bytes.
 *
 * What it does: 31 instructions; 3 call(s) to 0x02215698, 0x022156c4, 0x021f9df0; no back edge; returns through pop {r3, r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x7c -> constant 0x02236f14 (image word 0x02236f14)
 *   branch +0x1c -> +0x2c
 *   branch +0x24 -> +0x50
 *   branch +0x28 -> +0x74
 *   branch +0x40 -> +0x74
 *   branch +0x4c -> +0x74
 *   branch +0x60 -> +0x74
 *   test +0x18 cmp r1, #0
 *   test +0x20 cmp r1, #1
 *   test +0x34 cmp r0, #0
 *   test +0x5c cmp r0, #0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f9c5c; the literal pool and
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

extern void ov000_display_context_02215698(void);
extern void native_fn_022156c4(void);
extern void native_fn_021f9df0(void);


asm u32 native_ov000_021f9c5c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    bl ov000_display_context_02215698
    mov r4, r0
    bl native_fn_022156c4
    ldrb r1, [r4, #0x49c]
    mov r5, r0
    cmp r1, #0
    beq ov000_021f9c5c_L2c
    cmp r1, #1
    beq ov000_021f9c5c_L50
    b ov000_021f9c5c_L74
ov000_021f9c5c_L2c:
    ldr r0, =0x02236f14
    ldr r0, [r0, #0x4]
    cmp r0, #0
    movne r0, #1
    strneb r0, [r4, #0x49c]
    bne ov000_021f9c5c_L74
    bl native_fn_021f9df0
    mov r5, r0
    b ov000_021f9c5c_L74
ov000_021f9c5c_L50:
    ldr r0, =0x02236f14
    ldr r0, [r0, #0x4]
    blx r0
    cmp r0, #0
    beq ov000_021f9c5c_L74
    ldr r0, =0x02236f14
    mov r1, #0
    str r1, [r0, #0x4]
    strb r1, [r4, #0x49c]
ov000_021f9c5c_L74:
    mov r0, r5
    ldmia sp!, {r3, r4, r5, pc}
}
