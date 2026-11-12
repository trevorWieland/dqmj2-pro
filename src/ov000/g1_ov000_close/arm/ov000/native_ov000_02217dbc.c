/* ov000 row 0x02217dbc: 144 bytes.
 *
 * What it does: 36 instructions; 6 call(s) to 0x02049ad0, 0x022174a8, 0x0221572c, +3 more; loops (back edge at +0x10); returns through pop {r3, r4, r5, r6, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x20 -> +0x74
 *   branch +0x34 -> +0x74
 *   branch +0x44 -> +0x54
 *   branch +0x50 -> +0x74
 *   back edge +0x84 -> +0x0c
 *   test +0x1c cmp r0, #0
 *   test +0x30 cmp r6, #127
 *   test +0x3c cmp r6, #3
 *   test +0x4c cmp r0, #0
 *   test +0x80 cmp r5, #32
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02217dbc; the literal pool and
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
extern void native_fn_022174a8(void);
extern void native_fn_0221572c(void);
extern void native_fn_02217418(void);
extern void native_fn_0206006c(void);


asm u32 native_ov000_02217dbc (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, lr}
    sub sp, sp, #4
    mov r5, #0
ov000_02217dbc_Lc:
    mov r0, r5
    bl native_fn_02049ad0
    mov r4, r0
    ldr r0, [r4]
    cmp r0, #0
    beq ov000_02217dbc_L74
    ldrsb r0, [r4, #5]
    bl native_fn_022174a8
    mov r6, r0
    cmp r6, #127
    beq ov000_02217dbc_L74
    ldr r0, [r4]
    cmp r6, #3
    ldr r4, [r0, #0x4]
    bne ov000_02217dbc_L54
    bl native_fn_0221572c
    cmp r0, #0
    beq ov000_02217dbc_L74
ov000_02217dbc_L54:
    mov r0, r6
    bl native_fn_02217418
    ldrsb r1, [r4, #31]
    str r1, [sp]
    ldrsb r1, [r4, #28]
    ldrsb r2, [r4, #29]
    ldrsb r3, [r4, #30]
    bl native_fn_0206006c
ov000_02217dbc_L74:
    add r0, r5, #1
    mov r0, r0, lsl #24
    mov r5, r0, asr #24
    cmp r5, #32
    blt ov000_02217dbc_Lc
    add sp, sp, #4
    ldmia sp!, {r3, r4, r5, r6, pc}
}
