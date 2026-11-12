/* ov006 row 0x02204dfc: 76 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   back edge +0x44 -> +0x20
 *   test +0x18 cmp r6, #0
 *   test +0x3c cmp r6, r0, asr #24
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02204dfc; the literal pool and
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

extern void native_fn_021e5fec(void);
extern void native_fn_02081c9c(void);
extern void native_fn_02081c88(void);


asm u32 native_ov006_02204dfc (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    bl native_fn_021e5fec
    mov r4, r0
    bl native_fn_02081c9c
    mov r6, r0
    mov r5, #0
    cmp r6, #0
    ldmleia sp!, {r4, r5, r6, pc}
ov006_02204dfc_L20:
    mov r0, r5
    bl native_fn_02081c88
    ldrb r1, [r0]
    add r0, r5, #1
    mov r0, r0, lsl #24
    add r1, r1, #47
    strb r1, [r4, r5]
    cmp r6, r0, asr #24
    mov r5, r0, asr #24
    bgt ov006_02204dfc_L20
    ldmia sp!, {r4, r5, r6, pc}
}
