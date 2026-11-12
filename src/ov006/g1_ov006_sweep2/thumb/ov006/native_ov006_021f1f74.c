/* ov006 row 0x021f1f74: 52 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x1e -> +0x24
 *   back edge +0x28 -> +0x0c
 *   test +0x1c cmp r5, #0x5
 *   test +0x26 cmp r5, #0x6
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f1f74; the literal pool and
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

extern void native_fn_021f1f40(void);


asm u32 native_ov006_021f1f74 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    str r0, [sp]
    add r6, r1, #0x0
    add r4, r0, #0x0
    mov r5, #0x0
    mov r7, #0x3a
ov006_021f1f74_Lc:
    mov r1, #0x0
    ldrsb r1, [r6, r1]
    add r0, r4, #0x0
    add r6, r6, #0x1
    bl native_fn_021f1f40
    add r0, r4, r0
    add r4, r0, #0x0
    cmp r5, #0x5
    bge ov006_021f1f74_L24
    add r4, r0, #0x1
    strb r7, [r0, #0]
ov006_021f1f74_L24:
    add r5, r5, #0x1
    cmp r5, #0x6
    blt ov006_021f1f74_Lc
    mov r0, #0x0
    strb r0, [r4, #0]
    ldr r0, [sp]
    sub r0, r4, r0
    pop {r3, r4, r5, r6, r7, pc}
}
