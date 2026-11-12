/* ov001 row 0x02204898: 100 bytes.
 *
 * What it does: 25 instructions; 2 call(s) to 0x02204250, 0x022048b8; loops (back edge at +0x28); returns through pop {r4, r5, r6, r7, r8, pc}
 *
 * Decoded shape: loop with 2 calls (25 instructions, 2 calls, 0 branches, 2 back edges, 0 literal slots).
 *
 *   back edge +0x5c -> +0x20
 *   test +0x04 cmp r2, #0
 *   test +0x2c cmp r0, #0
 *   test +0x3c cmp r1, #2
 *   test +0x44 cmpeq r1, r7
 *   test +0x4c cmpeq r1, r6
 *   test +0x58 cmp r4, #64
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02204898; the literal pool and
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

extern void native_fn_02204250(void);


asm u32 native_ov001_02204898 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    cmp r2, #0
    moveq r2, #19
    mov r4, #0
    mov r7, r0
    mov r6, r1
    sub r5, r2, #1
    mov r8, r4
ov001_02204898_L20:
    mov r0, r4, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02204250
    cmp r0, #0
    ldmeqia sp!, {r4, r5, r6, r7, r8, pc}
    ldr r1, [r0]
    add r4, r4, #1
    cmp r1, #2
    ldreq r1, [r0, #0x30]
    cmpeq r1, r7
    ldreq r1, [r0, #0x34]
    cmpeq r1, r6
    streqh r8, [r0, #38]
    streq r5, [r0, #0x2c]
    cmp r4, #64
    blt ov001_02204898_L20
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
