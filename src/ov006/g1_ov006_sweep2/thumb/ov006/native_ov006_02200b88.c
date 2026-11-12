/* ov006 row 0x02200b88: 132 bytes.
 *
 * What it does: Writes one block of 2 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x7c -> constant 0x0221c160 (image word 0x0221c160)
 *   pool +0x80 -> constant 0x0001b144 (image word 0x0001b144)
 *   branch +0x0c -> +0x12
 *   branch +0x10 -> +0x2c
 *   branch +0x22 -> +0x2a
 *   branch +0x34 -> +0x6c
 *   branch +0x48 -> +0x6c
 *   branch +0x56 -> +0x6c
 *   branch +0x68 -> +0x6c
 *   branch +0x70 -> +0x76
 *   test +0x0a cmp r0, #0x0
 *   test +0x20 cmp r0, #0x0
 *   test +0x32 cmp r0, #0x0
 *   test +0x46 cmp r1, #0x0
 *   test +0x54 cmp r0, #0x0
 *   test +0x66 cmp r0, #0x0
 *   test +0x6e cmp r4, r0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02200b88; the literal pool and
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

extern void native_fn_0200bd04(void);
extern void native_fn_0200bfe4(void);
extern void native_fn_02015700(void);
extern void native_fn_02015780(void);
extern void native_fn_02015c70(void);
extern void native_fn_0200c02c(void);


asm u32 native_ov006_02200b88 (register u32 a0)
{
    push {r4, r5, r6, lr}
    sub sp, #0x48
    add r6, r0, #0x0
    ldr r0, [r6, #0]
    mov r5, #0x0
    cmp r0, #0x0
    bne ov006_02200b88_L12
    add r4, r5, #0x0
    b ov006_02200b88_L2c
ov006_02200b88_L12:
    add r0, sp, #0x0
    blx native_fn_0200bd04
    ldr r1, [r6, #0]
    add r0, sp, #0x0
    blx native_fn_0200bfe4
    cmp r0, #0x0
    bne ov006_02200b88_L2a
    add sp, #0x48
    add r0, r5, #0x0
    pop {r4, r5, r6, pc}
ov006_02200b88_L2a:
    add r4, sp, #0x0
ov006_02200b88_L2c:
    add r0, r4, #0x0
    blx native_fn_02015700
    cmp r0, #0x0
    beq ov006_02200b88_L6c
    ldr r1, =0x0221c160
    ldr r0, =0x0001b144
    ldr r3, [r1, #0]
    add r2, r3, #0x0
    add r2, #0x2c
    str r2, [r3, r0]
    ldr r1, [r1, #0]
    ldr r1, [r1, r0]
    cmp r1, #0x0
    beq ov006_02200b88_L6c
    mov r2, #0x1
    add r0, r4, #0x0
    lsl r2, r2, #0x10
    blx native_fn_02015780
    cmp r0, #0x0
    beq ov006_02200b88_L6c
    ldr r1, =0x0221c160
    add r0, r6, #0x0
    ldr r2, [r1, #0]
    ldr r1, =0x0001b144
    ldr r1, [r2, r1]
    blx native_fn_02015c70
    cmp r0, #0x0
    beq ov006_02200b88_L6c
    mov r5, #0x1
ov006_02200b88_L6c:
    add r0, sp, #0x0
    cmp r4, r0
    bne ov006_02200b88_L76
    blx native_fn_0200c02c
ov006_02200b88_L76:
    add r0, r5, #0x0
    add sp, #0x48
    pop {r4, r5, r6, pc}
}
