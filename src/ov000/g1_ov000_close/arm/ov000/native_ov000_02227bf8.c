/* ov000 row 0x02227bf8: 104 bytes.
 *
 * What it does: 24 instructions; 2 call(s) to 0x02088a64, 0x02227c10; loops (back edge at +0x34); returns through pop {r4, r5, r6, r7, r8, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x60 -> constant 0x02246c84 (image word 0x02246c84)
 *   pool +0x64 -> constant 0x02246aa8 (image word 0x02246aa8)
 *   branch +0x30 -> +0x44
 *   branch +0x40 -> +0x58
 *   back edge +0x54 -> +0x18
 *   test +0x18 cmp r8, #0
 *   test +0x24 cmp r0, #0
 *   test +0x2c cmpne r1, #0
 *   test +0x38 cmp r0, #0
 *   test +0x48 cmp r4, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02227bf8; the literal pool and
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

extern void native_fn_02088a64(void);


asm u32 native_ov000_02227bf8 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    mov r5, #0
    ldr r6, =0x02246c84
    ldr r7, =0x02246aa8
    mov r8, r0
    mov r4, r5
ov000_02227bf8_L18:
    cmp r8, #0
    moveq r0, r6
    movne r0, r7
    cmp r0, #0
    ldrnesh r1, [r0, #24]
    cmpne r1, #0
    beq ov000_02227bf8_L44
    bl native_fn_02088a64
    cmp r0, #0
    movne r5, #1
    bne ov000_02227bf8_L58
ov000_02227bf8_L44:
    add r4, r4, #1
    cmp r4, #3
    add r6, r6, #132
    add r7, r7, #132
    blt ov000_02227bf8_L18
ov000_02227bf8_L58:
    mov r0, r5
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
