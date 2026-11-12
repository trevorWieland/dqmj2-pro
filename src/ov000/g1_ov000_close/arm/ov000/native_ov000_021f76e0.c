/* ov000 row 0x021f76e0: 140 bytes.
 *
 * What it does: 35 instructions; 10 call(s) to 0x02062aa0, 0x021f79e0, 0x021f79e0, +7 more; loops (back edge at +0x04); returns through pop {r3, r4, r5, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x24 -> +0x30
 *   back edge +0x84 -> +0x3c
 *   test +0x20 cmp r0, #0
 *   test +0x34 cmp r4, #0
 *   test +0x80 cmp r5, r4
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f76e0; the literal pool and
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

extern void native_fn_02062aa0(void);
extern void native_fn_021f79e0(void);


asm u32 native_ov000_021f76e0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    bl native_fn_02062aa0
    mov r4, r0
    mov r0, #0
    bl native_fn_021f79e0
    mov r0, #13
    bl native_fn_021f79e0
    bl native_fn_02062aa0
    cmp r0, #0
    beq ov000_021f76e0_L30
    mov r0, #14
    bl native_fn_021f79e0
ov000_021f76e0_L30:
    mov r5, #0
    cmp r4, #0
    ldmleia sp!, {r3, r4, r5, pc}
ov000_021f76e0_L3c:
    add r0, r5, #1
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_021f79e0
    add r0, r5, #4
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_021f79e0
    add r0, r5, #7
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_021f79e0
    add r0, r5, #10
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_021f79e0
    add r5, r5, #1
    cmp r5, r4
    blt ov000_021f76e0_L3c
    ldmia sp!, {r3, r4, r5, pc}
}
