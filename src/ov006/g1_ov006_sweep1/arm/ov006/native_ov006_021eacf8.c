/* ov006 row 0x021eacf8: 184 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xb0 -> native_data2_02219290 (image word 0x02219290)
 *   pool +0xb4 -> constant 0x0221930c (image word 0x0221930c)
 *   branch +0x24 -> +0x84
 *   branch +0x34 -> +0x78
 *   branch +0x80 -> +0x94
 *   test +0x1c cmp r0, #0
 *   test +0x30 cmp r0, #0
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021eacf8; the literal pool and
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

extern u8 native_data2_02219290[];
extern void native_fn_02008ca4(void);
extern void native_fn_0207b460(void);
extern void native_fn_0207c2b8(void);
extern void native_fn_0207c3d8(void);
extern void native_fn_0206dcd0(void);
extern void native_fn_02008c58(void);


asm u32 native_ov006_021eacf8 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    sub sp, sp, #64
    ldr r1, =native_data2_02219290
    ldr r3, =0x0221930c
    ldr r1, [r1, #0x24]
    mov r2, #132
    mla r4, r1, r2, r3
    cmp r0, #0
    mov r1, r4
    beq ov006_021eacf8_L84
    bl native_fn_02008ca4
    ldr r0, [r4, #0x14]
    cmp r0, #0
    beq ov006_021eacf8_L78
    ldrsh r0, [r4, #24]
    ldrb r1, [r4, #0x1a]
    add r3, sp, #0
    add r2, r4, #122
    bl native_fn_0207b460
    add r1, sp, #0
    add r0, r4, #32
    bl native_fn_0207c2b8
    strh r0, [r4, #36]
    add r1, sp, #0
    add r0, r4, #32
    bl native_fn_0207c3d8
    strh r0, [r4, #38]
    mov r0, #0
    strb r0, [r4, #0x33]
    strb r0, [r4, #0x31]
ov006_021eacf8_L78:
    mov r0, r4
    bl native_fn_0206dcd0
    b ov006_021eacf8_L94
ov006_021eacf8_L84:
    mov r0, #0
    bl native_fn_02008c58
    mov r0, #0
    bl native_fn_0206dcd0
ov006_021eacf8_L94:
    ldr r0, =native_data2_02219290
    ldr r1, [r0, #0x24]
    add r1, r1, #1
    and r1, r1, #15
    str r1, [r0, #0x24]
    add sp, sp, #64
    ldmia sp!, {r4, pc}
}
