/* ov006 row 0x021ef1b8: 88 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x54 -> constant 0x0221aad0 (image word 0x0221aad0)
 *   branch +0x0a -> +0x3e
 *   branch +0x1e -> +0x3a
 *   branch +0x22 -> +0x32
 *   branch +0x26 -> +0x32
 *   branch +0x2a -> +0x30
 *   branch +0x2e -> +0x32
 *   back edge +0x38 -> +0x20
 *   back edge +0x3c -> +0x12
 *   branch +0x44 -> +0x50
 *   test +0x08 cmp r0, #0x0
 *   test +0x1c cmp r0, #0x0
 *   test +0x20 cmp r0, #0x4
 *   test +0x24 cmp r0, #0x5
 *   test +0x28 cmp r0, #0x14
 *   test +0x36 cmp r0, #0x0
 *   test +0x3a cmp r5, #0x0
 *   test +0x42 cmp r0, #0x0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ef1b8; the literal pool and
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

extern void native_fn_021eee7c(void);
extern void native_fn_02006b7c(void);
extern void native_fn_021ef0a0(void);


asm u32 native_ov006_021ef1b8 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    mov r5, #0x1
    bl native_fn_021eee7c
    cmp r0, #0x0
    beq ov006_021ef1b8_L3e
    mov r6, #0x0
    add r4, r6, #0x0
    mov r7, #0xa
ov006_021ef1b8_L12:
    add r0, r7, #0x0
    blx native_fn_02006b7c
    bl native_fn_021ef0a0
    cmp r0, #0x0
    beq ov006_021ef1b8_L3a
ov006_021ef1b8_L20:
    cmp r0, #0x4
    beq ov006_021ef1b8_L32
    cmp r0, #0x5
    beq ov006_021ef1b8_L32
    cmp r0, #0x14
    bne ov006_021ef1b8_L30
    add r5, r4, #0x0
    b ov006_021ef1b8_L32
ov006_021ef1b8_L30:
    add r5, r6, #0x0
ov006_021ef1b8_L32:
    bl native_fn_021ef0a0
    cmp r0, #0x0
    bne ov006_021ef1b8_L20
ov006_021ef1b8_L3a:
    cmp r5, #0x0
    bne ov006_021ef1b8_L12
ov006_021ef1b8_L3e:
    ldr r1, =0x0221aad0
    ldr r0, [r1, #0x54]
    cmp r0, #0x0
    beq ov006_021ef1b8_L50
    ldr r1, [r1, #0xc]
    blx r1
    ldr r0, =0x0221aad0
    mov r1, #0x0
    str r1, [r0, #0x54]
ov006_021ef1b8_L50:
    mov r0, #0x1
    pop {r3, r4, r5, r6, r7, pc}
}
