/* ov000 row 0x0220155c: 84 bytes.
 *
 * What it does: 17 instructions; 2 call(s) to 0x0205db90, 0x0205d9e8; loops (back edge at +0x14); 4 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x44 -> native_data_0222f4bc (image word 0x0222f4bc)
 *   pool +0x48 -> constant 0x020db220 (image word 0x020db220)
 *   pool +0x4c -> constant 0x020db21c (image word 0x020db21c)
 *   pool +0x50 -> constant 0x02237774 (image word 0x02237774)
 *   2 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0220155c; the literal pool and
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

extern u8 native_data_0222f4bc[];
extern void native_fn_0205db90(void);
extern void native_fn_0205d9e8(void);


asm u32 native_ov000_0220155c (register u32 a0)
{
    stmdb sp!, {lr}
    sub sp, sp, #36
    ldr r1, =native_data_0222f4bc
    add r0, sp, #4
    mvn r2, #0
    bl native_fn_0205db90
    mov r12, #2
    ldr r2, =0x020db220
    ldr r3, =0x020db21c
    add r1, sp, #4
    mov r0, #1
    str r12, [sp]
    bl native_fn_0205d9e8
    ldr r1, =0x02237774
    str r0, [r1]
    add sp, sp, #36
    ldmia sp!, {pc}
}
