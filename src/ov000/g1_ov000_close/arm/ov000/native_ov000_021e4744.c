/* ov000 row 0x021e4744: 136 bytes.
 *
 * What it does: 34 instructions; 3 call(s) to 0x0205be24, 0x021e46ec, 0x021e46ec; loops (back edge at +0x1c); returns through pop {r4, r5, r6, r7, r8, pc}
 *
 * Decoded shape: predicated block copy.
 *
 *   branch +0x18 -> +0x80
 *   branch +0x28 -> +0x38
 *   branch +0x34 -> +0x44
 *   branch +0x4c -> +0x80
 *   test +0x20 cmp r7, #0
 *   test +0x48 cmp r3, #0
 *   test +0x50 cmp r6, #0
 *   test +0x5c cmp r5, #0
 *   test +0x74 cmp r1, #0
 *   4 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e4744; the literal pool and
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

extern void native_fn_0205be24(void);
extern void native_fn_021e46ec(void);


asm u32 native_ov000_021e4744 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    movs r8, r0
    mov r7, r1
    mov r6, r2
    mov r5, r3
    mov r4, #0
    bmi ov000_021e4744_L80
    bl native_fn_0205be24
    cmp r7, #0
    mov r1, r8
    bne ov000_021e4744_L38
    mov r2, r4
    bl native_fn_021e46ec
    b ov000_021e4744_L44
ov000_021e4744_L38:
    mov r0, r4
    mov r2, #1
    bl native_fn_021e46ec
ov000_021e4744_L44:
    mov r3, r0
    cmp r3, #0
    beq ov000_021e4744_L80
    cmp r6, #0
    ldmneia r3, {r0, r1, r2}
    stmneia r6, {r0, r1, r2}
    cmp r5, #0
    addne r0, r3, #12
    ldmneia r0, {r0, r1, r2}
    stmneia r5, {r0, r1, r2}
    ldr r1, [sp, #0x18]
    mov r4, r3
    cmp r1, #0
    ldrne r0, [r3, #0x18]
    strne r0, [r1]
ov000_021e4744_L80:
    mov r0, r4
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
