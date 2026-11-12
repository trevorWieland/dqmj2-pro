/* ov000 row 0x02219f08: 140 bytes.
 *
 * What it does: 34 instructions; 6 call(s) to 0x0201d444, 0x0202a8e0, 0x0203cc2c, +3 more; loops (back edge at +0x2c); returns through pop {r4, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x88 -> native_data_0222facc (image word 0x0222facc)
 *   back edge +0x2c -> +0x14
 *   test +0x44 cmp r0, #0
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02219f08; the literal pool and
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

extern u8 native_data_0222facc[];
extern void native_fn_0201d444(void);
extern void native_fn_0202a8e0(void);
extern void native_fn_0203cc2c(void);
extern void native_fn_020481b8(void);
extern void native_fn_02048308(void);
extern void native_fn_0202a498(void);


asm u32 native_ov000_02219f08 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    sub sp, sp, #32
    add r2, sp, #0
    mov r1, #8
    mov r0, #0
ov000_02219f08_L14:
    strb r0, [r2]
    strb r0, [r2, #0x1]
    strb r0, [r2, #0x2]
    strb r0, [r2, #0x3]
    add r2, r2, #4
    subs r1, r1, #1
    bne ov000_02219f08_L14
    ldr r1, =native_data_0222facc
    add r0, sp, #0
    bl native_fn_0201d444
    add r0, sp, #0
    bl native_fn_0202a8e0
    cmp r0, #0
    addeq sp, sp, #32
    ldmeqia sp!, {r4, pc}
    add r0, sp, #0
    mov r1, #2
    bl native_fn_0203cc2c
    mov r4, r0
    add r0, r4, #2
    mov r1, #10
    mov r2, #4
    bl native_fn_020481b8
    bl native_fn_02048308
    mov r1, r4
    mov r0, #2
    bl native_fn_0202a498
    add sp, sp, #32
    ldmia sp!, {r4, pc}
}
