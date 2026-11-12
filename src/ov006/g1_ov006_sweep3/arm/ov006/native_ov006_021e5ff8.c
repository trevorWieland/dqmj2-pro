/* ov006 row 0x021e5ff8: 76 bytes.
 *
 * What it does: 16 instructions; 4 call(s) to 0x021e3cd4, 0x02008d78, 0x021e6560, +1 more; loops (back edge at +0x04); returns through pop {r3, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x40 -> constant 0x02218d7c (image word 0x02218d7c)
 *   pool +0x44 -> native_data_0220d108 (image word 0x0220d108)
 *   pool +0x48 -> constant 0x02218d70 (image word 0x02218d70)
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e5ff8; the literal pool and
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

extern void native_fn_021e3cd4(void);
extern void native_fn_02008d78(void);
extern void native_fn_021e6560(void);
extern u8 native_data_0220d108[];
extern void native_fn_021e57d0(void);


asm u32 native_ov006_021e5ff8 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    bl native_fn_021e3cd4
    ldr r0, =0x02218d7c
    mov r1, #0
    mov r2, #16
    bl native_fn_02008d78
    mov r0, #14
    mov r1, #1
    bl native_fn_021e6560
    ldr r0, =native_data_0220d108
    mvn r1, #0
    str r1, [r0]
    bl native_fn_021e57d0
    ldr r1, =0x02218d70
    str r0, [r1]
    ldmia sp!, {r3, pc}
}
