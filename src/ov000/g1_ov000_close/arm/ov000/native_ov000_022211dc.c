/* ov000 row 0x022211dc: 220 bytes.
 *
 * What it does: 52 instructions; 6 call(s) to 0x0221c658, 0x0221c758, 0x02008c58, +3 more; loops (back edge at +0x08); 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xd0 -> constant 0x022463b0 (image word 0x022463b0)
 *   pool +0xd4 -> constant 0x022463dc (image word 0x022463dc)
 *   pool +0xd8 -> constant 0x02246424 (image word 0x02246424)
 *   2 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022211dc; the literal pool and
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

extern void native_fn_0221c658(void);
extern void native_fn_0221c758(void);
extern void native_fn_02008c58(void);
extern void native_fn_020603ec(void);
extern void native_fn_020449d4(void);
extern void native_fn_0221f5fc(void);


asm u32 native_ov000_022211dc (register u32 a0)
{
    stmdb sp!, {lr}
    sub sp, sp, #84
    bl native_fn_0221c658
    mov r1, #3
    str r1, [sp]
    mov r1, #18
    str r1, [sp, #0x4]
    mov r2, #2
    str r2, [sp, #0x8]
    mov r1, #0
    str r1, [sp, #0xc]
    mov r3, #1
    str r3, [sp, #0x10]
    ldrsb r1, [r0, #16]
    mov r0, #29
    bl native_fn_0221c758
    add r1, sp, #20
    mov r0, #0
    mov r2, #64
    bl native_fn_02008c58
    ldr r0, =0x022463b0
    mov r2, #16
    ldrb r12, [r0, #0x3]
    ldr r1, =0x022463dc
    add r0, sp, #20
    str r2, [sp]
    mov r2, r12, lsl #1
    ldrsh r1, [r1, r2]
    ldr r2, =0x02246424
    mov r3, #15
    ldrb r2, [r2, r12]
    bl native_fn_020603ec
    ldr r0, =0x022463b0
    ldr r1, =0x022463dc
    ldrb r0, [r0, #0x3]
    mov r0, r0, lsl #1
    ldrsh r0, [r1, r0]
    bl native_fn_020449d4
    mov r1, #0
    str r1, [sp]
    mov r1, #1
    str r1, [sp, #0x4]
    ldrh r2, [r0, #4]
    mov r0, #29
    add r1, sp, #20
    mov r2, r2, lsl #24
    mov r2, r2, lsr #28
    and r2, r2, #255
    mov r3, #16
    bl native_fn_0221f5fc
    add sp, sp, #84
    ldmia sp!, {pc}
}
