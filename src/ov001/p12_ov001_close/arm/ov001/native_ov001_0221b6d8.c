/* ov001 row 0x0221b6d8: 112 bytes.
 *
 * What it does: 28 instructions; 2 call(s) to 0x021db8d0, 0x0221b6e4; loops (back edge at +0x10); returns through pop {r3, r4, r5, pc}
 *
 * Decoded shape: loop with 2 calls (28 instructions, 2 calls, 2 branches, 2 back edges, 0 literal slots).
 *
 *   branch +0x18 -> +0x4c
 *   branch +0x48 -> +0x68
 *   back edge +0x64 -> +0x0c
 *   test +0x14 cmp r0, #0
 *   test +0x24 cmp r1, #0
 *   test +0x2c cmpeq r1, #0
 *   test +0x34 cmpeq r1, #0
 *   test +0x3c cmpeq r1, #0
 *   test +0x44 cmpeq r0, #0
 *   test +0x4c cmp r4, #2
 *   test +0x5c cmp r4, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221b6d8; the literal pool and
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

extern void native_fn_021db8d0(void);


asm u32 native_ov001_0221b6d8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r5, [r0, #0x8]
    mov r4, #0
ov001_0221b6d8_Lc:
    mov r0, r5
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_0221b6d8_L4c
    add r0, r5, #512
    ldrsb r1, [r0, #56]
    cmp r1, #0
    ldreqsb r1, [r0, #57]
    cmpeq r1, #0
    ldreqsb r1, [r0, #58]
    cmpeq r1, #0
    ldreqsb r1, [r0, #59]
    cmpeq r1, #0
    ldreqsb r0, [r0, #78]
    cmpeq r0, #0
    beq ov001_0221b6d8_L68
ov001_0221b6d8_L4c:
    cmp r4, #2
    moveq r0, #1
    ldmeqia sp!, {r3, r4, r5, pc}
    add r4, r4, #1
    cmp r4, #3
    add r5, r5, #1088
    blt ov001_0221b6d8_Lc
ov001_0221b6d8_L68:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, pc}
}
