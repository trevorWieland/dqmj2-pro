/* ov000 row 0x02218800: 172 bytes.
 *
 * What it does: 41 instructions; 4 call(s) to 0x02066c3c, 0x0205f98c, 0x0221889c, +1 more; loops (back edge at +0x0c); returns through pop {r3, r4, r5, r6, r7, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xa4 -> constant 0x02245f2c (image word 0x02245f2c)
 *   pool +0xa8 -> constant 0x02245e54 (image word 0x02245e54)
 *   branch +0x5c -> +0x9c
 *   branch +0x7c -> +0x9c
 *   branch +0x84 -> +0x9c
 *   branch +0x90 -> +0x9c
 *   test +0x1c cmp r1, #127
 *   test +0x2c cmp r0, #0
 *   test +0x40 cmp r1, #0
 *   test +0x58 cmp r0, r6
 *   test +0x78 cmp r1, r4
 *   test +0x80 cmp r1, r3
 *   test +0x8c cmp r0, r6
 *   test +0x94 cmp r0, r2
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02218800; the literal pool and
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

extern void native_fn_02066c3c(void);
extern void native_fn_0205f98c(void);


asm u32 native_ov000_02218800 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    ldr r4, =0x02245f2c
    mov r6, r0
    bl native_fn_02066c3c
    ldr r1, [r4]
    mov r7, r0
    mov r5, #0
    cmp r1, #127
    moveq r0, r5
    ldmeqia sp!, {r3, r4, r5, r6, r7, pc}
    ldr r0, [r4, #0x1c]
    cmp r0, #0
    moveq r0, r5
    ldmeqia sp!, {r3, r4, r5, r6, r7, pc}
    ldr r1, =0x02245e54
    ldr r1, [r1, #0x20]
    cmp r1, #0
    movne r0, r5
    ldmneia sp!, {r3, r4, r5, r6, r7, pc}
    mov r1, r5
    bl native_fn_0205f98c
    ldrb r0, [r7]
    cmp r0, r6
    bne ov000_02218800_L9c
    ldr r0, =0x02245e54
    ldrsh r6, [r4, #22]
    ldrsh r4, [r4, #20]
    ldrsh r1, [r0, #56]
    add r2, r6, #16
    add r3, r4, #44
    cmp r1, r4
    blt ov000_02218800_L9c
    cmp r1, r3
    bgt ov000_02218800_L9c
    ldrsh r0, [r0, #58]
    cmp r0, r6
    blt ov000_02218800_L9c
    cmp r0, r2
    movle r5, #1
ov000_02218800_L9c:
    mov r0, r5
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
