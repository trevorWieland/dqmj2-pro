/* ov001 row 0x0221e518: 140 bytes.
 *
 * What it does: 35 instructions; 5 call(s) to 0x021db8d0, 0x0221e584, 0x0221e584, +2 more; loops (back edge at +0x20); returns through pop {r4, r5, r6, r7, r8, pc}
 *
 * Decoded shape: loop with 5 calls (35 instructions, 5 calls, 1 branch, 3 back edges, 0 literal slots).
 *
 *   branch +0x28 -> +0x6c
 *   branch +0x38 -> +0x6c
 *   branch +0x54 -> +0x6c
 *   back edge +0x68 -> +0x40
 *   back edge +0x80 -> +0x14
 *   test +0x24 cmp r0, #0
 *   test +0x34 cmp r0, #0
 *   test +0x4c cmp r0, #4
 *   test +0x64 cmp r1, r0
 *   test +0x6c cmp r6, #2
 *   test +0x7c cmp r6, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221e518; the literal pool and
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


asm u32 native_ov001_0221e518 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    mov r6, #0
    ldr r5, [r0, #0x4]
    mov r8, #3
    mov r4, r6
ov001_0221e518_L14:
    add r0, r6, r6, lsl #4
    add r7, r5, r0, lsl #6
    mov r0, r7
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_0221e518_L6c
    ldrb r0, [r7, #0x323]
    mov r1, r4
    cmp r0, #0
    ble ov001_0221e518_L6c
    mov r2, r7
ov001_0221e518_L40:
    ldrb r0, [r2, #0x35e]
    add r0, r0, #209
    and r0, r0, #255
    cmp r0, #4
    movls r6, r8
    bls ov001_0221e518_L6c
    ldrb r0, [r7, #0x323]
    add r1, r1, #1
    add r2, r2, #1
    cmp r1, r0
    blt ov001_0221e518_L40
ov001_0221e518_L6c:
    cmp r6, #2
    moveq r0, #1
    ldmeqia sp!, {r4, r5, r6, r7, r8, pc}
    add r6, r6, #1
    cmp r6, #3
    blt ov001_0221e518_L14
    mov r0, #0
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
