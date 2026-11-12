/* ov000 row 0x021f2b14: 92 bytes.
 *
 * What it does: 22 instructions; 2 call(s) to 0x0205f98c, 0x021f2b28; loops (back edge at +0x20); returns through pop {r3, r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x58 -> constant 0x02236da4 (image word 0x02236da4)
 *   back edge +0x50 -> +0x14
 *   test +0x24 cmp r4, #0
 *   test +0x30 cmp r1, #0
 *   test +0x4c cmp r4, #2
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f2b14; the literal pool and
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

extern void native_fn_0205f98c(void);


asm u32 native_ov000_021f2b14 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    ldr r7, =0x02236da4
    mov r6, r0
    mov r5, r1
    mov r4, #0
ov000_021f2b14_L14:
    ldr r0, [r7, #0x14]
    mov r1, r4
    ldr r0, [r0, #0x1c]
    bl native_fn_0205f98c
    cmp r4, #0
    moveq r1, r6
    movne r1, r5
    cmp r1, #0
    ldr r1, [r0, #0x7c]
    orrne r1, r1, #2
    biceq r1, r1, #2
    str r1, [r0, #0x7c]
    add r0, r4, #1
    and r4, r0, #255
    cmp r4, #2
    blo ov000_021f2b14_L14
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
