/* ov001 row 0x021f18d8: 128 bytes.
 *
 * What it does: 31 instructions; 2 call(s) to 0x021f19f0, 0x02049be4; loops (back edge at +0x58); returns through pop {r3, r4, r5, r6, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 2 calls (31 instructions, 2 calls, 0 branches, 1 back edge, 1 literal slot).
 *
 *   pool +0x7c -> constant 0x02238f58 (image word 0x02238f58)
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f18d8; the literal pool and
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

extern void native_fn_021f19f0(void);
extern void native_fn_02049be4(void);


asm u32 native_ov001_021f18d8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, lr}
    sub sp, sp, #28
    mov r6, r1
    mov r5, r2
    mov r4, r3
    bl native_fn_021f19f0
    str r6, [sp]
    str r5, [sp, #0x4]
    mov r1, #0
    ldrb r3, [sp, #0x30]
    str r4, [sp, #0x8]
    ldr r2, =0x02238f58
    str r3, [sp, #0xc]
    ldr r2, [r2, #0x28]
    ldrsb r3, [sp, #52]
    str r2, [sp, #0x10]
    mov r2, r1
    str r3, [sp, #0x14]
    mov r12, #1
    mov r3, #127
    mov r5, r0
    str r12, [sp, #0x18]
    bl native_fn_02049be4
    ldr r1, =0x02238f58
    ldrb r2, [sp, #0x30]
    ldr r3, [r1, #0x28]
    mov r0, r5
    mla r2, r4, r2, r3
    str r2, [r1, #0x28]
    add sp, sp, #28
    ldmia sp!, {r3, r4, r5, r6, pc}
}
