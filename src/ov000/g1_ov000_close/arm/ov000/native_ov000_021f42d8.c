/* ov000 row 0x021f42d8: 1180 bytes.
 *
 * What it does: 288 instructions; 38 call(s) to 0x02061c1c, 0x01ffb50c, 0x02061c1c, +35 more; loops (back edge at +0x28); 7 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x480 -> native_data_0222f2b4 (image word 0x0222f2b4)
 *   pool +0x484 -> native_data_0222f2b8 (image word 0x0222f2b8)
 *   pool +0x488 -> native_data_0222f2bc (image word 0x0222f2bc)
 *   pool +0x48c -> native_data_0222f2c0 (image word 0x0222f2c0)
 *   pool +0x490 -> native_data_0222f2c4 (image word 0x0222f2c4)
 *   pool +0x494 -> native_data_0222f2c8 (image word 0x0222f2c8)
 *   pool +0x498 -> native_data_0222f2cc (image word 0x0222f2cc)
 *   2 block transfer(s), 70 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f42d8; the literal pool and
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

extern void native_fn_02061c1c(void);
extern void native_fn_01ffb50c(void);
extern u8 native_data_0222f2b4[];
extern void native_fn_01ffb648(void);
extern u8 native_data_0222f2b8[];
extern u8 native_data_0222f2bc[];
extern u8 native_data_0222f2c0[];
extern u8 native_data_0222f2c4[];
extern u8 native_data_0222f2c8[];
extern u8 native_data_0222f2cc[];
extern void native_fn_02045ed0(void);
extern void native_fn_021f47ec(void);
extern void native_fn_02061260(void);


asm u32 native_ov000_021f42d8 (register u32 a0)
{
    stmdb sp!, {lr}
    sub sp, sp, #12
    mov r1, #2
    str r1, [sp]
    mov r12, #0
    str r12, [sp, #0x4]
    mov r0, #6
    mov r2, #4
    mov r3, #8
    str r12, [sp, #0x8]
    bl native_fn_02061c1c
    mov r3, #0
    mov r0, #6
    mov r1, #16
    mov r2, #4
    str r3, [sp]
    bl native_fn_01ffb50c
    mov r0, #2
    str r0, [sp]
    mov r12, #0
    str r12, [sp, #0x4]
    mov r0, #7
    mov r1, #15
    mov r2, #4
    mov r3, #1
    str r12, [sp, #0x8]
    bl native_fn_02061c1c
    ldr r1, =native_data_0222f2b4
    mov r0, #7
    bl native_fn_01ffb648
    mov r0, #2
    str r0, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    str r0, [sp, #0x8]
    mov r0, #8
    mov r1, #16
    mov r2, #4
    mov r3, #12
    bl native_fn_02061c1c
    mov r0, #2
    str r0, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    str r0, [sp, #0x8]
    mov r0, #9
    mov r1, #3
    mov r2, #8
    mov r3, r2
    bl native_fn_02061c1c
    mov r0, #0
    str r0, [sp]
    mov r0, #9
    mov r1, #16
    mov r2, #4
    mov r3, #27
    bl native_fn_01ffb50c
    mov r0, #2
    str r0, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    str r0, [sp, #0x8]
    mov r0, #10
    mov r1, #15
    mov r2, #8
    mov r3, #1
    bl native_fn_02061c1c
    ldr r1, =native_data_0222f2b8
    mov r0, #10
    bl native_fn_01ffb648
    mov r0, #2
    mov r2, #8
    str r0, [sp]
    mov r12, #0
    str r12, [sp, #0x4]
    mov r3, r2
    mov r0, #11
    mov r1, #16
    str r12, [sp, #0x8]
    bl native_fn_02061c1c
    mov r0, #2
    str r0, [sp]
    mov r12, #0
    str r12, [sp, #0x4]
    mov r0, #12
    mov r1, #3
    mov r2, #10
    mov r3, #8
    str r12, [sp, #0x8]
    bl native_fn_02061c1c
    mov r1, #0
    mov r0, #12
    str r1, [sp]
    mov r1, #16
    mov r2, #4
    mov r3, #28
    bl native_fn_01ffb50c
    mov r0, #2
    str r0, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    str r0, [sp, #0x8]
    mov r0, #13
    mov r1, #15
    mov r2, #10
    mov r3, #1
    bl native_fn_02061c1c
    mov r0, #13
    ldr r1, =native_data_0222f2bc
    bl native_fn_01ffb648
    mov r0, #2
    str r0, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    str r0, [sp, #0x8]
    mov r0, #14
    mov r1, #16
    mov r2, #10
    mov r3, #8
    bl native_fn_02061c1c
    mov r0, #2
    str r0, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    str r0, [sp, #0x8]
    mov r0, #15
    mov r1, #3
    mov r2, #12
    mov r3, #8
    bl native_fn_02061c1c
    mov r12, #0
    mov r0, #15
    mov r1, #16
    mov r2, #4
    mov r3, #29
    str r12, [sp]
    bl native_fn_01ffb50c
    mov r0, #2
    str r0, [sp]
    mov r12, #0
    str r12, [sp, #0x4]
    mov r0, #16
    mov r1, #15
    mov r2, #12
    mov r3, #1
    str r12, [sp, #0x8]
    bl native_fn_02061c1c
    ldr r1, =native_data_0222f2c0
    mov r0, #16
    bl native_fn_01ffb648
    mov r0, #2
    str r0, [sp]
    mov r1, #0
    str r1, [sp, #0x4]
    mov r0, #17
    str r1, [sp, #0x8]
    mov r1, #16
    mov r2, #12
    mov r3, #8
    bl native_fn_02061c1c
    mov r0, #2
    str r0, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    str r0, [sp, #0x8]
    mov r0, #21
    mov r1, #3
    mov r2, #14
    mov r3, #8
    bl native_fn_02061c1c
    mov r0, #0
    str r0, [sp]
    mov r0, #21
    mov r1, #16
    mov r2, #4
    mov r3, #30
    bl native_fn_01ffb50c
    mov r0, #2
    str r0, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    str r0, [sp, #0x8]
    mov r0, #22
    mov r1, #15
    mov r2, #14
    mov r3, #1
    bl native_fn_02061c1c
    mov r0, #22
    ldr r1, =native_data_0222f2c4
    bl native_fn_01ffb648
    mov r0, #2
    str r0, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    str r0, [sp, #0x8]
    mov r0, #23
    mov r1, #16
    mov r2, #14
    mov r3, r2
    bl native_fn_02061c1c
    mov r0, #2
    str r0, [sp]
    mov r12, #0
    str r12, [sp, #0x4]
    mov r0, #18
    mov r1, #3
    mov r2, #16
    mov r3, #8
    str r12, [sp, #0x8]
    bl native_fn_02061c1c
    mov r12, #0
    mov r0, #18
    mov r1, #16
    mov r2, #4
    mov r3, #31
    str r12, [sp]
    bl native_fn_01ffb50c
    mov r0, #2
    str r0, [sp]
    mov r12, #0
    str r12, [sp, #0x4]
    mov r0, #19
    mov r1, #15
    mov r2, #16
    mov r3, #1
    str r12, [sp, #0x8]
    bl native_fn_02061c1c
    ldr r1, =native_data_0222f2c8
    mov r0, #19
    bl native_fn_01ffb648
    mov r0, #2
    str r0, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    str r0, [sp, #0x8]
    mov r0, #20
    mov r1, #16
    mov r2, r1
    mov r3, #8
    bl native_fn_02061c1c
    mov r0, #2
    str r0, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    str r0, [sp, #0x8]
    mov r0, #24
    mov r1, #3
    mov r2, #18
    mov r3, #8
    bl native_fn_02061c1c
    mov r0, #0
    str r0, [sp]
    mov r0, #24
    mov r1, #16
    mov r2, #4
    mov r3, #33
    bl native_fn_01ffb50c
    mov r0, #2
    str r0, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    str r0, [sp, #0x8]
    mov r0, #25
    mov r1, #15
    mov r2, #18
    mov r3, #1
    bl native_fn_02061c1c
    ldr r1, =native_data_0222f2cc
    mov r0, #25
    bl native_fn_01ffb648
    mov r0, #2
    str r0, [sp]
    mov r12, #0
    str r12, [sp, #0x4]
    mov r0, #26
    mov r1, #16
    mov r2, #18
    mov r3, #14
    str r12, [sp, #0x8]
    bl native_fn_02061c1c
    mov r0, #1
    bl native_fn_02045ed0
    mov r0, #255
    bl native_fn_021f47ec
    mov r0, #0
    bl native_fn_02061260
    add sp, sp, #12
    ldmia sp!, {pc}
}
