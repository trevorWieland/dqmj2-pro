/* ov001 row 0x021feaa8: 168 bytes.
 *
 * What it does: 39 instructions; 6 call(s) to 0x0201d444, 0x0202a8e0, 0x0203cc2c, +3 more; loops (back edge at +0x2c); returns through pop {r3, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: loop with 6 calls (39 instructions, 6 calls, 2 branches, 7 back edges, 3 literal slots).
 *
 *   pool +0x9c -> native_data_0222ef64 (image word 0x0222ef64)
 *   pool +0xa0 -> constant 0x02239c10 (image word 0x02239c10)
 *   pool +0xa4 -> native_data_0222ef7c (image word 0x0222ef7c)
 *   back edge +0x2c -> +0x14
 *   branch +0x48 -> +0x60
 *   test +0x44 cmp r0, #0
 *   test +0x74 cmp r0, #0
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021feaa8; the literal pool and
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

extern u8 native_data_0222ef64[];
extern void native_fn_0201d444(void);
extern void native_fn_0202a8e0(void);
extern void native_fn_0203cc2c(void);
extern u8 native_data_0222ef7c[];


asm u32 native_ov001_021feaa8 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    sub sp, sp, #32
    add r2, sp, #0
    mov r1, #8
    mov r0, #0
ov001_021feaa8_L14:
    strb r0, [r2]
    strb r0, [r2, #0x1]
    strb r0, [r2, #0x2]
    strb r0, [r2, #0x3]
    add r2, r2, #4
    subs r1, r1, #1
    bne ov001_021feaa8_L14
    ldr r1, =native_data_0222ef64
    add r0, sp, #0
    bl native_fn_0201d444
    add r0, sp, #0
    bl native_fn_0202a8e0
    cmp r0, #0
    beq ov001_021feaa8_L60
    add r0, sp, #0
    mov r1, #2
    bl native_fn_0203cc2c
    ldr r1, =0x02239c10
    str r0, [r1, #0x48]
ov001_021feaa8_L60:
    ldr r1, =native_data_0222ef7c
    add r0, sp, #0
    bl native_fn_0201d444
    add r0, sp, #0
    bl native_fn_0202a8e0
    cmp r0, #0
    addeq sp, sp, #32
    ldmeqia sp!, {r3, pc}
    add r0, sp, #0
    mov r1, #2
    bl native_fn_0203cc2c
    ldr r1, =0x02239c10
    str r0, [r1, #0x44]
    add sp, sp, #32
    ldmia sp!, {r3, pc}
}
