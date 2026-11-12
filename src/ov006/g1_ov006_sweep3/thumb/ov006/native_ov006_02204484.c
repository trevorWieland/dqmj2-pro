/* ov006 row 0x02204484: 272 bytes.
 *
 * What it does: 127 instructions; 8 call(s) to 0x02203114, 0x02005d50, 0x0220428c, +5 more; loops (back edge at +0x1e); returns through pop {r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x10c -> constant 0x0221c1b0 (image word 0x0221c1b0)
 *   branch +0x3a -> +0x9a
 *   branch +0x56 -> +0x84
 *   branch +0x6e -> +0x7e
 *   branch +0x7c -> +0x84
 *   back edge +0x82 -> +0x60
 *   branch +0x92 -> +0xf6
 *   branch +0x98 -> +0xf6
 *   branch +0xb4 -> +0xe2
 *   branch +0xcc -> +0xdc
 *   branch +0xda -> +0xe2
 *   back edge +0xe0 -> +0xbe
 *   branch +0xf0 -> +0xf6
 *   test +0x38 cmp r6, #0x0
 *   test +0x54 cmp r4, r1
 *   test +0x6c cmp r2, r1
 *   test +0x80 cmp r6, r0
 *   test +0x90 cmp r4, r0
 *   test +0xb2 cmp r4, r1
 *   test +0xca cmp r3, r1
 *   test +0xde cmp r6, r0
 *   test +0xee cmp r4, r0
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02204484; the literal pool and
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

extern void native_fn_02203114(void);
extern void native_fn_02005d50(void);
extern void native_fn_0220428c(void);
extern void native_fn_02008430(void);
extern void native_fn_02005d20(void);


asm u32 native_ov006_02204484 (register u32 a0)
{
    push {r4, r5, r6, r7, lr}
    sub sp, #0xc
    add r5, r1, #0x0
    add r4, r0, #0x0
    ldr r1, =0x0221c1b0
    mov r0, #0x1a
    lsl r0, r0, #0x4
    add r7, r4, #0x0
    mul r7, r0
    ldr r1, [r1, #0]
    sub r0, r0, #0x4
    add r1, r1, r7
    ldr r0, [r1, r0]
    add r6, r2, #0x0
    str r3, [sp]
    bl native_fn_02203114
    str r0, [sp, #0x8]
    mov r0, #0x3
    add r1, r5, #0x3
    bic r1, r0
    ldr r0, [sp, #0x8]
    asr r5, r1, #0x2
    strh r5, [r0, #0xa]
    mov r0, #0x1
    blx native_fn_02005d50
    str r0, [sp, #0x4]
    cmp r6, #0x0
    beq ov006_02204484_L9a
    ldr r0, =0x0221c1b0
    mov r2, #0x1a
    ldr r0, [r0, #0]
    lsl r2, r2, #0x4
    add r1, r4, #0x0
    mul r1, r2
    add r3, r0, r1
    add r1, r2, #0x0
    sub r1, #0x20
    sub r2, #0x14
    add r4, r3, r1
    add r1, r3, r2
    cmp r4, r1
    beq ov006_02204484_L84
    add r1, r0, r7
    mov r0, #0x63
    lsl r0, r0, #0x2
    add r0, r1, r0
ov006_02204484_L60:
    ldrh r2, [r4, #0x8]
    ldrh r1, [r4, #0xa]
    ldr r6, [r4, #0x4]
    add r3, r2, r1
    ldrh r1, [r6, #0x8]
    add r2, r3, r5
    cmp r2, r1
    bgt ov006_02204484_L7e
    ldr r0, [sp, #0x8]
    ldr r1, [sp, #0x8]
    strh r3, [r0, #0x8]
    add r0, r6, #0x0
    bl native_fn_0220428c
    b ov006_02204484_L84
ov006_02204484_L7e:
    add r4, r6, #0x0
    cmp r6, r0
    bne ov006_02204484_L60
ov006_02204484_L84:
    ldr r0, =0x0221c1b0
    ldr r0, [r0, #0]
    add r1, r0, r7
    mov r0, #0x63
    lsl r0, r0, #0x2
    add r0, r1, r0
    cmp r4, r0
    bne ov006_02204484_Lf6
    blx native_fn_02008430
    b ov006_02204484_Lf6
ov006_02204484_L9a:
    ldr r0, =0x0221c1b0
    mov r2, #0x1a
    ldr r0, [r0, #0]
    lsl r2, r2, #0x4
    add r1, r4, #0x0
    mul r1, r2
    add r3, r0, r1
    add r1, r2, #0x0
    sub r1, #0x14
    sub r2, #0x20
    add r4, r3, r1
    add r1, r3, r2
    cmp r4, r1
    beq ov006_02204484_Le2
    add r1, r0, r7
    mov r0, #0x6
    lsl r0, r0, #0x6
    add r0, r1, r0
ov006_02204484_Lbe:
    ldrh r1, [r4, #0x8]
    ldr r6, [r4, #0]
    sub r3, r1, r5
    ldrh r2, [r6, #0x8]
    ldrh r1, [r6, #0xa]
    add r1, r2, r1
    cmp r3, r1
    blt ov006_02204484_Ldc
    ldr r0, [sp, #0x8]
    ldr r1, [sp, #0x8]
    strh r3, [r0, #0x8]
    add r0, r4, #0x0
    bl native_fn_0220428c
    b ov006_02204484_Le2
ov006_02204484_Ldc:
    add r4, r6, #0x0
    cmp r6, r0
    bne ov006_02204484_Lbe
ov006_02204484_Le2:
    ldr r0, =0x0221c1b0
    ldr r0, [r0, #0]
    add r1, r0, r7
    mov r0, #0x6
    lsl r0, r0, #0x6
    add r0, r1, r0
    cmp r4, r0
    bne ov006_02204484_Lf6
    blx native_fn_02008430
ov006_02204484_Lf6:
    ldr r0, [sp, #0x8]
    ldrh r1, [r0, #0x8]
    ldr r0, [sp]
    str r1, [r0, #0]
    ldr r0, [sp, #0x4]
    blx native_fn_02005d20
    ldr r0, [sp, #0x8]
    add sp, #0xc
    pop {r4, r5, r6, r7, pc}
    mov r8, r8
}
