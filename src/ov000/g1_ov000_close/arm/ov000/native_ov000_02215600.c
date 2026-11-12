/* ov000 row 0x02215600: 148 bytes.
 *
 * What it does: 36 instructions; 4 call(s) to 0x02215dac, 0x02215ee4, 0x02215f78, +1 more; loops (back edge at +0x80); returns through pop {r4, r5, r6, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x90 -> constant 0x022459b4 (image word 0x022459b4)
 *   branch +0x18 -> +0x30
 *   branch +0x20 -> +0x40
 *   branch +0x28 -> +0x68
 *   branch +0x2c -> +0x78
 *   branch +0x3c -> +0x78
 *   branch +0x48 -> +0x78
 *   branch +0x64 -> +0x78
 *   branch +0x7c -> +0x88
 *   back edge +0x80 -> +0x00
 *   test +0x14 cmp r0, #0
 *   test +0x1c cmp r0, #1
 *   test +0x24 cmp r0, #2
 *   test +0x44 cmp r0, r4
 *   test +0x78 cmp r6, #0
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02215600; the literal pool and
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

extern void native_fn_02215dac(void);
extern void native_fn_02215ee4(void);
extern void native_fn_02215f78(void);


asm u32 native_ov000_02215600 (register u32 a0)
{
ov000_02215600_L0:
    stmdb sp!, {r4, r5, r6, lr}
    ldr r5, =0x022459b4
    mov r6, #0
    ldr r0, [r5, #0x4]
    ldr r4, [r5]
    cmp r0, #0
    beq ov000_02215600_L30
    cmp r0, #1
    beq ov000_02215600_L40
    cmp r0, #2
    beq ov000_02215600_L68
    b ov000_02215600_L78
ov000_02215600_L30:
    bl native_fn_02215dac
    mov r0, #1
    str r0, [r5, #0x4]
    b ov000_02215600_L78
ov000_02215600_L40:
    bl native_fn_02215ee4
    cmp r0, r4
    beq ov000_02215600_L78
    ldr r2, [r5]
    mov r1, #2
    str r2, [r5, #0xc]
    str r1, [r5, #0x4]
    str r0, [r5, #0x8]
    mov r6, #1
    b ov000_02215600_L78
ov000_02215600_L68:
    bl native_fn_02215f78
    mov r0, r6
    ldr r4, [r5, #0x8]
    str r0, [r5, #0x4]
ov000_02215600_L78:
    cmp r6, #0
    beq ov000_02215600_L88
    bl ov000_02215600_L0
    mov r4, r0
ov000_02215600_L88:
    mov r0, r4
    ldmia sp!, {r4, r5, r6, pc}
}
