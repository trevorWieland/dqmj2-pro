/* ov000 row 0x022252ac: 160 bytes.
 *
 * What it does: 37 instructions; 2 call(s) to 0x02008e0c, 0x01ffa5ac; loops (back edge at +0x6c); returns through pop {r3, r4, r5, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x94 -> constant 0x02246c84 (image word 0x02246c84)
 *   pool +0x98 -> constant 0x02246e19 (image word 0x02246e19)
 *   pool +0x9c -> constant 0x02246e18 (image word 0x02246e18)
 *   branch +0x38 -> +0x48
 *   test +0x30 cmp r5, #67
 *   test +0x3c cmp r5, #0
 *   test +0x58 cmp r2, #67
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022252ac; the literal pool and
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

extern void native_fn_02008e0c(void);
extern void native_fn_01ffa5ac(void);


asm u32 native_ov000_022252ac (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r4, =0x02246c84
    mov r0, #132
    ldrb r3, [r4, #0x190]
    ldrb r2, [r4, #0x18e]
    mov r1, #67
    smulbb r0, r3, r0
    adds r12, r4, r0
    smulbb r14, r2, r1
    moveq r0, #0
    ldmeqia sp!, {r3, r4, r5, pc}
    rsb r5, lr, #132
    cmp r5, #67
    movgt r5, r1
    bgt ov000_022252ac_L48
    cmp r5, #0
    movlt r0, #0
    ldmltia sp!, {r3, r4, r5, pc}
ov000_022252ac_L48:
    ldrb r3, [r4, #0x190]
    rsb r1, lr, #132
    sub r2, r1, #1
    ldr r0, =0x02246c84
    cmp r2, #67
    strb r3, [r0, #0x194]
    ldr r1, =0x02246e19
    movgt r2, #67
    add r0, r12, lr
    bl native_fn_02008e0c
    ldrb r2, [r4, #0x18e]
    ldr r0, =0x02246e18
    add r1, r5, #1
    add r2, r2, #48
    mov r2, r2, lsl #16
    mov r2, r2, lsr #16
    bl native_fn_01ffa5ac
    mov r0, #1
    ldmia sp!, {r3, r4, r5, pc}
}
