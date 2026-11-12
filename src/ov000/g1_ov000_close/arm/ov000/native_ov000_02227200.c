/* ov000 row 0x02227200: 108 bytes.
 *
 * What it does: 25 instructions; 6 call(s) to 0x02223c60, 0x02227200, 0x01ffab90, +3 more; loops (back edge at +0x04); returns through pop {r4, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x64 -> constant 0x022468b8 (image word 0x022468b8)
 *   pool +0x68 -> native_data_0222fe90 (image word 0x0222fe90)
 *   branch +0x24 -> +0x34
 *   back edge +0x28 -> +0x00
 *   branch +0x30 -> +0x5c
 *   branch +0x3c -> +0x5c
 *   branch +0x50 -> +0x58
 *   test +0x20 cmp r0, #2
 *   test +0x34 cmp r0, #3
 *   test +0x4c cmp r0, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02227200; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity fixes the instruction stream, not the field, block and callee semantics behind the addresses and strides it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void ov000_context_02246600_02223c60(void);
extern u8 native_data_0222fe90[];
extern void native_fn_01ffab90(void);
extern void native_fn_01ffb340(void);
extern void native_fn_0222728c(void);
extern void native_fn_01ffa4b4(void);


asm u32 native_ov000_02227200 (register u32 a0)
{
ov000_02227200_L0:
    stmdb sp!, {r4, lr}
    bl ov000_context_02246600_02223c60
    ldr r1, =0x022468b8
    ldr r2, =native_data_0222fe90
    ldr r1, [r1, #0x14]
    ldr r4, [r0]
    ldr r0, [r2, r1, lsl #2]
    blx r0
    cmp r0, #2
    bne ov000_02227200_L34
    bl ov000_02227200_L0
    mov r4, r0
    b ov000_02227200_L5c
ov000_02227200_L34:
    cmp r0, #3
    moveq r4, #0
    beq ov000_02227200_L5c
    bl native_fn_01ffab90
    bl native_fn_01ffb340
    ldrb r0, [r0, #0x11]
    cmp r0, #0
    beq ov000_02227200_L58
    bl native_fn_0222728c
ov000_02227200_L58:
    bl native_fn_01ffa4b4
ov000_02227200_L5c:
    mov r0, r4
    ldmia sp!, {r4, pc}
}
