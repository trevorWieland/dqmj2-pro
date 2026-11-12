/* ov000 row 0x02228d58: 252 bytes.
 *
 * What it does: 63 instructions; 6 call(s) to 0x02044d84, 0x02228e04, 0x02044d84, +3 more; loops (back edge at +0x20); returns through pop {r4, r5, r6, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x1c -> +0xf4
 *   branch +0x28 -> +0x64
 *   branch +0x3c -> +0xac
 *   branch +0x50 -> +0xac
 *   branch +0x70 -> +0xac
 *   branch +0x84 -> +0xac
 *   branch +0x98 -> +0xac
 *   branch +0xb8 -> +0xf4
 *   branch +0xcc -> +0xf4
 *   branch +0xe0 -> +0xf4
 *   test +0x18 cmp r0, r1
 *   test +0x24 cmp r0, #1
 *   test +0x30 cmp r0, #50
 *   test +0x38 cmplo r0, #50
 *   test +0x44 cmp r0, #0
 *   test +0x4c cmpeq r0, #0
 *   test +0x6c cmp r0, #0
 *   test +0x78 cmp r0, #50
 *   test +0x80 cmplo r0, #50
 *   test +0x8c cmp r0, #1
 *   test +0x94 cmpeq r0, #1
 *   test +0xb4 cmp r0, #0
 *   test +0xc0 cmp r0, #20
 *   test +0xc8 cmplo r0, #20
 *   test +0xd4 cmp r0, #0
 *   test +0xdc cmpeq r0, #0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02228d58; the literal pool and
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

extern void native_fn_02044d84(void);


asm u32 native_ov000_02228d58 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r6, r0
    mov r5, r1
    ldrsh r0, [r6, #24]
    ldrsh r1, [r5, #24]
    mov r4, r2
    cmp r0, r1
    bne ov000_02228d58_Lf4
    bl native_fn_02044d84
    cmp r0, #1
    bne ov000_02228d58_L64
    ldrb r0, [r6, #0x30]
    cmp r0, #50
    ldrlob r0, [r5, #0x30]
    cmplo r0, #50
    blo ov000_02228d58_Lac
    ldrb r0, [r6, #0x1a]
    cmp r0, #0
    ldreqb r0, [r5, #0x1a]
    cmpeq r0, #0
    bne ov000_02228d58_Lac
    mov r0, #1
    str r0, [r4]
    ldrsh r0, [r6, #24]
    ldmia sp!, {r4, r5, r6, pc}
ov000_02228d58_L64:
    ldrsh r0, [r6, #24]
    bl native_fn_02044d84
    cmp r0, #0
    bne ov000_02228d58_Lac
    ldrb r0, [r6, #0x30]
    cmp r0, #50
    ldrlob r0, [r5, #0x30]
    cmplo r0, #50
    blo ov000_02228d58_Lac
    ldrb r0, [r6, #0x1a]
    cmp r0, #1
    ldreqb r0, [r5, #0x1a]
    cmpeq r0, #1
    bne ov000_02228d58_Lac
    mov r0, #2
    str r0, [r4]
    ldrsh r0, [r6, #24]
    ldmia sp!, {r4, r5, r6, pc}
ov000_02228d58_Lac:
    ldrsh r0, [r6, #24]
    bl native_fn_02044d84
    cmp r0, #0
    bne ov000_02228d58_Lf4
    ldrb r0, [r6, #0x30]
    cmp r0, #20
    ldrlob r0, [r5, #0x30]
    cmplo r0, #20
    blo ov000_02228d58_Lf4
    ldrb r0, [r6, #0x1a]
    cmp r0, #0
    ldreqb r0, [r5, #0x1a]
    cmpeq r0, #0
    bne ov000_02228d58_Lf4
    mov r0, #1
    str r0, [r4]
    ldrsh r0, [r6, #24]
    ldmia sp!, {r4, r5, r6, pc}
ov000_02228d58_Lf4:
    mvn r0, #0
    ldmia sp!, {r4, r5, r6, pc}
}
