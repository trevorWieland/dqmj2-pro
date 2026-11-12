/* ov001 row 0x022136fc: 172 bytes.
 *
 * What it does: 35 instructions; 4 call(s) to 0x0205db90, 0x0205da98, 0x0205db90, +1 more; loops (back edge at +0x14); 8 literal slot(s) in the extent
 *
 * Decoded shape: loop with 4 calls (35 instructions, 4 calls, 0 branches, 4 back edges, 8 literal slots).
 *
 *   pool +0x8c -> native_data_0222f188 (image word 0x0222f188)
 *   pool +0x90 -> constant 0x020dabb0 (image word 0x020dabb0)
 *   pool +0x94 -> constant 0x0223e198 (image word 0x0223e198)
 *   pool +0x98 -> constant 0x020dabbc (image word 0x020dabbc)
 *   pool +0x9c -> native_data_0222f194 (image word 0x0222f194)
 *   pool +0xa0 -> constant 0x020dbc10 (image word 0x020dbc10)
 *   pool +0xa4 -> constant 0x0223f198 (image word 0x0223f198)
 *   pool +0xa8 -> constant 0x020dbc14 (image word 0x020dbc14)
 *   2 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022136fc; the literal pool and
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

extern u8 native_data_0222f188[];
extern void native_fn_0205db90(void);
extern void native_fn_0205da98(void);
extern u8 native_data_0222f194[];


asm u32 native_ov001_022136fc (register u32 a0)
{
    stmdb sp!, {lr}
    sub sp, sp, #44
    ldr r1, =native_data_0222f188
    add r0, sp, #12
    mvn r2, #0
    bl native_fn_0205db90
    ldr r0, =0x020dabb0
    mov r1, #6
    str r0, [sp]
    str r1, [sp, #0x4]
    mov r12, #2
    ldr r0, =0x0223e198
    ldr r3, =0x020dabbc
    add r2, sp, #12
    mov r1, #4096
    str r12, [sp, #0x8]
    bl native_fn_0205da98
    ldr r1, =native_data_0222f194
    add r0, sp, #12
    mvn r2, #0
    bl native_fn_0205db90
    ldr r0, =0x020dbc10
    mov r1, #1
    str r0, [sp]
    str r1, [sp, #0x4]
    mov r1, #2
    str r1, [sp, #0x8]
    ldr r0, =0x0223f198
    ldr r3, =0x020dbc14
    add r2, sp, #12
    mov r1, #14336
    bl native_fn_0205da98
    mov r0, #1
    add sp, sp, #44
    ldmia sp!, {pc}
}
