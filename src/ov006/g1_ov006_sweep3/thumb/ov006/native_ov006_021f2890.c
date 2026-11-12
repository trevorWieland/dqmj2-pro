/* ov006 row 0x021f2890: 124 bytes.
 *
 * What it does: 46 instructions; 8 call(s) to 0x022034dc, 0x021f5418, 0x021f290c, +5 more; no back edge; returns through pop {r4, r5, r6, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x6c -> constant 0x0221c098 (image word 0x0221c098)
 *   pool +0x70 -> constant 0x00000209 (image word 0x00000209)
 *   pool +0x74 -> native_data_0220b11c (image word 0x0220b11c)
 *   pool +0x78 -> native_data_0220b11e (image word 0x0220b11e)
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f2890; the literal pool and
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

extern void native_fn_022034dc(void);
extern void native_fn_021f5418(void);
extern void native_fn_021f290c(void);
extern void native_fn_022037c0(void);
extern void native_fn_021f5328(void);
extern u8 native_data_0220b11c[];
extern u8 native_data_0220b11e[];
extern void native_fn_022036ac(void);
extern void native_fn_022038ac(void);


asm u32 native_ov006_021f2890 (register u32 a0)
{
    push {r4, r5, r6, lr}
    sub sp, #0x10
    add r6, r0, #0x0
    mov r0, #0x0
    add r5, r1, #0x0
    add r1, r0, #0x0
    bl native_fn_022034dc
    add r4, r0, #0x0
    ldr r0, =0x0221c098
    add r1, r5, #0x0
    ldr r0, [r0, #0]
    bl native_fn_021f5418
    add r5, r0, #0x0
    bl native_fn_021f290c
    mov r1, #0x5e
    str r1, [sp]
    mov r1, #0x2
    str r1, [sp, #0x4]
    str r0, [sp, #0x8]
    add r0, r4, #0x0
    mov r1, #0xd
    mov r2, #0x3c
    mov r3, #0xe6
    str r5, [sp, #0xc]
    bl native_fn_022037c0
    bl native_fn_021f5328
    add r5, r0, #0x0
    bl native_fn_021f5328
    add r2, r0, #0x0
    ldr r0, =0x00000209
    ldr r1, =native_data_0220b11c
    str r0, [sp]
    lsl r3, r5, #0x2
    ldrh r1, [r1, r3]
    lsl r3, r2, #0x2
    ldr r2, =native_data_0220b11e
    add r0, r4, #0x0
    ldrh r2, [r2, r3]
    mov r3, #0x2
    str r6, [sp, #0x4]
    bl native_fn_022036ac
    add r0, r4, #0x0
    bl native_fn_022038ac
    add sp, #0x10
    pop {r4, r5, r6, pc}
    mov r8, r8
}
