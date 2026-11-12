/* ov000 row 0x022157a0: 112 bytes.
 *
 * What it does: 25 instructions; 5 call(s) to 0x02008d78, 0x0204b1c0, 0x022157c4, +2 more; loops (back edge at +0x10); returns through pop {r3, r4, r5, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x64 -> constant 0x02245a54 (image word 0x02245a54)
 *   pool +0x68 -> constant 0x022459b4 (image word 0x022459b4)
 *   pool +0x6c -> constant 0x02245a6c (image word 0x02245a6c)
 *   back edge +0x38 -> +0x24
 *   back edge +0x5c -> +0x44
 *   test +0x30 cmp r4, #8
 *   test +0x54 cmp r5, #12
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022157a0; the literal pool and
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

extern void native_fn_02008d78(void);
extern void native_fn_0204b1c0(void);
extern void native_fn_02063270(void);


asm u32 native_ov000_022157a0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r0, =0x02245a54
    mov r1, #0
    mov r2, #24
    bl native_fn_02008d78
    ldr r0, =0x022459b4
    mov r4, #0
    ldr r5, =0x02245a6c
    strb r4, [r0, #0x496]
ov000_022157a0_L24:
    mov r0, r5
    bl native_fn_0204b1c0
    add r4, r4, #1
    cmp r4, #8
    add r5, r5, #80
    blt ov000_022157a0_L24
    ldr r4, =0x022459b4
    mov r5, #0
ov000_022157a0_L44:
    and r0, r5, #255
    bl native_fn_02063270
    add r5, r5, #1
    strb r0, [r4, #0x478]
    cmp r5, #12
    add r4, r4, #1
    blt ov000_022157a0_L44
    ldmia sp!, {r3, r4, r5, pc}
}
