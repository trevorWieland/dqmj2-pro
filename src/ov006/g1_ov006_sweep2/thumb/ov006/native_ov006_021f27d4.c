/* ov006 row 0x021f27d4: 40 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f27d4; the literal pool and
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

extern void native_fn_021f2798(void);
extern void native_fn_02202a80(void);
extern void native_fn_02007308(void);
extern void native_fn_02202b24(void);


asm u32 native_ov006_021f27d4 (register u32 a0)
{
    push {r3, r4, r5, lr}
    add r5, r1, #0x0
    bl native_fn_021f2798
    add r1, sp, #0x0
    mov r2, #0x4
    bl native_fn_02202a80
    ldr r1, [sp]
    add r4, r0, #0x0
    blx native_fn_02007308
    ldr r2, [sp]
    add r0, r4, #0x0
    mov r1, #0x0
    blx r5
    add r0, r4, #0x0
    bl native_fn_02202b24
    pop {r3, r4, r5, pc}
}
