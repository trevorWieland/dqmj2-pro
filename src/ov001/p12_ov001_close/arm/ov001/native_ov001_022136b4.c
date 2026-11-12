/* ov001 row 0x022136b4: 72 bytes.
 *
 * What it does: 18 instructions; 4 call(s) to 0x021f1a44, 0x021f1aa8, 0x0205f998, +1 more; loops (back edge at +0x10); returns through pop {r4, r5, r6, pc}
 *
 * Decoded shape: loop with 4 calls (18 instructions, 4 calls, 1 branch, 4 back edges, 0 literal slots).
 *
 *   branch +0x20 -> +0x30
 *   back edge +0x40 -> +0x0c
 *   test +0x1c cmp r1, r6
 *   test +0x3c cmp r5, #32
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022136b4; the literal pool and
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

extern void native_fn_021f1a44(void);
extern void native_fn_021f1aa8(void);
extern void native_fn_0205f998(void);


asm u32 native_ov001_022136b4 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r6, r0
    mov r5, #0
ov001_022136b4_Lc:
    mov r0, r5
    bl native_fn_021f1a44
    mov r4, r0
    ldr r1, [r4]
    cmp r1, r6
    bne ov001_022136b4_L30
    bl native_fn_021f1aa8
    mov r0, r4
    bl native_fn_0205f998
ov001_022136b4_L30:
    add r0, r5, #1
    mov r0, r0, lsl #24
    mov r5, r0, asr #24
    cmp r5, #32
    blt ov001_022136b4_Lc
    ldmia sp!, {r4, r5, r6, pc}
}
