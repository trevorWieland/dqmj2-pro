/* ov000 row 0x021d99ac: 328 bytes.
 *
 * What it does: 79 instructions; 4 call(s) to 0x021d97e0, 0x021d9864, 0x021d98f0, +1 more; loops (back edge at +0x20); returns through pop {r4, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x13c -> constant 0x02231bd4 (image word 0x02231bd4)
 *   pool +0x140 -> constant 0x04000060 (image word 0x04000060)
 *   pool +0x144 -> constant 0x0223142c (image word 0x0223142c)
 *   branch +0x18 -> +0x6c
 *   branch +0x70 -> +0xb4
 *   branch +0xb8 -> +0xfc
 *   test +0x10 cmp r0, #0
 *   test +0x6c cmp r4, #0
 *   test +0x7c cmp r2, #0
 *   test +0x90 cmp r2, #0
 *   test +0xa4 cmp r2, #0
 *   test +0xb4 cmp r4, #1
 *   test +0xc4 cmp r2, #0
 *   test +0xd8 cmp r2, #0
 *   test +0xec cmp r2, #0
 *   test +0x104 cmp r2, #0
 *   test +0x118 cmp r2, #0
 *   test +0x12c cmp r2, #0
 *   0 block transfer(s), 10 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021d99ac; the literal pool and
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

extern void native_fn_021d97e0(void);
extern void native_fn_021d9864(void);
extern void native_fn_021d98f0(void);
extern void native_fn_021d9960(void);


asm u32 native_ov000_021d99ac (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldr r1, =0x02231bd4
    mov r4, r0
    ldr r0, [r1, r4, lsl #2]
    cmp r0, #0
    moveq r0, #0
    beq ov000_021d99ac_L6c
    add r0, r0, #4
    bl native_fn_021d97e0
    ldr r0, =0x02231bd4
    ldr r0, [r0, r4, lsl #2]
    add r0, r0, #68
    bl native_fn_021d9864
    ldr r0, =0x02231bd4
    ldr r0, [r0, r4, lsl #2]
    add r0, r0, #116
    bl native_fn_021d98f0
    ldr r0, =0x02231bd4
    ldr r0, [r0, r4, lsl #2]
    add r0, r0, #136
    bl native_fn_021d9960
    ldr r2, =0x04000060
    mov r0, #1
    ldrh r1, [r2]
    bic r1, r1, #12288
    orr r1, r1, #8
    strh r1, [r2]
ov000_021d99ac_L6c:
    cmp r4, #0
    bne ov000_021d99ac_Lb4
    ldr r1, =0x0223142c
    ldr r2, [r1, #0x7b4]
    cmp r2, #0
    movne r1, #31
    strneb r1, [r2, #0x172]
    ldr r1, =0x0223142c
    ldr r2, [r1, #0x7b8]
    cmp r2, #0
    movne r1, #0
    strneb r1, [r2, #0x172]
    ldr r1, =0x0223142c
    ldr r2, [r1, #0x7bc]
    cmp r2, #0
    movne r1, #0
    strneb r1, [r2, #0x172]
    ldmia sp!, {r4, pc}
ov000_021d99ac_Lb4:
    cmp r4, #1
    bne ov000_021d99ac_Lfc
    ldr r1, =0x0223142c
    ldr r2, [r1, #0x7b4]
    cmp r2, #0
    movne r1, #0
    strneb r1, [r2, #0x172]
    ldr r1, =0x0223142c
    ldr r2, [r1, #0x7b8]
    cmp r2, #0
    movne r1, #31
    strneb r1, [r2, #0x172]
    ldr r1, =0x0223142c
    ldr r2, [r1, #0x7bc]
    cmp r2, #0
    movne r1, #0
    strneb r1, [r2, #0x172]
    ldmia sp!, {r4, pc}
ov000_021d99ac_Lfc:
    ldr r1, =0x0223142c
    ldr r2, [r1, #0x7b4]
    cmp r2, #0
    movne r1, #0
    strneb r1, [r2, #0x172]
    ldr r1, =0x0223142c
    ldr r2, [r1, #0x7b8]
    cmp r2, #0
    movne r1, #0
    strneb r1, [r2, #0x172]
    ldr r1, =0x0223142c
    ldr r2, [r1, #0x7bc]
    cmp r2, #0
    movne r1, #31
    strneb r1, [r2, #0x172]
    ldmia sp!, {r4, pc}
}
