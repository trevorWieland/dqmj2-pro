/* ov000 row 0x02220680: 148 bytes.
 *
 * What it does: 36 instructions; 3 call(s) to 0x02062b00, 0x02072f48, 0x022206a4; loops (back edge at +0x08); returns through pop {r4, r5, r6, r7, r8, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x90 -> constant 0x022463b0 (image word 0x022463b0)
 *   branch +0x2c -> +0x78
 *   branch +0x40 -> +0x78
 *   branch +0x4c -> +0x64
 *   branch +0x54 -> +0x78
 *   branch +0x60 -> +0x78
 *   back edge +0x84 -> +0x24
 *   test +0x28 cmp r2, #0
 *   test +0x3c cmp r0, r2
 *   test +0x48 cmp r7, r0
 *   test +0x50 cmp r0, #2
 *   test +0x5c cmp r0, #2
 *   test +0x6c cmp r0, #0
 *   test +0x7c cmp r4, #100
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02220680; the literal pool and
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

extern void native_fn_02062b00(void);
extern void native_fn_02072f48(void);


asm u32 native_ov000_02220680 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    mov r7, r0
    bl native_fn_02062b00
    rsb r2, r7, #1
    mov r1, #132
    mul r6, r2, r1
    ldr r8, =0x022463b0
    mov r5, r0
    mov r4, #0
ov000_02220680_L24:
    ldr r2, [r5, #0x14]
    cmp r2, #0
    beq ov000_02220680_L78
    ldr r0, [r8, #0x1c]
    add r1, r6, r0
    ldr r0, [r1, #0x14]
    cmp r0, r2
    beq ov000_02220680_L78
    ldrb r0, [r5, #0x1b]
    cmp r7, r0
    beq ov000_02220680_L64
    cmp r0, #2
    bne ov000_02220680_L78
    ldrb r0, [r1, #0x1b]
    cmp r0, #2
    beq ov000_02220680_L78
ov000_02220680_L64:
    ldrsh r0, [r5, #24]
    bl native_fn_02072f48
    cmp r0, #0
    moveq r0, #1
    ldmeqia sp!, {r4, r5, r6, r7, r8, pc}
ov000_02220680_L78:
    add r4, r4, #1
    cmp r4, #100
    add r5, r5, #132
    blt ov000_02220680_L24
    mov r0, #0
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
