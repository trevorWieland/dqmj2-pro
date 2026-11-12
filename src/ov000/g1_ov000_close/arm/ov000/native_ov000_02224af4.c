/* ov000 row 0x02224af4: 144 bytes.
 *
 * What it does: 34 instructions; 8 call(s) to 0x01ffa5ac, 0x022256e4, 0x02062378, +5 more; loops (back edge at +0x10); returns through pop {r4, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x88 -> constant 0x022468d5 (image word 0x022468d5)
 *   pool +0x8c -> constant 0x022468b8 (image word 0x022468b8)
 *   test +0x2c cmp r0, #19
 *   test +0x3c cmp r0, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02224af4; the literal pool and
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

extern void native_fn_01ffa5ac(void);
extern void native_fn_022256e4(void);
extern void native_fn_02062378(void);
extern void native_fn_02062520(void);
extern void native_fn_02061284(void);
extern void native_fn_02061260(void);
extern void native_fn_02227648(void);
extern void native_fn_02041538(void);


asm u32 native_ov000_02224af4 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldr r0, =0x022468d5
    mov r1, #1
    mov r2, #25
    bl native_fn_01ffa5ac
    mov r0, #25
    bl native_fn_022256e4
    movs r4, r0
    moveq r0, #0
    ldmeqia sp!, {r4, pc}
    bl native_fn_02062378
    cmp r0, #19
    movne r0, #0
    ldmneia sp!, {r4, pc}
    bl native_fn_02062520
    cmp r0, #0
    mov r0, #0
    ldmeqia sp!, {r4, pc}
    bl native_fn_02061284
    mov r0, #0
    bl native_fn_02061260
    ldrsb r1, [r4]
    ldr r0, =0x022468b8
    strb r1, [r0, #0x1e]
    bl native_fn_02227648
    mov r0, #0
    mov r1, #2
    mov r2, #10
    bl native_fn_02041538
    ldr r0, =0x022468b8
    mov r1, #2
    str r1, [r0, #0x14]
    mov r0, #0
    ldmia sp!, {r4, pc}
}
