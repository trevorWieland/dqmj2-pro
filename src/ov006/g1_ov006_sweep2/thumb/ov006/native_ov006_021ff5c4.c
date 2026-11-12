/* ov006 row 0x021ff5c4: 80 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x2e -> +0x3a
 *   back edge +0x38 -> +0x2a
 *   back edge +0x4a -> +0x1a
 *   test +0x2c cmp r0, #0x0
 *   test +0x36 cmp r1, #0x3
 *   test +0x48 cmp r6, #0x4
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ff5c4; the literal pool and
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

extern void native_fn_02008d78(void);
extern void native_fn_02008e0c(void);
extern void native_fn_0201f274(void);


asm u32 native_ov006_021ff5c4 (register u32 a0)
{
    push {r4, r5, r6, r7, lr}
    sub sp, #0xc
    str r0, [sp]
    str r1, [sp, #0x4]
    add r0, sp, #0x8
    mov r1, #0x0
    mov r2, #0x4
    blx native_fn_02008d78
    mov r6, #0x0
    add r5, r6, #0x0
    mov r4, #0x20
    add r7, sp, #0x8
ov006_021ff5c4_L1a:
    ldr r0, [sp]
    add r1, r7, #0x0
    add r0, r0, r5
    mov r2, #0x3
    blx native_fn_02008e0c
    mov r1, #0x0
    add r2, r7, #0x0
ov006_021ff5c4_L2a:
    ldrb r0, [r2, #0]
    cmp r0, #0x0
    bne ov006_021ff5c4_L3a
    add r1, r1, #0x1
    strb r4, [r2, #0]
    add r2, r2, #0x1
    cmp r1, #0x3
    blt ov006_021ff5c4_L2a
ov006_021ff5c4_L3a:
    add r0, r7, #0x0
    blx native_fn_0201f274
    ldr r1, [sp, #0x4]
    add r5, r5, #0x3
    strb r0, [r1, r6]
    add r6, r6, #0x1
    cmp r6, #0x4
    blt ov006_021ff5c4_L1a
    add sp, #0xc
    pop {r4, r5, r6, r7, pc}
}
