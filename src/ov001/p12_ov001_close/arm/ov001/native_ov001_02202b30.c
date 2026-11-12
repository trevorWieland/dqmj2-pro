/* ov001 row 0x02202b30: 84 bytes.
 *
 * What it does: 17 instructions; 2 call(s) to 0x0205db90, 0x0205da98; loops (back edge at +0x14); 4 literal slot(s) in the extent
 *
 * Decoded shape: block fill (17 instructions, 2 calls, 0 branches, 2 back edges, 4 literal slots).
 *
 *   pool +0x44 -> native_data_0222eff0 (image word 0x0222eff0)
 *   pool +0x48 -> constant 0x020db21c (image word 0x020db21c)
 *   pool +0x4c -> constant 0x0223a8ec (image word 0x0223a8ec)
 *   pool +0x50 -> constant 0x020db220 (image word 0x020db220)
 *   3 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02202b30; the literal pool and
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

extern u8 native_data_0222eff0[];
extern void native_fn_0205db90(void);
extern void native_fn_0205da98(void);


asm u32 native_ov001_02202b30 (register u32 a0)
{
    stmdb sp!, {lr}
    sub sp, sp, #44
    ldr r1, =native_data_0222eff0
    add r0, sp, #12
    mvn r2, #0
    bl native_fn_0205db90
    ldr r0, =0x020db21c
    mov r12, #2
    stmia sp, {r0, r12}
    ldr r0, =0x0223a8ec
    ldr r3, =0x020db220
    add r2, sp, #12
    mov r1, #12288
    str r12, [sp, #0x8]
    bl native_fn_0205da98
    add sp, sp, #44
    ldmia sp!, {pc}
}
