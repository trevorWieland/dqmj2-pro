/* ov001 row 0x0221873c: 160 bytes.
 *
 * What it does: 40 instructions; 3 call(s) to 0x021db8d0, 0x022187d4, 0x02218754; loops (back edge at +0x1c); returns through pop {r4, r5, r6, r7, r8, pc}
 *
 * Decoded shape: loop with 3 calls (40 instructions, 3 calls, 8 branches, 2 back edges, 0 literal slots).
 *
 *   branch +0x24 -> +0x78
 *   branch +0x2c -> +0x44
 *   branch +0x3c -> +0x98
 *   branch +0x40 -> +0x78
 *   branch +0x48 -> +0x60
 *   branch +0x58 -> +0x98
 *   branch +0x5c -> +0x78
 *   branch +0x64 -> +0x78
 *   branch +0x74 -> +0x98
 *   back edge +0x94 -> +0x18
 *   test +0x20 cmp r0, #0
 *   test +0x28 cmp r6, #0
 *   test +0x38 cmp r0, r7
 *   test +0x44 cmp r6, #1
 *   test +0x54 cmp r7, r0
 *   test +0x60 cmp r6, #2
 *   test +0x70 cmp r0, r7
 *   test +0x78 cmp r4, #2
 *   test +0x88 cmp r4, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221873c; the literal pool and
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


asm u32 native_ov001_0221873c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    mov r8, r0
    mov r7, r2
    mov r6, r3
    add r5, r8, r1
    mov r4, #0
ov001_0221873c_L18:
    mov r0, r8
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_0221873c_L78
    cmp r6, #0
    bne ov001_0221873c_L44
    add r0, r5, #512
    ldrsb r0, [r0, #44]
    cmp r0, r7
    blt ov001_0221873c_L98
    b ov001_0221873c_L78
ov001_0221873c_L44:
    cmp r6, #1
    bne ov001_0221873c_L60
    add r0, r5, #512
    ldrsb r0, [r0, #44]
    cmp r7, r0
    bne ov001_0221873c_L98
    b ov001_0221873c_L78
ov001_0221873c_L60:
    cmp r6, #2
    bne ov001_0221873c_L78
    add r0, r5, #512
    ldrsb r0, [r0, #44]
    cmp r0, r7
    bgt ov001_0221873c_L98
ov001_0221873c_L78:
    cmp r4, #2
    moveq r0, #1
    ldmeqia sp!, {r4, r5, r6, r7, r8, pc}
    add r4, r4, #1
    cmp r4, #3
    add r8, r8, #1088
    add r5, r5, #1088
    blt ov001_0221873c_L18
ov001_0221873c_L98:
    mov r0, #0
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
