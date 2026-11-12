/* ov001 row 0x022285f8: 164 bytes.
 *
 * What it does: 40 instructions; 9 call(s) to 0x02223fe8, 0x02226bdc, 0x0207afec, +6 more; loops (back edge at +0x2c); returns through pop {r3, r4, r5, r6, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block copy loop (40 instructions, 9 calls, 0 branches, 9 back edges, 1 literal slot).
 *
 *   pool +0xa0 -> native_data_0222e6e0 (image word 0x0222e6e0)
 *   2 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022285f8; the literal pool and
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

extern u8 native_data_0222e6e0[];
extern void native_fn_02223fe8(void);
extern void native_fn_02226bdc(void);
extern void native_fn_0207afec(void);
extern void native_fn_02225534(void);
extern void native_fn_02225354(void);
extern void native_fn_0222470c(void);
extern void native_fn_02224570(void);
extern void native_fn_02224050(void);
extern void native_fn_02226cb0(void);


asm u32 native_ov001_022285f8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, lr}
    sub sp, sp, #12
    ldr r1, =native_data_0222e6e0
    add r3, sp, #0
    mov r6, r0
    ldmia r1, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    ldr r5, [r6, #0x4]
    mov r0, r3
    mov r1, r5
    ldr r4, [r6, #0x8]
    bl native_fn_02223fe8
    add r0, sp, #0
    mov r1, r6
    mov r2, #57
    bl native_fn_02226bdc
    mov r0, r4
    bl native_fn_0207afec
    ldrb r2, [r0, #0x1f]
    add r0, sp, #0
    mov r1, r5
    bl native_fn_02225534
    add r0, sp, #0
    mov r1, r5
    bl native_fn_02225354
    add r0, sp, #0
    mov r1, r5
    mov r2, #0
    mov r3, #4
    bl native_fn_0222470c
    mov r1, r5
    add r0, sp, #0
    mov r2, #4
    bl native_fn_02224570
    add r0, sp, #0
    bl native_fn_02224050
    add r0, sp, #0
    bl native_fn_02226cb0
    add sp, sp, #12
    ldmia sp!, {r3, r4, r5, r6, pc}
}
