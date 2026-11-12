/* ov001 row 0x021fddb4: 132 bytes.
 *
 * What it does: 32 instructions; 5 call(s) to 0x021fd074, 0x02202384, 0x02202398, +2 more; loops (back edge at +0x14); returns through pop {r4, r5, r6, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 5 calls (32 instructions, 5 calls, 0 branches, 3 back edges, 1 literal slot).
 *
 *   pool +0x80 -> constant 0x02239f4c (image word 0x02239f4c)
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021fddb4; the literal pool and
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

extern void native_fn_021fd074(void);
extern void native_fn_02202384(void);
extern void native_fn_02202398(void);
extern void native_fn_0206d250(void);
extern void native_fn_02045dc4(void);


asm u32 native_ov001_021fddb4 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    sub sp, sp, #8
    mov r4, r0
    mov r1, r4
    mov r0, #0
    bl native_fn_021fd074
    mov r5, r0
    mov r0, #0
    bl native_fn_02202384
    mov r0, r0, asr #3
    add r2, r0, #5
    mov r1, r4
    mov r0, #0
    and r6, r2, #255
    bl native_fn_02202398
    mov r4, r0
    ldrsb r0, [r5, #12]
    bl native_fn_0206d250
    mov r2, r6
    add r0, r0, r0, lsl #2
    add r0, r0, r4, asr #3
    add r0, r0, #3
    and r3, r0, #255
    mov r0, #2
    str r0, [sp]
    str r0, [sp, #0x4]
    mov r0, #1
    ldr r1, =0x02239f4c
    ldrb r1, [r1, #0x17]
    bl native_fn_02045dc4
    add sp, sp, #8
    ldmia sp!, {r4, r5, r6, pc}
}
