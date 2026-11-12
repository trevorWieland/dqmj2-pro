/* ov000 row 0x0221f5fc: 236 bytes.
 *
 * What it does: 58 instructions; 8 call(s) to 0x02049ad0, 0x02049ffc, 0x02008be0, +5 more; loops (back edge at +0x14); returns through pop {r4, r5, r6, r7, r8, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0xe8 -> constant 0x020dbc18 (image word 0x020dbc18)
 *   branch +0x48 -> +0x70
 *   test +0x3c cmp r8, #0
 *   1 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221f5fc; the literal pool and
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
extern void native_fn_02049ffc(void);
extern void native_fn_02008be0(void);
extern void native_fn_02049f4c(void);
extern void native_fn_02085270(void);
extern void native_fn_02087a48(void);
extern void native_fn_02086b14(void);


asm u32 native_ov000_0221f5fc (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    sub sp, sp, #16
    mov r7, r1
    mov r8, r2
    mov r6, r3
    bl native_fn_02049ad0
    mov r4, r0
    ldr r0, [r4]
    ldr r5, [r0, #0x4]
    mov r0, r5
    bl native_fn_02049ffc
    add r1, sp, #8
    mov r0, #0
    mov r2, #8
    bl native_fn_02008be0
    cmp r8, #0
    moveq r0, #12288
    streqh r0, [sp, #8]
    beq ov000_0221f5fc_L70
    add r0, r8, #13
    mov r0, r0, lsl #16
    mov r0, r0, lsr #16
    add r0, r0, #123
    add r1, r0, #256
    ldr r0, =0x020dbc18
    mov r1, r1, lsl #1
    ldrh r0, [r0, r1]
    strh r0, [sp, #8]
ov000_0221f5fc_L70:
    mov r0, r4
    bl native_fn_02049f4c
    mov r1, #0
    mov r2, r1
    add r0, r5, #60
    bl native_fn_02085270
    ldrb r4, [sp, #0x28]
    mov r0, #1
    str r0, [sp]
    add r1, sp, #8
    str r1, [sp, #0x4]
    mov r0, r5
    mov r2, r6
    mov r1, #0
    mov r3, r4
    bl native_fn_02087a48
    add r0, r6, #8
    mov r3, r4
    ldrsb r4, [sp, #44]
    mov r0, r0, lsl #16
    mov r2, r0, asr #16
    mov r0, r5
    mov r1, #0
    stmia sp, {r4, r7}
    bl native_fn_02087a48
    mov r0, r5
    mov r1, #0
    bl native_fn_02086b14
    add sp, sp, #16
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
