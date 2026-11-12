/* ov006 row 0x021e7ca0: 84 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   test +0x18 cmp r0, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e7ca0; the literal pool and
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

extern void native_fn_02049ae4(void);
extern void native_fn_02049f30(void);
extern void native_fn_02049f24(void);
extern void native_fn_02049f14(void);
extern void native_fn_020853c8(void);


asm u32 native_ov006_021e7ca0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    mov r7, r0
    mov r6, r1
    bl native_fn_02049ae4
    mov r5, r0
    ldr r0, [r5, #0x4]
    cmp r0, #0
    moveq r0, #0
    ldmeqia sp!, {r3, r4, r5, r6, r7, pc}
    bl native_fn_02049f30
    bl native_fn_02049f24
    mov r4, r0
    mov r1, r7
    blx r6
    mov r0, r4
    bl native_fn_02049f14
    ldr r0, [r5, #0x4]
    mov r1, r4
    bl native_fn_020853c8
    mov r0, #1
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
