/* ov000 row 0x02207bd4: 208 bytes.
 *
 * What it does: 48 instructions; 9 call(s) to 0x02207c1c, 0x02206128, 0x0205db90, +6 more; loops (back edge at +0x2c); 4 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xc0 -> constant 0x022383e8 (image word 0x022383e8)
 *   pool +0xc4 -> native_data_0222f720 (image word 0x0222f720)
 *   pool +0xc8 -> constant 0x020dae90 (image word 0x020dae90)
 *   pool +0xcc -> constant 0x020dae88 (image word 0x020dae88)
 *   back edge +0x2c -> +0x14
 *   back edge +0x58 -> +0x48
 *   test +0x54 cmp r3, #4
 *   2 block transfer(s), 10 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02207bd4; the literal pool and
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

extern void native_fn_02206128(void);
extern u8 native_data_0222f720[];
extern void native_fn_0205db90(void);
extern void native_fn_0205d9e8(void);
extern void native_fn_0220819c(void);
extern void native_fn_02208638(void);
extern void native_fn_02045738(void);
extern void native_fn_0220668c(void);
extern void native_fn_020418b0(void);


asm u32 native_ov000_02207bd4 (register u32 a0)
{
    stmdb sp!, {lr}
    sub sp, sp, #36
    add r2, sp, #4
    mov r1, #8
    mov r0, #0
ov000_02207bd4_L14:
    strb r0, [r2]
    strb r0, [r2, #0x1]
    strb r0, [r2, #0x2]
    strb r0, [r2, #0x3]
    add r2, r2, #4
    subs r1, r1, #1
    bne ov000_02207bd4_L14
    ldr r1, =0x022383e8
    mov r3, #0
    strb r3, [r1, #0xf0]
    mov r0, #4
    strb r0, [r1, #0xf1]
    mov r2, #32
ov000_02207bd4_L48:
    add r0, r1, r3, lsl #2
    add r3, r3, #1
    str r2, [r0, #0xf4]
    cmp r3, #4
    blt ov000_02207bd4_L48
    bl native_fn_02206128
    ldr r2, =0x022383e8
    ldr r1, =native_data_0222f720
    strb r0, [r2, #0x114]
    add r0, sp, #4
    mvn r2, #0
    bl native_fn_0205db90
    mov r12, #4
    ldr r2, =0x020dae90
    ldr r3, =0x020dae88
    add r1, sp, #4
    mov r0, #2
    str r12, [sp]
    bl native_fn_0205d9e8
    ldr r1, =0x022383e8
    str r0, [r1, #0x120]
    bl native_fn_0220819c
    bl native_fn_02208638
    mov r0, #1
    bl native_fn_02045738
    bl native_fn_0220668c
    mov r0, #2
    bl native_fn_020418b0
    add sp, sp, #36
    ldmia sp!, {pc}
}
