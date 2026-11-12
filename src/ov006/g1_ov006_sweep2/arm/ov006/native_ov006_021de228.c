/* ov006 row 0x021de228: 96 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   back edge +0x58 -> +0x34
 *   test +0x24 cmp r3, #0
 *   test +0x44 cmp r3, r1
 *   test +0x54 cmp r2, #9
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021de228; the literal pool and
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

extern void native_fn_02067b3c(void);
extern void native_fn_021de1a8(void);
extern void native_fn_021de1ec(void);


asm u32 native_ov006_021de228 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r4, r0
    bl native_fn_02067b3c
    mov r5, r0
    mov r0, r4
    bl native_fn_021de1a8
    mov r4, r0
    bl native_fn_021de1ec
    sub r3, r4, r0
    cmp r3, #0
    mov r0, #0
    ldmleia sp!, {r3, r4, r5, pc}
    mov r2, r0
ov006_021de228_L34:
    add r0, r5, r2, lsl #3
    ldr r0, [r0, #0x4]
    ldr r1, [r5, r2, lsl #3]
    mov r0, r0, lsl #16
    cmp r3, r1
    mov r0, r0, asr #16
    ldmloia sp!, {r3, r4, r5, pc}
    add r2, r2, #1
    cmp r2, #9
    blt ov006_021de228_L34
    ldmia sp!, {r3, r4, r5, pc}
}
