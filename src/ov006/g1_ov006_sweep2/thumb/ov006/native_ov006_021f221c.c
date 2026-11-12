/* ov006 row 0x021f221c: 40 bytes.
 *
 * What it does: Writes 2 blocks of 1 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x20 -> native_data_0221c004 (image word 0x0221c004)
 *   pool +0x24 -> native_data2_0221c004 (image word 0x0221c004)
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f221c; the literal pool and
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

extern u8 native_data_0221c004[];
extern void native_fn_0220498c(void);
extern void native_fn_022043a4(void);
extern u8 native_data2_0221c004[];
extern void native_fn_02203c20(void);


asm u32 native_ov006_021f221c (register u32 a0)
{
    push {r3, lr}
    ldr r1, =native_data_0221c004
    mov r0, #0x1
    ldr r1, [r1, #0]
    ldr r1, [r1, #0]
    bl native_fn_0220498c
    ldr r0, =native_data_0221c004
    ldr r0, [r0, #0]
    ldr r0, [r0, #0x4]
    bl native_fn_022043a4
    ldr r0, =native_data2_0221c004
    bl native_fn_02203c20
    pop {r3, pc}
}
