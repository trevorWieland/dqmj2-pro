/* ov006 row 0x022031a0: 136 bytes.
 *
 * What it does: Writes one block of 1 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x74 -> native_data_0220bb48 (image word 0x0220bb48)
 *   pool +0x78 -> constant 0x0221c180 (image word 0x0221c180)
 *   pool +0x7c -> constant 0x04001050 (image word 0x04001050)
 *   pool +0x80 -> constant 0x04000050 (image word 0x04000050)
 *   pool +0x84 -> native_fn_02203228+1 (image word 0x02203229)
 *   branch +0x22 -> +0x2a
 *   branch +0x28 -> +0x30
 *   branch +0x34 -> +0x3c
 *   branch +0x40 -> +0x4c
 *   branch +0x4a -> +0x54
 *   test +0x16 cmp r0, #0x1
 *   test +0x32 cmp r2, #0x0
 *   test +0x3c cmp r0, #0x1
 *   0 block transfer(s), 9 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x022031a0; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity proves the instruction stream, not the meaning of the fields, blocks and callee contracts it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_0220bb48[];
extern void native_fn_020042e0(void);
extern void native_fn_02203228(void);
extern void native_fn_0220490c(void);


asm u32 native_ov006_022031a0 (register u32 a0)
{
    push {r3, r4, r5, r6, lr}
    sub sp, #0x4
    add r6, r3, #0x0
    ldr r3, =native_data_0220bb48
    add r5, r0, #0x0
    ldrb r4, [r3, #0x8]
    add r0, r1, #0x0
    add r1, r2, #0x0
    add r2, sp, #0x0
    strb r4, [r2, #0]
    ldrb r4, [r3, #0x9]
    cmp r0, #0x1
    strb r4, [r2, #0x1]
    ldrb r4, [r3, #0xa]
    ldrb r3, [r3, #0xb]
    strb r4, [r2, #0x2]
    strb r3, [r2, #0x3]
    bne ov006_022031a0_L2a
    ldr r2, =0x0221c180
    ldr r4, [r2, #0]
    b ov006_022031a0_L30
ov006_022031a0_L2a:
    ldr r2, =0x0221c180
    ldr r4, [r2, #0]
    add r4, #0xc
ov006_022031a0_L30:
    ldrb r2, [r4, #0x9]
    cmp r2, #0x0
    beq ov006_022031a0_L3c
    add sp, #0x4
    mov r0, #0x0
    pop {r3, r4, r5, r6, pc}
ov006_022031a0_L3c:
    cmp r0, #0x1
    add r2, sp, #0x0
    bne ov006_022031a0_L4c
    ldrsb r2, [r2, r5]
    ldr r0, =0x04001050
    blx native_fn_020042e0
    b ov006_022031a0_L54
ov006_022031a0_L4c:
    ldrsb r2, [r2, r5]
    ldr r0, =0x04000050
    blx native_fn_020042e0
ov006_022031a0_L54:
    ldr r1, =native_fn_02203228+1
    mov r0, #0x1
    add r2, r4, #0x0
    mov r3, #0xc8
    bl native_fn_0220490c
    str r0, [r4, #0]
    mov r0, #0x0
    strh r0, [r4, #0x4]
    strb r5, [r4, #0x8]
    strh r6, [r4, #0x6]
    mov r0, #0x1
    strb r0, [r4, #0x9]
    add sp, #0x4
    pop {r3, r4, r5, r6, pc}
    mov r8, r8
}
