/* ov000 row 0x021e7764: 100 bytes.
 *
 * What it does: 24 instructions; 3 call(s) to 0x021e77bc, 0x0201d800, 0x021e7794; loops (back edge at +0x38); returns through pop {r4, r5, r6, r7, r8, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x60 -> constant 0x022351e8 (image word 0x022351e8)
 *   branch +0x18 -> +0x58
 *   branch +0x2c -> +0x58
 *   branch +0x44 -> +0x58
 *   back edge +0x54 -> +0x30
 *   test +0x14 cmp r0, #0
 *   test +0x24 cmp r5, #0
 *   test +0x3c cmp r0, #0
 *   test +0x4c cmp r4, r5
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e7764; the literal pool and
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

extern void native_fn_0201d800(void);


asm u32 native_ov000_021e7764 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    ldr r1, =0x022351e8
    mov r8, r0
    ldr r0, [r1]
    mov r7, #0
    cmp r0, #0
    beq ov000_021e7764_L58
    ldr r5, [r0, #0x4]
    mov r4, r7
    cmp r5, #0
    add r6, r0, #8
    ble ov000_021e7764_L58
ov000_021e7764_L30:
    mov r0, r8
    mov r1, r6
    bl native_fn_0201d800
    cmp r0, #0
    moveq r7, r6
    beq ov000_021e7764_L58
    add r4, r4, #1
    cmp r4, r5
    add r6, r6, #72
    blt ov000_021e7764_L30
ov000_021e7764_L58:
    mov r0, r7
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
