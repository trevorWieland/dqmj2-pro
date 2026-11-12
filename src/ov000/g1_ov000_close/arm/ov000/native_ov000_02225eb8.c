/* ov000 row 0x02225eb8: 496 bytes.
 *
 * What it does: 119 instructions; 11 call(s) to 0x02225edc, 0x02226024, 0x02227bf8, +8 more; loops (back edge at +0x4c); returns through pop {r4, r5, r6, r7, r8, pc}; 5 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x1dc -> constant 0x02246aa8 (image word 0x02246aa8)
 *   pool +0x1e0 -> constant 0x02246c84 (image word 0x02246c84)
 *   pool +0x1e4 -> constant 0x022468b8 (image word 0x022468b8)
 *   pool +0x1e8 -> constant 0x02246e18 (image word 0x02246e18)
 *   pool +0x1ec -> constant 0x02246c3c (image word 0x02246c3c)
 *   back edge +0x4c -> +0x24
 *   branch +0x64 -> +0x16c
 *   branch +0x78 -> +0x16c
 *   branch +0x88 -> +0x9c
 *   branch +0x98 -> +0x16c
 *   branch +0xa8 -> +0xbc
 *   branch +0xb8 -> +0x16c
 *   branch +0xd8 -> +0x16c
 *   branch +0xf4 -> +0x16c
 *   branch +0x104 -> +0x168
 *   branch +0x114 -> +0x168
 *   branch +0x170 -> +0x194
 *   branch +0x190 -> +0x1d4
 *   test +0x30 cmp r0, #0
 *   test +0x40 cmp r0, #0
 *   test +0x48 cmp r1, #3
 *   test +0x58 cmp r1, #0
 *   test +0x68 cmp r7, #0
 *   test +0x6c cmpeq r8, #0
 *   test +0x84 cmp r0, #0
 *   test +0xa4 cmp r0, #0
 *   test +0xcc cmp r1, #100
 *   test +0xe8 cmp r1, #100
 *   test +0x100 cmp r0, #1
 *   test +0x110 cmp r0, #0
 *   test +0x16c cmp r6, #0
 *   0 block transfer(s), 17 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02225eb8; the literal pool and
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

extern void native_fn_02227bf8(void);
extern void native_fn_02223c54(void);
extern void native_fn_02227c60(void);
extern void native_fn_02008d78(void);
extern void native_fn_02224b84(void);


asm u32 native_ov000_02225eb8 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    ldr r4, =0x02246aa8
    mov r6, #0
    ldr r5, =0x02246c84
    mov r7, r6
    mov r8, r6
    mov r1, r6
    mov r2, r5
    mov r3, r4
ov000_02225eb8_L24:
    ldrsh r0, [r2, #24]
    add r1, r1, #1
    add r2, r2, #132
    cmp r0, #0
    ldrsh r0, [r3, #24]
    addne r8, r8, #1
    add r3, r3, #132
    cmp r0, #0
    addne r7, r7, #1
    cmp r1, #3
    blt ov000_02225eb8_L24
    ldr r0, =0x022468b8
    ldr r1, [r0, #0x10]
    cmp r1, #0
    movle r1, #6
    strleb r1, [r0, #0x1f]
    ble ov000_02225eb8_L16c
    cmp r7, #0
    cmpeq r8, #0
    moveq r1, #3
    streqb r1, [r0, #0x1f]
    beq ov000_02225eb8_L16c
    mov r0, #0
    bl native_fn_02227bf8
    cmp r0, #0
    beq ov000_02225eb8_L9c
    ldr r0, =0x022468b8
    mov r1, #4
    strb r1, [r0, #0x1f]
    b ov000_02225eb8_L16c
ov000_02225eb8_L9c:
    mov r0, #1
    bl native_fn_02227bf8
    cmp r0, #0
    beq ov000_02225eb8_Lbc
    ldr r0, =0x022468b8
    mov r1, #5
    strb r1, [r0, #0x1f]
    b ov000_02225eb8_L16c
ov000_02225eb8_Lbc:
    ldr r0, =0x022468b8
    ldrsb r1, [r0, #29]
    add r1, r1, r7
    sub r1, r1, r8
    cmp r1, #100
    movgt r1, #1
    strgtb r1, [r0, #0x1f]
    bgt ov000_02225eb8_L16c
    ldrsb r1, [r0, #30]
    add r1, r1, r8
    sub r1, r1, r7
    cmp r1, #100
    movgt r1, #2
    strgtb r1, [r0, #0x1f]
    bgt ov000_02225eb8_L16c
    bl native_fn_02223c54
    ldrsb r0, [r0, #89]
    cmp r0, #1
    bne ov000_02225eb8_L168
    mov r0, #1
    bl native_fn_02227c60
    cmp r0, #0
    beq ov000_02225eb8_L168
    ldr r1, =0x022468b8
    mov r0, #10
    strb r0, [r1, #0x1a]
    mov r0, #5
    str r0, [r1, #0x14]
    mov r2, #7
    strb r2, [r1, #0x1f]
    mov r3, #127
    ldr r0, =0x02246e18
    mov r1, #0
    mov r2, #68
    strb r3, [r5, #0x18c]
    strb r3, [r4, #0x18c]
    bl native_fn_02008d78
    ldr r0, =0x02246c3c
    mov r1, #0
    mov r2, #68
    bl native_fn_02008d78
    mov r0, #0
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
ov000_02225eb8_L168:
    mov r6, #1
ov000_02225eb8_L16c:
    cmp r6, #0
    beq ov000_02225eb8_L194
    ldr r1, =0x022468b8
    mov r2, #0
    mov r0, #1
    strb r2, [r1, #0x1f]
    bl native_fn_02224b84
    ldr r1, =0x022468b8
    str r0, [r1, #0x14]
    b ov000_02225eb8_L1d4
ov000_02225eb8_L194:
    ldr r3, =0x022468b8
    mov r1, #9
    mov r6, #127
    ldr r0, =0x02246e18
    strb r1, [r3, #0x1a]
    mov r7, #5
    mov r1, #0
    mov r2, #68
    str r7, [r3, #0x14]
    strb r6, [r5, #0x18c]
    strb r6, [r4, #0x18c]
    bl native_fn_02008d78
    ldr r0, =0x02246c3c
    mov r1, #0
    mov r2, #68
    bl native_fn_02008d78
ov000_02225eb8_L1d4:
    mov r0, #0
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
