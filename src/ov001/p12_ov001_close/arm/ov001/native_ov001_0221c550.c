/* ov001 row 0x0221c550: 196 bytes.
 *
 * What it does: 49 instructions; 7 call(s) to 0x021db8d0, 0x0221c5f4, 0x0207afec, +4 more; loops (back edge at +0x18); returns through pop {r4, r5, r6, r7, r8, pc}
 *
 * Decoded shape: loop with 7 calls (49 instructions, 7 calls, 5 branches, 6 back edges, 0 literal slots).
 *
 *   branch +0x20 -> +0xa4
 *   branch +0x30 -> +0x78
 *   branch +0x3c -> +0xa4
 *   branch +0x5c -> +0xa4
 *   back edge +0x70 -> +0x48
 *   branch +0x74 -> +0xa4
 *   branch +0x94 -> +0xa4
 *   back edge +0xa0 -> +0x78
 *   back edge +0xb8 -> +0x0c
 *   test +0x1c cmp r0, #0
 *   test +0x2c cmp r0, #1
 *   test +0x38 cmp r0, #0
 *   test +0x54 cmp r0, #0
 *   test +0x6c cmp r6, r0
 *   test +0x8c cmp r0, #0
 *   test +0x9c cmp r6, #6
 *   test +0xa4 cmp r5, #2
 *   test +0xb4 cmp r5, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221c550; the literal pool and
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
extern void native_fn_0207afec(void);


asm u32 native_ov001_0221c550 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    ldr r4, [r0, #0x8]
    mov r5, #0
ov001_0221c550_Lc:
    add r0, r5, r5, lsl #4
    add r7, r4, r0, lsl #6
    mov r0, r7
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_0221c550_La4
    ldrb r0, [r7, #0x322]
    mov r6, #0
    cmp r0, #1
    beq ov001_0221c550_L78
    ldrb r0, [r7, #0x323]
    cmp r0, #0
    ble ov001_0221c550_La4
    add r0, r5, r5, lsl #4
    add r8, r4, r0, lsl #6
ov001_0221c550_L48:
    ldrb r0, [r7, #0x35e]
    bl native_fn_0207afec
    ldrsh r0, [r0, #24]
    cmp r0, #0
    movne r5, #3
    bne ov001_0221c550_La4
    ldrb r0, [r8, #0x323]
    add r6, r6, #1
    add r7, r7, #1
    cmp r6, r0
    blt ov001_0221c550_L48
    b ov001_0221c550_La4
ov001_0221c550_L78:
    ldr r0, [r7, #0x1e8]
    add r0, r0, r6
    ldrb r0, [r0, #0x8]
    bl native_fn_0207afec
    ldrsh r0, [r0, #24]
    cmp r0, #0
    movne r5, #3
    bne ov001_0221c550_La4
    add r6, r6, #1
    cmp r6, #6
    blt ov001_0221c550_L78
ov001_0221c550_La4:
    cmp r5, #2
    moveq r0, #1
    ldmeqia sp!, {r4, r5, r6, r7, r8, pc}
    add r5, r5, #1
    cmp r5, #3
    blt ov001_0221c550_Lc
    mov r0, #0
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
