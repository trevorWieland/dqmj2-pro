/* ov006 row 0x021dc08c: 124 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x58 -> +0x68
 *   back edge +0x64 -> +0x40
 *   test +0x4c cmp r0, #12288
 *   test +0x60 cmp r3, #32
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021dc08c; the literal pool and
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

extern void native_fn_02008be0(void);
extern void native_fn_021d8414(void);
extern void native_fn_021d7ad0(void);


asm u32 native_ov006_021dc08c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    sub sp, sp, #32
    mov r6, r1
    mov r4, r0
    mov r5, r2
    add r1, sp, #0
    mov r0, #0
    mov r2, #32
    bl native_fn_02008be0
    add r1, sp, #0
    mov r0, r6
    add r3, r5, #1
    mov r2, #16
    bl native_fn_021d8414
    mov r3, #0
    add r1, sp, #0
ov006_021dc08c_L40:
    add r0, r1, r3, lsl #1
    ldrh r0, [r0, #2]
    mov r2, r3, lsl #1
    cmp r0, #12288
    movne r0, #43
    strneh r0, [r1, r2]
    bne ov006_021dc08c_L68
    add r3, r3, #1
    cmp r3, #32
    blo ov006_021dc08c_L40
ov006_021dc08c_L68:
    add r1, sp, #0
    mov r0, r4
    bl native_fn_021d7ad0
    add sp, sp, #32
    ldmia sp!, {r4, r5, r6, pc}
}
