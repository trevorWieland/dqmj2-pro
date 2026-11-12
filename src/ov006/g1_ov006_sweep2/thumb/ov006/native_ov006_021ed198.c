/* ov006 row 0x021ed198: 48 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x10 -> +0x18
 *   branch +0x1c -> +0x24
 *   test +0x0e cmp r2, #0x0
 *   test +0x1a cmp r0, #0x70
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ed198; the literal pool and
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

extern void native_fn_021edcb8(void);
extern void native_fn_021edb9c(void);


asm u32 native_ov006_021ed198 (register u32 a0)
{
    push {r3, r4, r5, lr}
    add r4, r0, #0x6
    ldrh r0, [r4, #0x2]
    add r5, r1, #0x0
    bl native_fn_021edcb8
    add r2, r0, #0x0
    cmp r2, #0x0
    bgt ov006_021ed198_L18
    mov r0, #0x0
    mvn r0, r0
    pop {r3, r4, r5, pc}
ov006_021ed198_L18:
    ldrb r0, [r4, #0]
    cmp r0, #0x70
    beq ov006_021ed198_L24
    mov r0, #0x0
    mvn r0, r0
    pop {r3, r4, r5, pc}
ov006_021ed198_L24:
    add r0, r5, #0x0
    add r1, r4, #0x6
    bl native_fn_021edb9c
    mov r0, #0x0
    pop {r3, r4, r5, pc}
}
