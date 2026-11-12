/* ov000 row 0x022171f8: 104 bytes.
 *
 * What it does: 24 instructions; 6 call(s) to 0x02041814, 0x0202a498, 0x020653ac, +3 more; loops (back edge at +0x04); returns through pop {r3, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x60 -> constant 0x0224532c (image word 0x0224532c)
 *   pool +0x64 -> constant 0x022459b4 (image word 0x022459b4)
 *   branch +0x20 -> +0x38
 *   test +0x08 cmp r0, #1
 *   test +0x1c cmp r1, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022171f8; the literal pool and
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

extern void native_fn_02041814(void);
extern void native_fn_0202a498(void);
extern void native_fn_020653ac(void);
extern void native_fn_02045738(void);
extern void native_fn_02215850(void);
extern void native_fn_02215a14(void);


asm u32 native_ov000_022171f8 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    bl native_fn_02041814
    cmp r0, #1
    moveq r0, #1
    ldmeqia sp!, {r3, pc}
    ldr r0, =0x0224532c
    ldr r1, [r0, #0x14]
    cmp r1, #0
    beq ov000_022171f8_L38
    mov r0, #2
    bl native_fn_0202a498
    ldr r0, =0x0224532c
    mov r1, #0
    str r1, [r0, #0x14]
ov000_022171f8_L38:
    bl native_fn_020653ac
    mov r0, #1
    bl native_fn_02045738
    bl native_fn_02215850
    bl native_fn_02215a14
    ldr r0, =0x022459b4
    mov r1, #13
    strb r1, [r0, #0x494]
    mov r0, #3
    ldmia sp!, {r3, pc}
}
