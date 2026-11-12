/* ov000 row 0x022078e0: 116 bytes.
 *
 * What it does: 29 instructions; 7 call(s) to 0x02049ad0, 0x02207610, 0x020852c8, +4 more; loops (back edge at +0x1c); returns through pop {r3, r4, r5, r6, r7, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x28 -> +0x54
 *   branch +0x3c -> +0x4c
 *   branch +0x48 -> +0x54
 *   back edge +0x64 -> +0x10
 *   test +0x24 cmp r7, #0
 *   test +0x34 cmp r0, #0
 *   test +0x60 cmp r6, #6
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022078e0; the literal pool and
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

extern void native_fn_02049ad0(void);
extern void native_fn_02207610(void);
extern void native_fn_020852c8(void);
extern void native_fn_02206c6c(void);
extern void native_fn_02085200(void);


asm u32 native_ov000_022078e0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    mov r6, #0
    mov r4, #3
    mov r5, #1
ov000_022078e0_L10:
    add r0, r6, #1
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    ldr r7, [r0]
    cmp r7, #0
    beq ov000_022078e0_L54
    mov r0, r6
    bl native_fn_02207610
    cmp r0, #0
    ldr r0, [r7, #0x4]
    beq ov000_022078e0_L4c
    mov r1, r5
    bl native_fn_020852c8
    b ov000_022078e0_L54
ov000_022078e0_L4c:
    mov r1, r4
    bl native_fn_020852c8
ov000_022078e0_L54:
    add r0, r6, #1
    mov r0, r0, lsl #24
    mov r6, r0, asr #24
    cmp r6, #6
    blt ov000_022078e0_L10
    bl native_fn_02206c6c
    bl native_fn_02085200
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
