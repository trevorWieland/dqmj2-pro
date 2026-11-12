/* ov000 row 0x02217814: 116 bytes.
 *
 * What it does: 28 instructions; 2 call(s) to 0x0221783c, 0x02062aa0; loops (back edge at +0x44); returns through pop {r4, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x70 -> constant 0x0224532c (image word 0x0224532c)
 *   branch +0x0c -> +0x34
 *   branch +0x14 -> +0x28
 *   branch +0x20 -> +0x54
 *   branch +0x24 -> +0x44
 *   branch +0x2c -> +0x54
 *   branch +0x30 -> +0x44
 *   branch +0x38 -> +0x44
 *   test +0x08 cmp r4, #12
 *   test +0x10 cmp r4, #8
 *   test +0x18 cmpne r4, #9
 *   test +0x1c cmpne r4, #12
 *   test +0x28 cmp r4, #1
 *   test +0x34 cmp r4, #127
 *   test +0x48 cmp r0, #0
 *   test +0x60 tst r0, #1
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02217814; the literal pool and
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

extern void native_fn_02062aa0(void);


asm u32 native_ov000_02217814 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r4, r0
    cmp r4, #12
    bgt ov000_02217814_L34
    cmp r4, #8
    blt ov000_02217814_L28
    cmpne r4, #9
    cmpne r4, #12
    beq ov000_02217814_L54
    b ov000_02217814_L44
ov000_02217814_L28:
    cmp r4, #1
    beq ov000_02217814_L54
    b ov000_02217814_L44
ov000_02217814_L34:
    cmp r4, #127
    bne ov000_02217814_L44
    mov r0, #0
    ldmia sp!, {r4, pc}
ov000_02217814_L44:
    bl native_fn_02062aa0
    cmp r0, #0
    moveq r0, #0
    ldmeqia sp!, {r4, pc}
ov000_02217814_L54:
    ldr r0, =0x0224532c
    ldr r0, [r0, #0x28]
    mov r0, r0, lsr r4
    tst r0, #1
    movne r0, #1
    moveq r0, #0
    ldmia sp!, {r4, pc}
}
