/* ov000 row 0x022158c8: 152 bytes.
 *
 * What it does: 38 instructions; 6 call(s) to 0x02215064, 0x0205f98c, 0x0221750c, +3 more; loops (back edge at +0x38); returns through bx lr
 *
 * Decoded shape: aggregate copy.
 *
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022158c8; the literal pool and
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

extern void native_fn_02215064(void);
extern void native_fn_0205f98c(void);
extern void native_fn_0221750c(void);
extern void native_fn_02215984(void);
extern void native_fn_02048a94(void);
extern void native_fn_02048a9c(void);


asm u32 native_ov000_022158c8 (register u32 a0)
{
    stmdb sp!, {r0, r1, r2, r3}
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    ldrsh r1, [sp, #28]
    mov r4, r0
    mov r5, #7
    strh r1, [r4, #20]
    ldrsh r12, [sp, #30]
    mov r1, #1
    mov r7, r2
    strh r12, [r4, #22]
    strb r5, [r4, #0x20]
    mov r2, r1
    strb r1, [r4, #0x21]
    mov r6, r3
    bl native_fn_02215064
    ldr r0, [r4, #0x1c]
    mov r1, #0
    bl native_fn_0205f98c
    and r1, r7, #255
    mov r5, r0
    bl native_fn_0221750c
    add r1, sp, #28
    mov r0, r4
    bl native_fn_02215984
    ldr r1, [r5, #0x7c]
    mov r0, r5
    orr r1, r1, #2
    str r1, [r5, #0x7c]
    ldrb r1, [r4, #0x20]
    bl native_fn_02048a94
    ldrb r1, [r4, #0x21]
    mov r0, r5
    bl native_fn_02048a9c
    str r6, [r4]
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, lr}
    add sp, sp, #16
    bx lr
}
