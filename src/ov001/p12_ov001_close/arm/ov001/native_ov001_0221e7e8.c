/* ov001 row 0x0221e7e8: 148 bytes.
 *
 * What it does: 37 instructions; 5 call(s) to 0x021dbec8, 0x021db8d0, 0x02210ba8, +2 more; loops (back edge at +0x0c); returns through pop {r3, r4, r5, r6, r7, pc}
 *
 * Decoded shape: loop with 5 calls (37 instructions, 5 calls, 6 branches, 5 back edges, 0 literal slots).
 *
 *   branch +0x28 -> +0x54
 *   branch +0x38 -> +0x8c
 *   branch +0x50 -> +0x8c
 *   branch +0x58 -> +0x7c
 *   branch +0x60 -> +0x74
 *   branch +0x70 -> +0x7c
 *   back edge +0x88 -> +0x1c
 *   test +0x24 cmp r0, #0
 *   test +0x34 cmp r0, #0
 *   test +0x44 cmp r1, #0
 *   test +0x4c cmpeq r0, #0
 *   test +0x54 cmp r5, #2
 *   test +0x5c cmp r6, #0
 *   test +0x6c cmp r0, #9
 *   test +0x80 cmp r5, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221e7e8; the literal pool and
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

extern void native_fn_021dbec8(void);
extern void native_fn_021db8d0(void);
extern void native_fn_02210ba8(void);
extern void native_fn_0203d294(void);


asm u32 native_ov001_0221e7e8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    ldr r7, [r0, #0x8]
    ldr r0, [r0]
    bl native_fn_021dbec8
    mov r6, r0
    mov r5, #0
    mov r4, #10
ov001_0221e7e8_L1c:
    mov r0, r7
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_0221e7e8_L54
    mov r0, r7
    bl native_fn_02210ba8
    cmp r0, #0
    beq ov001_0221e7e8_L8c
    add r0, r7, #512
    ldrsb r1, [r0, #66]
    cmp r1, #0
    ldreqsb r0, [r0, #67]
    cmpeq r0, #0
    bne ov001_0221e7e8_L8c
ov001_0221e7e8_L54:
    cmp r5, #2
    bne ov001_0221e7e8_L7c
    cmp r6, #0
    bne ov001_0221e7e8_L74
    mov r0, r4
    bl native_fn_0203d294
    cmp r0, #9
    bge ov001_0221e7e8_L7c
ov001_0221e7e8_L74:
    mov r0, #1
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov001_0221e7e8_L7c:
    add r5, r5, #1
    cmp r5, #3
    add r7, r7, #1088
    blt ov001_0221e7e8_L1c
ov001_0221e7e8_L8c:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
