/* ov001 row 0x021e9d20: 80 bytes.
 *
 * What it does: 19 instructions; 2 call(s) to 0x021eedbc, 0x021e9d30; loops (back edge at +0x40); returns through pop {r3, r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 2 calls (19 instructions, 2 calls, 1 branch, 1 back edge, 1 literal slot).
 *
 *   pool +0x4c -> constant 0x02238dec (image word 0x02238dec)
 *   branch +0x18 -> +0x38
 *   back edge +0x40 -> +0x10
 *   test +0x14 cmp lr, r12
 *   test +0x3c cmp r5, #10
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021e9d20; the literal pool and
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

extern void native_fn_021eedbc(void);


asm u32 native_ov001_021e9d20 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r4, =0x02238dec
    mov r5, #0
    mvn r12, #0
ov001_021e9d20_L10:
    ldr lr, [r4, r5, lsl #2]
    cmp lr, r12
    bne ov001_021e9d20_L38
    ldr r12, [sp, #0x10]
    str r12, [sp]
    bl native_fn_021eedbc
    ldr r1, =0x02238dec
    str r0, [r1, r5, lsl #2]
    mov r0, #1
    ldmia sp!, {r3, r4, r5, pc}
ov001_021e9d20_L38:
    add r5, r5, #1
    cmp r5, #10
    blt ov001_021e9d20_L10
    mov r0, #0
    ldmia sp!, {r3, r4, r5, pc}
}
