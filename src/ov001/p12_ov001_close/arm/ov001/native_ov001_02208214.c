/* ov001 row 0x02208214: 140 bytes.
 *
 * What it does: 34 instructions; 6 call(s) to 0x02207938, 0x0201d444, 0x0202a8e0, +3 more; loops (back edge at +0x0c); returns through pop {r3, r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 6 calls (34 instructions, 6 calls, 1 branch, 7 back edges, 1 literal slot).
 *
 *   pool +0x88 -> native_data_0222f078 (image word 0x0222f078)
 *   back edge +0x38 -> +0x20
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02208214; the literal pool and
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

extern void native_fn_02207938(void);
extern u8 native_data_0222f078[];
extern void native_fn_0201d444(void);
extern void native_fn_0202a8e0(void);
extern void native_fn_0203cc2c(void);
extern void native_fn_02008e0c(void);
extern void native_fn_0202a498(void);


asm u32 native_ov001_02208214 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    sub sp, sp, #32
    mov r5, r0
    bl native_fn_02207938
    mov r4, r0
    add r2, sp, #0
    mov r1, #8
    mov r0, #0
ov001_02208214_L20:
    strb r0, [r2]
    strb r0, [r2, #0x1]
    strb r0, [r2, #0x2]
    strb r0, [r2, #0x3]
    add r2, r2, #4
    subs r1, r1, #1
    bne ov001_02208214_L20
    ldr r1, =native_data_0222f078
    add r0, sp, #0
    mov r2, r5
    bl native_fn_0201d444
    add r0, sp, #0
    bl native_fn_0202a8e0
    mov r5, r0
    add r0, sp, #0
    mov r1, #2
    bl native_fn_0203cc2c
    ldr r1, [r4, #0x14]
    mov r4, r0
    mov r2, r5
    bl native_fn_02008e0c
    mov r1, r4
    mov r0, #2
    bl native_fn_0202a498
    add sp, sp, #32
    ldmia sp!, {r3, r4, r5, pc}
}
