/* ov001 row 0x022185b0: 148 bytes.
 *
 * What it does: 37 instructions; 5 call(s) to 0x0221863c, 0x0207afec, 0x022185d8, +2 more; loops (back edge at +0x30); returns through pop {r4, r5, r6, pc}
 *
 * Decoded shape: loop with 5 calls (37 instructions, 5 calls, 2 branches, 4 back edges, 0 literal slots).
 *
 *   branch +0x18 -> +0x5c
 *   branch +0x24 -> +0x8c
 *   back edge +0x54 -> +0x28
 *   branch +0x58 -> +0x8c
 *   back edge +0x88 -> +0x5c
 *   test +0x14 cmp r0, #1
 *   test +0x20 cmp r0, #0
 *   test +0x3c cmp r5, r0, lsr #28
 *   test +0x50 cmp r4, r0
 *   test +0x74 cmp r5, r0, lsr #28
 *   test +0x84 cmp r4, #6
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022185b0; the literal pool and
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

extern void native_fn_0207afec(void);


asm u32 native_ov001_022185b0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r6, r0
    ldrb r0, [r6, #0x322]
    mov r5, r1
    mov r4, #0
    cmp r0, #1
    beq ov001_022185b0_L5c
    ldrb r0, [r6, #0x323]
    cmp r0, #0
    ble ov001_022185b0_L8c
ov001_022185b0_L28:
    add r0, r6, r4
    ldrb r0, [r0, #0x35e]
    bl native_fn_0207afec
    ldrh r0, [r0, #8]
    mov r0, r0, lsl #20
    cmp r5, r0, lsr #28
    moveq r0, #1
    ldmeqia sp!, {r4, r5, r6, pc}
    ldrb r0, [r6, #0x323]
    add r4, r4, #1
    cmp r4, r0
    blt ov001_022185b0_L28
    b ov001_022185b0_L8c
ov001_022185b0_L5c:
    ldr r0, [r6, #0x1e8]
    add r0, r0, r4
    ldrb r0, [r0, #0x8]
    bl native_fn_0207afec
    ldrh r0, [r0, #8]
    mov r0, r0, lsl #20
    cmp r5, r0, lsr #28
    moveq r0, #1
    ldmeqia sp!, {r4, r5, r6, pc}
    add r4, r4, #1
    cmp r4, #6
    blt ov001_022185b0_L5c
ov001_022185b0_L8c:
    mov r0, #0
    ldmia sp!, {r4, r5, r6, pc}
}
