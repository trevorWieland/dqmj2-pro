/* ov000 row 0x02219e40: 152 bytes.
 *
 * What it does: 37 instructions; 4 call(s) to 0x020462cc, 0x02084924, 0x02085320, +1 more; loops (back edge at +0x0c); returns through pop {r3, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x94 -> constant 0x02246044 (image word 0x02246044)
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02219e40; the literal pool and
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

extern void native_fn_020462cc(void);
extern void native_fn_02084924(void);
extern void native_fn_02085320(void);
extern void native_fn_02085270(void);


asm u32 native_ov000_02219e40 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    sub sp, sp, #24
    mov r0, #0
    bl native_fn_020462cc
    ldr r1, [r0, #0x8]
    mov r0, #6
    mov r1, r1, lsr #5
    add r1, r1, #1
    str r0, [sp]
    mov r0, #2
    str r0, [sp, #0x4]
    mov r0, #1
    str r0, [sp, #0x8]
    add r1, r1, #1
    str r1, [sp, #0xc]
    mov r1, #0
    str r1, [sp, #0x10]
    mov r2, #18
    mov r3, #32
    str r0, [sp, #0x14]
    bl native_fn_02084924
    ldr r3, =0x02246044
    mov r1, #0
    mov r2, #9
    str r0, [r3, #0x8]
    bl native_fn_02085320
    ldr r0, =0x02246044
    mov r1, #8
    ldr r0, [r0, #0x8]
    mov r2, #16
    add r0, r0, #60
    bl native_fn_02085270
    ldr r0, =0x02246044
    mov r1, #0
    str r1, [r0]
    add sp, sp, #24
    ldmia sp!, {r3, pc}
}
