/* ov000 row 0x022122dc: 184 bytes.
 *
 * What it does: 45 instructions; 5 call(s) to 0x02211104, 0x02002618, 0x02025a28, +2 more; loops (back edge at +0x20); returns through pop {r3, r4, r5, r6, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0xb4 -> constant 0x45800000 (image word 0x45800000)
 *   4 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022122dc; the literal pool and
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

extern void native_fn_02211104(void);
extern void native_fn_02002618(void);
extern void native_fn_02025a28(void);
extern void native_fn_02025578(void);
extern void native_fn_020280fc(void);


asm u32 native_ov000_022122dc (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, lr}
    sub sp, sp, #12
    mov r0, r0, lsl #16
    mov r1, r1, lsl #16
    mov r0, r0, asr #16
    mov r1, r1, asr #16
    mov r6, r2
    mov r5, r3
    bl native_fn_02211104
    mov r4, r0
    add r3, r4, #312
    ldmia r6, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    add r0, r4, #132
    add r3, r4, #300
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    ldr r2, [r4, #0x84]
    ldr r1, [r4, #0x138]
    add r0, sp, #0
    sub r1, r2, r1
    str r1, [sp]
    ldr r3, [r4, #0x88]
    ldr r2, [r4, #0x13c]
    mov r1, r0
    sub r2, r3, r2
    str r2, [sp, #0x4]
    ldr r3, [r4, #0x8c]
    ldr r2, [r4, #0x140]
    sub r2, r3, r2
    str r2, [sp, #0x8]
    bl native_fn_02002618
    mov r0, r5
    bl native_fn_02025a28
    ldr r1, =0x45800000
    bl native_fn_02025578
    mov r2, r0
    add r0, r4, #324
    add r1, sp, #0
    bl native_fn_020280fc
    mov r0, #1
    strb r0, [r4, #0xb]
    mov r0, #0
    add sp, sp, #12
    ldmia sp!, {r3, r4, r5, r6, pc}
}
