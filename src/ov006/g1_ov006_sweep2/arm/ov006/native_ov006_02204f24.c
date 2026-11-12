/* ov006 row 0x02204f24: 52 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x30 -> constant 0x0221c1f0 (image word 0x0221c1f0)
 *   branch +0x10 -> +0x1c
 *   test +0x0c cmp r1, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02204f24; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity proves the instruction stream, not the meaning of the fields, blocks and callee contracts it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_0202a498(void);


asm u32 native_ov006_02204f24 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r0, =0x0221c1f0
    ldr r1, [r0, #0x8]
    cmp r1, #0
    beq ov006_02204f24_L1c
    mov r0, #1
    bl native_fn_0202a498
ov006_02204f24_L1c:
    ldr r0, =0x0221c1f0
    mov r1, #0
    str r1, [r0]
    str r1, [r0, #0x8]
    ldmia sp!, {r3, pc}
}
