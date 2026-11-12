/* ov000 row 0x02215324: 152 bytes.
 *
 * What it does: 37 instructions; 4 call(s) to 0x0207baa0, 0x02210f74, 0x0207afec, +1 more; loops (back edge at +0x30); returns through pop {r3, r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x94 -> constant 0x0000270f (image word 0x0000270f)
 *   branch +0x40 -> +0x5c
 *   branch +0x58 -> +0x88
 *   branch +0x6c -> +0x7c
 *   branch +0x78 -> +0x88
 *   test +0x3c cmp r4, r0
 *   test +0x68 cmp r0, #0
 *   test +0x70 cmp r4, r0
 *   test +0x80 cmp r4, r0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02215324; the literal pool and
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

extern void native_fn_0207baa0(void);
extern void native_fn_02210f74(void);
extern void native_fn_0207afec(void);


asm u32 native_ov000_02215324 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    sub sp, sp, #8
    mov r12, #0
    str r12, [sp]
    mov r4, r1
    str r12, [sp, #0x4]
    mov r6, r2
    mov r7, r0
    ldrsh r1, [r4, #24]
    ldrsh r2, [r4, #46]
    mov r0, r6
    mov r5, r3
    bl native_fn_0207baa0
    mov r4, r0
    mvn r0, #0
    cmp r4, r0
    bne ov000_02215324_L5c
    mov r0, r7
    mov r1, r5
    bl native_fn_02210f74
    ldrsh r1, [r7, #36]
    sub r4, r0, r1
    b ov000_02215324_L88
ov000_02215324_L5c:
    mov r0, r6
    bl native_fn_0207afec
    ldrsh r0, [r0, #28]
    cmp r0, #0
    ble ov000_02215324_L7c
    cmp r4, r0
    movge r4, r0
    b ov000_02215324_L88
ov000_02215324_L7c:
    ldr r0, =0x0000270f
    cmp r4, r0
    movge r4, r0
ov000_02215324_L88:
    mov r0, r4
    add sp, sp, #8
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
