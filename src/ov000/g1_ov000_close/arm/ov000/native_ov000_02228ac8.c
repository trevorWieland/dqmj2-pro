/* ov000 row 0x02228ac8: 172 bytes.
 *
 * What it does: 43 instructions; 7 call(s) to 0x0222a00c, 0x0222a00c, 0x0222a00c, +4 more; loops (back edge at +0xa8); returns through pop {r3, r4, r5, r6, r7, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x3c -> +0x64
 *   branch +0x50 -> +0x64
 *   branch +0x74 -> +0x9c
 *   branch +0x88 -> +0x9c
 *   back edge +0xa8 -> +0x14
 *   test +0x20 cmp r0, r7
 *   test +0x38 cmp r6, r0
 *   test +0x4c cmp r5, r0
 *   test +0x70 cmp r5, r0
 *   test +0x84 cmp r6, r0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02228ac8; the literal pool and
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

extern void native_fn_0222a00c(void);


asm u32 native_ov000_02228ac8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    mov r6, r0
    mov r5, r1
    mov r4, #0
    mvn r7, #0
ov000_02228ac8_L14:
    mov r0, r4
    bl native_fn_0222a00c
    ldrsh r0, [r0, #2]
    cmp r0, r7
    mvneq r0, #0
    ldmeqia sp!, {r3, r4, r5, r6, r7, pc}
    mov r0, r4
    bl native_fn_0222a00c
    ldrsh r0, [r0, #2]
    cmp r6, r0
    bne ov000_02228ac8_L64
    mov r0, r4
    bl native_fn_0222a00c
    ldrsh r0, [r0, #4]
    cmp r5, r0
    bne ov000_02228ac8_L64
    mov r0, r4
    bl native_fn_0222a00c
    ldrsh r0, [r0]
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov000_02228ac8_L64:
    mov r0, r4
    bl native_fn_0222a00c
    ldrsh r0, [r0, #2]
    cmp r5, r0
    bne ov000_02228ac8_L9c
    mov r0, r4
    bl native_fn_0222a00c
    ldrsh r0, [r0, #4]
    cmp r6, r0
    bne ov000_02228ac8_L9c
    mov r0, r4
    bl native_fn_0222a00c
    ldrsh r0, [r0]
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov000_02228ac8_L9c:
    add r0, r4, #1
    mov r0, r0, lsl #16
    mov r4, r0, lsr #16
    b ov000_02228ac8_L14
}
