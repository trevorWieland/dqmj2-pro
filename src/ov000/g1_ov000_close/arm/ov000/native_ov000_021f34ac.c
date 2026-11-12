/* ov000 row 0x021f34ac: 152 bytes.
 *
 * What it does: 37 instructions; 3 call(s) to 0x0202a498, 0x0202a498, 0x0202a498; loops (back edge at +0x20); returns through pop {r3, r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x94 -> constant 0x02236ec0 (image word 0x02236ec0)
 *   branch +0x1c -> +0x34
 *   branch +0x44 -> +0x60
 *   branch +0x70 -> +0x8c
 *   test +0x14 cmp r1, #0
 *   test +0x3c cmp r1, #0
 *   test +0x68 cmp r1, #0
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f34ac; the literal pool and
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

extern void native_fn_0202a498(void);


asm u32 native_ov000_021f34ac (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r1, =0x02236ec0
    mov r4, #1
    ldr r1, [r1]
    mov r5, r0
    cmp r1, #0
    moveq r4, #0
    beq ov000_021f34ac_L34
    bl native_fn_0202a498
    ldr r0, =0x02236ec0
    mov r1, #0
    str r1, [r0]
    str r1, [r0, #0x14]
ov000_021f34ac_L34:
    ldr r0, =0x02236ec0
    ldr r1, [r0, #0x8]
    cmp r1, #0
    moveq r4, #0
    beq ov000_021f34ac_L60
    mov r0, r5
    bl native_fn_0202a498
    ldr r0, =0x02236ec0
    mov r1, #0
    str r1, [r0, #0x8]
    str r1, [r0, #0x4]
ov000_021f34ac_L60:
    ldr r0, =0x02236ec0
    ldr r1, [r0, #0x10]
    cmp r1, #0
    moveq r4, #0
    beq ov000_021f34ac_L8c
    mov r0, r5
    bl native_fn_0202a498
    ldr r0, =0x02236ec0
    mov r1, #0
    str r1, [r0, #0x10]
    str r1, [r0, #0xc]
ov000_021f34ac_L8c:
    mov r0, r4
    ldmia sp!, {r3, r4, r5, pc}
}
