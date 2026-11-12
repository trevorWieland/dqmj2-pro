/* ov006 row 0x02203114: 52 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x14 -> +0x2a
 *   test +0x12 cmp r0, r2
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02203114; the literal pool and
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

extern void native_fn_02005d50(void);
extern void native_fn_020024bc(void);
extern void native_fn_02005d20(void);


asm u32 native_ov006_02203114 (register u32 a0)
{
    push {r4, r5, r6, lr}
    add r5, r0, #0x0
    mov r0, #0x1
    mov r4, #0x0
    blx native_fn_02005d50
    add r6, r0, #0x0
    ldrb r2, [r5, #0x3]
    ldrb r0, [r5, #0x2]
    cmp r0, r2
    beq ov006_02203114_L2a
    ldrh r1, [r5, #0]
    add r0, r2, r1
    sub r0, r0, #0x1
    blx native_fn_020024bc
    strb r0, [r5, #0x3]
    ldrb r0, [r5, #0x3]
    lsl r0, r0, #0x2
    add r0, r5, r0
    ldr r4, [r0, #0x4]
ov006_02203114_L2a:
    add r0, r6, #0x0
    blx native_fn_02005d20
    add r0, r4, #0x0
    pop {r4, r5, r6, pc}
}
