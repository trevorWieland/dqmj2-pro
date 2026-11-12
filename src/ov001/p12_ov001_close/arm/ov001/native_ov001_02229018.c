/* ov001 row 0x02229018: 184 bytes.
 *
 * What it does: 45 instructions; 8 call(s) to 0x02223fe8, 0x02226bdc, 0x0222595c, +5 more; loops (back edge at +0x30); returns through pop {r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block copy loop (45 instructions, 8 calls, 0 branches, 8 back edges, 1 literal slot).
 *
 *   pool +0xb4 -> native_data_0222e608 (image word 0x0222e608)
 *   2 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02229018; the literal pool and
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

extern u8 native_data_0222e608[];
extern void native_fn_02223fe8(void);
extern void native_fn_02226bdc(void);
extern void native_fn_0222595c(void);
extern void native_fn_022240a4(void);
extern void native_fn_0222470c(void);
extern void native_fn_02224570(void);
extern void native_fn_02224050(void);
extern void native_fn_02226cb0(void);


asm u32 native_ov001_02229018 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, lr}
    sub sp, sp, #20
    ldr r1, =native_data_0222e608
    add r3, sp, #8
    mov r7, r0
    ldmia r1, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    ldr r5, [r7, #0x4]
    mov r0, r3
    mov r1, r5
    ldr r6, [r7, #0x8]
    ldr r4, [r7]
    bl native_fn_02223fe8
    add r0, sp, #8
    mov r1, r7
    mov r2, #75
    bl native_fn_02226bdc
    add r0, sp, #8
    mov r1, r5
    mov r2, r6
    bl native_fn_0222595c
    mov r0, #1
    str r0, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    mov r1, r4
    mov r3, r6
    add r0, sp, #8
    mov r2, r5
    bl native_fn_022240a4
    add r0, sp, #8
    mov r1, r5
    mov r2, #2
    mov r3, #4
    bl native_fn_0222470c
    mov r1, r5
    add r0, sp, #8
    mov r2, #4
    bl native_fn_02224570
    add r0, sp, #8
    bl native_fn_02224050
    add r0, sp, #8
    bl native_fn_02226cb0
    add sp, sp, #20
    ldmia sp!, {r4, r5, r6, r7, pc}
}
