/* ov000 row 0x02228968: 144 bytes.
 *
 * What it does: 36 instructions; 5 call(s) to 0x02229f98, 0x02229f98, 0x02229f98, +2 more; loops (back edge at +0x8c); returns through pop {r4, r5, r6, r7, r8, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x40 -> +0x84
 *   branch +0x54 -> +0x84
 *   branch +0x68 -> +0x74
 *   branch +0x70 -> +0x84
 *   back edge +0x8c -> +0x18
 *   test +0x24 cmp r0, r8
 *   test +0x3c cmp r7, r0
 *   test +0x50 cmp r6, r0
 *   test +0x64 cmp r0, #0
 *   test +0x6c cmp r5, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02228968; the literal pool and
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

extern void native_fn_02229f98(void);


asm u32 native_ov000_02228968 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    mov r7, r0
    mov r6, r1
    mov r5, r2
    mov r4, #0
    mvn r8, #0
ov000_02228968_L18:
    mov r0, r4
    bl native_fn_02229f98
    ldrsh r0, [r0, #2]
    cmp r0, r8
    mvneq r0, #0
    ldmeqia sp!, {r4, r5, r6, r7, r8, pc}
    mov r0, r4
    bl native_fn_02229f98
    ldrsh r0, [r0, #2]
    cmp r7, r0
    bne ov000_02228968_L84
    mov r0, r4
    bl native_fn_02229f98
    ldrb r0, [r0, #0x4]
    cmp r6, r0
    bne ov000_02228968_L84
    mov r0, r4
    bl native_fn_02229f98
    ldrb r0, [r0, #0x5]
    cmp r0, #0
    beq ov000_02228968_L74
    cmp r5, #0
    beq ov000_02228968_L84
ov000_02228968_L74:
    mov r0, r4
    bl native_fn_02229f98
    ldrsh r0, [r0]
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
ov000_02228968_L84:
    add r0, r4, #1
    and r4, r0, #255
    b ov000_02228968_L18
}
