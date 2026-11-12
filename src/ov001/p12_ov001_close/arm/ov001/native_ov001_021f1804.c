/* ov001 row 0x021f1804: 212 bytes.
 *
 * What it does: 52 instructions; 9 call(s) to 0x020c5938, 0x021f19f0, 0x02048094, +6 more; loops (back edge at +0x08); returns through pop {r4, r5, r6, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 9 calls (52 instructions, 9 calls, 0 branches, 8 back edges, 1 literal slot).
 *
 *   pool +0xd0 -> constant 0x021c9698 (image word 0x021c9698)
 *   test +0x28 cmp r0, #0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f1804; the literal pool and
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

extern void native_fn_020c5938(void);
extern void native_fn_021f19f0(void);
extern void native_fn_02048094(void);
extern void native_fn_0204a04c(void);
extern void native_fn_02008be0(void);
extern void native_fn_02046af4(void);
extern void native_fn_020470fc(void);
extern void native_fn_02087674(void);
extern void native_fn_02085270(void);


asm u32 native_ov001_021f1804 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    sub sp, sp, #72
    bl native_fn_020c5938
    add r0, r0, #1
    mov r1, r0, lsl #16
    mov r0, #2
    mov r4, r1, lsr #16
    ldr r6, =0x021c9698
    bl native_fn_021f19f0
    ldr r0, [r0]
    cmp r0, #0
    ldr r5, [r0, #0x4]
    addeq sp, sp, #72
    ldmeqia sp!, {r4, r5, r6, pc}
    mov r0, r4
    mov r1, #32
    bl native_fn_02048094
    mov r1, #1
    mov r0, r5
    mov r2, r1
    mov r3, #15
    bl native_fn_0204a04c
    add r1, sp, #8
    mov r0, #0
    mov r2, #64
    bl native_fn_02008be0
    add r1, sp, #8
    mov r0, #255
    str r1, [sp]
    str r0, [sp, #0x4]
    ldrb r2, [r5, #0x5e]
    ldr r1, [r5, #0x68]
    mov r0, r6
    mov r3, #0
    bl native_fn_02046af4
    add r0, sp, #8
    bl native_fn_020470fc
    strh r0, [r5, #108]
    mov r0, r6
    add r1, r5, #60
    add r2, sp, #8
    bl native_fn_02087674
    mov r3, r0
    ldrb r1, [r5, #0x5e]
    add r0, r5, #60
    mov r2, #0
    rsb r1, r3, r1, lsl #3
    mov r1, r1, lsl #15
    mov r1, r1, asr #16
    bl native_fn_02085270
    add sp, sp, #72
    ldmia sp!, {r4, r5, r6, pc}
}
