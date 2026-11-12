/* ov000 row 0x02221154: 136 bytes.
 *
 * What it does: 32 instructions; 3 call(s) to 0x02221198, 0x0221f8bc, 0x02221134; loops (back edge at +0x60); returns through pop {r4, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x80 -> constant 0x022463b0 (image word 0x022463b0)
 *   pool +0x84 -> constant 0x022463dc (image word 0x022463dc)
 *   branch +0x38 -> +0x64
 *   back edge +0x60 -> +0x44
 *   test +0x0c cmp r2, #0
 *   test +0x24 cmp r0, #0
 *   test +0x2c cmpne r0, #0
 *   test +0x50 cmp r0, #0
 *   test +0x5c cmp r3, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02221154; the literal pool and
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

extern void native_fn_0221f8bc(void);
extern void native_fn_02221134(void);


asm u32 native_ov000_02221154 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r4, r0
    ldr r0, =0x022463b0
    cmp r2, #0
    ldr r2, [r0, #0x1c]
    movne r1, #6
    ldrsh r0, [r2, #24]
    moveq r1, #5
    and r1, r1, #255
    cmp r0, #0
    ldrnesh r0, [r2, #156]
    cmpne r0, #0
    subeq r0, r1, #3
    andeq r1, r0, #255
    beq ov000_02221154_L64
    ldr r2, =0x022463dc
    mov r3, #0
ov000_02221154_L44:
    mov r0, r3, lsl #1
    ldrsh r0, [r2, r0]
    add r3, r3, #1
    cmp r0, #0
    subeq r0, r1, #1
    andeq r1, r0, #255
    cmp r3, #3
    blt ov000_02221154_L44
ov000_02221154_L64:
    ldr r2, =0x022463b0
    mov r0, r4
    ldr r2, [r2, #0xc]
    bl native_fn_0221f8bc
    mov r0, r4
    bl native_fn_02221134
    ldmia sp!, {r4, pc}
}
