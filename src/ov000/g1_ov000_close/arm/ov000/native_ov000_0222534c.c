/* ov000 row 0x0222534c: 232 bytes.
 *
 * What it does: 55 instructions; 6 call(s) to 0x02008e0c, 0x02227cec, 0x02227ebc, +3 more; loops (back edge at +0x3c); returns through pop {r3, r4, r5, r6, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xdc -> constant 0x02246c84 (image word 0x02246c84)
 *   pool +0xe0 -> constant 0x02246e19 (image word 0x02246e19)
 *   pool +0xe4 -> constant 0x02246e18 (image word 0x02246e18)
 *   branch +0x74 -> +0x88
 *   test +0x6c cmp r5, #63
 *   test +0x78 cmp r5, #0
 *   test +0xa0 cmp r2, #63
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0222534c; the literal pool and
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
extern void native_fn_02227cec(void);
extern void native_fn_02227ebc(void);
extern void native_fn_020d16b8(void);
extern void native_fn_01ffa5ac(void);


asm u32 native_ov000_0222534c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, lr}
    sub sp, sp, #284
    ldr r4, =0x02246c84
    mov r2, #132
    ldrb r0, [r4, #0x190]
    ldrb r1, [r4, #0x18e]
    smulbb r0, r0, r2
    adds r0, r4, r0
    rsb r6, r1, r1, lsl #6
    addeq sp, sp, #284
    moveq r0, #0
    ldmeqia sp!, {r3, r4, r5, r6, pc}
    ldrb r3, [r4, #0x190]
    add r1, sp, #152
    mla r0, r3, r2, r4
    bl native_fn_02008e0c
    add r0, sp, #152
    bl native_fn_02227cec
    add r0, sp, #152
    bl native_fn_02227ebc
    add r0, sp, #152
    add r1, sp, #0
    bl native_fn_020d16b8
    mov r0, r4
    ldrb r0, [r0, #0x18e]
    rsb r0, r0, r0, lsl #6
    rsb r5, r0, #152
    cmp r5, #63
    movgt r5, #63
    bgt ov000_0222534c_L88
    cmp r5, #0
    addlt sp, sp, #284
    movlt r0, #0
    ldmltia sp!, {r3, r4, r5, r6, pc}
ov000_0222534c_L88:
    ldrb r3, [r4, #0x190]
    ldr r0, =0x02246c84
    rsb r1, r6, #152
    sub r2, r1, #1
    strb r3, [r0, #0x194]
    add r0, sp, #0
    cmp r2, #63
    ldr r1, =0x02246e19
    movgt r2, #63
    add r0, r0, r6
    bl native_fn_02008e0c
    ldrb r2, [r4, #0x18e]
    ldr r0, =0x02246e18
    add r1, r5, #1
    add r2, r2, #48
    mov r2, r2, lsl #16
    mov r2, r2, lsr #16
    bl native_fn_01ffa5ac
    mov r0, #1
    add sp, sp, #284
    ldmia sp!, {r3, r4, r5, r6, pc}
}
