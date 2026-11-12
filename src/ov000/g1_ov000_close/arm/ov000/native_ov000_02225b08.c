/* ov000 row 0x02225b08: 232 bytes.
 *
 * What it does: 56 instructions; 8 call(s) to 0x0206271c, 0x02062a10, 0x02008e0c, +5 more; loops (back edge at +0x34); returns through pop {r3, r4, r5, r6, r7, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xe0 -> constant 0x02246aa8 (image word 0x02246aa8)
 *   pool +0xe4 -> constant 0x022468b8 (image word 0x022468b8)
 *   branch +0x84 -> +0xa8
 *   back edge +0xa4 -> +0x78
 *   test +0x08 cmp r7, #3
 *   test +0x24 cmp r2, #0
 *   test +0x80 cmp r1, #0
 *   test +0xa0 cmp r4, #5
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02225b08; the literal pool and
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

extern void native_fn_0206271c(void);
extern void native_fn_02062a10(void);
extern void native_fn_02008e0c(void);
extern void native_fn_0207aebc(void);
extern void native_fn_02223d58(void);
extern void native_fn_02223e40(void);
extern void native_fn_021f51d4(void);


asm u32 native_ov000_02225b08 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    mov r7, r0
    cmp r7, #3
    mov r0, #0
    ldr r2, =0x02246aa8
    ldmhsia sp!, {r3, r4, r5, r6, r7, pc}
    mov r1, #132
    mla r5, r7, r1, r2
    ldrsh r2, [r5, #24]
    cmp r2, #0
    ldmeqia sp!, {r3, r4, r5, r6, r7, pc}
    ldrb r1, [r5, #0x1a]
    mov r0, r2
    bl native_fn_0206271c
    ldr r1, =0x022468b8
    mov r4, r0
    ldrsb r2, [r1, #29]
    add r2, r2, #1
    strb r2, [r1, #0x1d]
    ldrsb r2, [r1, #30]
    sub r2, r2, #1
    strb r2, [r1, #0x1e]
    bl native_fn_02062a10
    mov r6, r0
    mov r0, r5
    mov r1, r6
    mov r2, #132
    bl native_fn_02008e0c
    str r4, [r6, #0x14]
    mov r4, #0
ov000_02225b08_L78:
    add r2, r6, r4, lsl #1
    ldrb r1, [r2, #0x7a]
    cmp r1, #0
    beq ov000_02225b08_La8
    ldrsh r0, [r5, #24]
    ldrb r2, [r2, #0x7b]
    bl native_fn_0207aebc
    add r0, r4, #1
    mov r0, r0, lsl #24
    mov r4, r0, asr #24
    cmp r4, #5
    blt ov000_02225b08_L78
ov000_02225b08_La8:
    mov r0, r7, lsl #24
    mov r4, r0, asr #24
    mov r1, r4
    mov r0, #1
    mov r2, #0
    bl native_fn_02223d58
    mov r0, #1
    mov r1, r4
    mov r2, r0
    bl native_fn_02223e40
    mov r0, #1
    bl native_fn_021f51d4
    mov r0, #1
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
