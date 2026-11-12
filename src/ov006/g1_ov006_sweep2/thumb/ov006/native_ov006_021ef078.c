/* ov006 row 0x021ef078: 40 bytes.
 *
 * What it does: Writes one block of 1 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x20 -> constant 0x0221aad0 (image word 0x0221aad0)
 *   pool +0x24 -> constant 0x0221ab54 (image word 0x0221ab54)
 *   back edge +0x18 -> +0x12
 *   test +0x16 cmp r2, #0x4
 *   1 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ef078; the literal pool and
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

extern void native_fn_02007ff4(void);
extern void native_fn_02008008(void);


asm u32 native_ov006_021ef078 (register u32 a0)
{
    push {r3, lr}
    blx native_fn_02007ff4
    ldr r1, =0x0221aad0
    mov r2, #0x0
    str r2, [r1, #0x68]
    str r2, [r1, #0x6c]
    ldr r3, =0x0221ab54
    add r1, r2, #0x0
ov006_021ef078_L12:
    add r2, r2, #0x1
    stmia r3!, {r1}
    cmp r2, #0x4
    blt ov006_021ef078_L12
    blx native_fn_02008008
    pop {r3, pc}
}
