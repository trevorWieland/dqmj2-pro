/* ov000 row 0x021f19e4: 120 bytes.
 *
 * What it does: 30 instructions; 3 call(s) to 0x020635d4, 0x020635d4, 0x021f18cc; loops (back edge at +0x20); returns through pop {r4, r5, r6, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x44 -> +0x54
 *   branch +0x58 -> +0x68
 *   test +0x40 cmp r6, #0
 *   test +0x48 cmp r0, #0
 *   test +0x54 cmp r6, #0
 *   test +0x5c cmp r0, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f19e4; the literal pool and
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

extern void native_fn_020635d4(void);
extern void native_fn_021f18cc(void);


asm u32 native_ov000_021f19e4 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r5, r0
    ldr r2, [r5]
    mov r4, r1
    mov r0, r2, lsl #16
    mov r1, r2, lsr #16
    mov r0, r0, asr #16
    and r1, r1, #255
    bl native_fn_020635d4
    ldr r1, [r4]
    mov r6, r0
    mov r0, r1, lsl #16
    mov r1, r1, lsr #16
    mov r0, r0, asr #16
    and r1, r1, #255
    bl native_fn_020635d4
    cmp r6, #0
    bne ov000_021f19e4_L54
    cmp r0, #0
    movne r0, #1
    ldmneia sp!, {r4, r5, r6, pc}
ov000_021f19e4_L54:
    cmp r6, #0
    beq ov000_021f19e4_L68
    cmp r0, #0
    mvneq r0, #0
    ldmeqia sp!, {r4, r5, r6, pc}
ov000_021f19e4_L68:
    mov r0, r5
    mov r1, r4
    bl native_fn_021f18cc
    ldmia sp!, {r4, r5, r6, pc}
}
