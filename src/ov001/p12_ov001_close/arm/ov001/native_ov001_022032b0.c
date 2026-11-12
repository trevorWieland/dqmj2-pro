/* ov001 row 0x022032b0: 88 bytes.
 *
 * What it does: 21 instructions; 3 call(s) to 0x021db508, 0x021db508, 0x022032c4; loops (back edge at +0x1c); returns through pop {r3, r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 3 calls (21 instructions, 3 calls, 0 branches, 3 back edges, 1 literal slot).
 *
 *   pool +0x54 -> constant 0x02239d04 (image word 0x02239d04)
 *   back edge +0x4c -> +0x14
 *   test +0x48 cmp r7, #3
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022032b0; the literal pool and
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

extern void native_fn_021db508(void);


asm u32 native_ov001_022032b0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    mov r7, #0
    ldr r5, =0x02239d04
    mov r6, r7
    mov r4, #2
ov001_022032b0_L14:
    mov r0, r6
    mov r1, r7
    bl native_fn_021db508
    add r1, r5, r7, lsl #2
    str r0, [r1, #0x1c]
    mov r0, r4
    mov r1, r7
    bl native_fn_021db508
    add r1, r7, #1
    add r2, r5, r7, lsl #2
    mov r1, r1, lsl #24
    mov r7, r1, asr #24
    str r0, [r2, #0x28]
    cmp r7, #3
    blt ov001_022032b0_L14
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
