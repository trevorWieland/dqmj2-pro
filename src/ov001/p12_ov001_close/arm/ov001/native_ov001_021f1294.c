/* ov001 row 0x021f1294: 144 bytes.
 *
 * What it does: 35 instructions; 5 call(s) to 0x021f0f88, 0x02084dec, 0x02045ed0, +2 more; loops (back edge at +0x10); returns through pop {r3, r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 5 calls (35 instructions, 5 calls, 0 branches, 5 back edges, 1 literal slot).
 *
 *   pool +0x8c -> constant 0x02238f58 (image word 0x02238f58)
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f1294; the literal pool and
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

extern void native_fn_021f0f88(void);
extern void native_fn_02084dec(void);
extern void native_fn_02045ed0(void);
extern void native_fn_02085270(void);
extern void native_fn_02085264(void);


asm u32 native_ov001_021f1294 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    sub sp, sp, #8
    mov r4, r0
    mov r5, r1
    bl native_fn_021f0f88
    mov r1, r0, asr #4
    add r0, r0, r1, lsr #27
    mov r0, r0, asr #5
    add r0, r0, #1
    add r0, r0, #1
    mov r1, r5
    str r0, [sp]
    mov r3, #1
    mov r0, #0
    mov r2, #2
    str r3, [sp, #0x4]
    bl native_fn_02084dec
    ldr r1, =0x02238f58
    str r0, [r1, #0x4]
    mov r0, #1
    bl native_fn_02045ed0
    ldr r0, =0x02238f58
    mov r1, #12
    ldr r0, [r0, #0x4]
    mov r2, #2
    add r0, r0, #60
    bl native_fn_02085270
    mov r1, r4
    ldr r0, =0x02238f58
    mov r2, #0
    ldr r0, [r0, #0x4]
    add r0, r0, #48
    bl native_fn_02085264
    add sp, sp, #8
    ldmia sp!, {r3, r4, r5, pc}
}
