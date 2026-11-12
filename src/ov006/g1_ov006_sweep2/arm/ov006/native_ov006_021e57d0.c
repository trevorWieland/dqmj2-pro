/* ov006 row 0x021e57d0: 48 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   back edge +0x24 -> +0x0c
 *   test +0x14 cmp r0, #0
 *   test +0x20 cmp r4, #64
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e57d0; the literal pool and
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

extern void native_fn_020bb144(void);


asm u32 native_ov006_021e57d0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, #0
    mov r4, r5
ov006_021e57d0_Lc:
    mov r0, r4
    bl native_fn_020bb144
    cmp r0, #0
    add r4, r4, #1
    addne r5, r5, #1
    cmp r4, #64
    blt ov006_021e57d0_Lc
    mov r0, r5
    ldmia sp!, {r3, r4, r5, pc}
}
