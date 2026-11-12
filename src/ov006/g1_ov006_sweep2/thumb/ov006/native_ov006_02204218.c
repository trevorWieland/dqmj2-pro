/* ov006 row 0x02204218: 32 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x18 -> constant 0x027e0000 (image word 0x027e0000)
 *   pool +0x1c -> constant 0x00003ff8 (image word 0x00003ff8)
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02204218; the literal pool and
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

extern void native_fn_022048a8(void);


asm u32 native_ov006_02204218 (register u32 a0)
{
    push {r3, lr}
    mov r0, #0x1
    bl native_fn_022048a8
    ldr r3, =0x027e0000
    ldr r1, =0x00003ff8
    mov r0, #0x1
    ldr r2, [r3, r1]
    orr r0, r2
    str r0, [r3, r1]
    pop {r3, pc}
    mov r8, r8
}
