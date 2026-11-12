/* ov000 row 0x021dd170: 116 bytes.
 *
 * What it does: 29 instructions; 1 call(s) to 0x021dcf94; loops (back edge at +0x4c); returns through pop {r3, r4, r5, pc}
 *
 * Decoded shape: chunk loop.
 *
 *   branch +0x54 -> +0x68
 *   test +0x08 cmp r2, #0
 *   test +0x24 cmp r2, #0
 *   test +0x50 cmp r0, #0
 *   2 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021dd170; the literal pool and
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

extern void native_fn_021dcf94(void);


asm u32 native_ov000_021dd170 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    sub sp, sp, #16
    cmp r2, #0
    mov r4, #0
    mov r5, r3
    addeq sp, sp, #16
    moveq r0, r4
    ldmeqia sp!, {r3, r4, r5, pc}
    ldr r2, [r2, #0xc]
    cmp r2, #0
    addeq sp, sp, #16
    moveq r0, r4
    ldmeqia sp!, {r3, r4, r5, pc}
    adds r2, r2, #12
    addeq sp, sp, #16
    moveq r0, r4
    ldmeqia sp!, {r3, r4, r5, pc}
    add r3, sp, #4
    str r4, [sp]
    bl native_fn_021dcf94
    cmp r0, #0
    beq ov000_021dd170_L68
    add r0, sp, #4
    ldmia r0, {r0, r1, r2}
    stmia r5, {r0, r1, r2}
    mov r4, #1
ov000_021dd170_L68:
    mov r0, r4
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, pc}
}
