/* ov001 row 0x02219108: 112 bytes.
 *
 * What it does: 28 instructions; 2 call(s) to 0x021db8d0, 0x0221911c; loops (back edge at +0x18); returns through pop {r4, r5, r6, r7, r8, pc}
 *
 * Decoded shape: block load (28 instructions, 2 calls, 3 branches, 2 back edges, 0 literal slots).
 *
 *   branch +0x2c -> +0x44
 *   branch +0x40 -> +0x68
 *   branch +0x48 -> +0x58
 *   back edge +0x64 -> +0x14
 *   test +0x1c cmp r0, #0
 *   test +0x28 cmpne r1, r0
 *   test +0x3c cmp r0, #0
 *   test +0x44 cmp r5, #2
 *   test +0x4c cmp r6, #0
 *   test +0x5c cmp r5, #3
 *   1 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02219108; the literal pool and
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


asm u32 native_ov001_02219108 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    mov r6, #0
    ldmia r0, {r4, r7}
    mov r5, r6
    mov r8, #1
ov001_02219108_L14:
    mov r0, r7
    bl native_fn_021db8d0
    cmp r0, #0
    ldrneb r1, [r4, #0x31f]
    ldrneb r0, [r7, #0x31f]
    cmpne r1, r0
    beq ov001_02219108_L44
    add r0, r7, #512
    ldrsb r0, [r0, #53]
    mov r6, r8
    cmp r0, #0
    beq ov001_02219108_L68
ov001_02219108_L44:
    cmp r5, #2
    bne ov001_02219108_L58
    cmp r6, #0
    movne r0, #1
    ldmneia sp!, {r4, r5, r6, r7, r8, pc}
ov001_02219108_L58:
    add r5, r5, #1
    cmp r5, #3
    add r7, r7, #1088
    blt ov001_02219108_L14
ov001_02219108_L68:
    mov r0, #0
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
