/* ov000 row 0x02206724: 248 bytes.
 *
 * What it does: 58 instructions; 8 call(s) to 0x02048f2c, 0x02048f1c, 0x0201d444, +5 more; loops (back edge at +0x30); returns through pop {r3, r4, r5, r6, r7, r8, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xe8 -> native_data_0222f624 (image word 0x0222f624)
 *   pool +0xec -> native_data_0222ba0b (image word 0x0222ba0b)
 *   pool +0xf0 -> constant 0x02238270 (image word 0x02238270)
 *   pool +0xf4 -> constant 0x02238254 (image word 0x02238254)
 *   back edge +0x30 -> +0x18
 *   back edge +0xb0 -> +0x74
 *   test +0xa4 cmp r4, #7
 *   0 block transfer(s), 10 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02206724; the literal pool and
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

extern void native_fn_02048f2c(void);
extern void native_fn_02048f1c(void);
extern u8 native_data_0222f624[];
extern void native_fn_0201d444(void);
extern void native_fn_0205ff80(void);
extern u8 native_data_0222ba0b[];
extern void native_fn_0205ffcc(void);
extern void native_fn_02065730(void);
extern void native_fn_0205ff9c(void);


asm u32 native_ov000_02206724 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, lr}
    sub sp, sp, #36
    mov r8, r0
    add r3, sp, #4
    mov r0, #7
    mov r2, #0
ov000_02206724_L18:
    strb r2, [r3]
    strb r2, [r3, #0x1]
    strb r2, [r3, #0x2]
    strb r2, [r3, #0x3]
    add r3, r3, #4
    subs r0, r0, #1
    bne ov000_02206724_L18
    strb r2, [r3]
    mov r0, #2
    mov r1, #1
    strb r2, [r3, #0x1]
    bl native_fn_02048f2c
    mov r0, #3
    mov r1, #1
    bl native_fn_02048f1c
    ldr r1, =native_data_0222f624
    add r0, sp, #4
    bl native_fn_0201d444
    add r0, sp, #4
    bl native_fn_0205ff80
    ldr r5, =native_data_0222ba0b
    ldr r6, =0x02238270
    mov r4, #0
ov000_02206724_L74:
    ldrb r7, [r5, #0x2]
    mov r0, r6
    ldr r1, [r8, r7, lsl #2]
    mov r3, r7
    str r1, [sp]
    ldrsb r1, [r5]
    ldrb r2, [r5, #0x1]
    bl native_fn_0205ffcc
    ldr r1, [r8, r7, lsl #2]
    add r4, r4, #1
    add r0, r1, r0
    str r0, [r8, r7, lsl #2]
    cmp r4, #7
    add r5, r5, #3
    add r6, r6, #12
    blt ov000_02206724_L74
    ldr r1, [r8, #0x8]
    ldr r0, =0x02238254
    str r1, [sp]
    mov r1, #13
    mov r2, #1
    mov r3, #2
    bl native_fn_02065730
    ldr r1, [r8, #0x8]
    add r0, r1, r0
    str r0, [r8, #0x8]
    bl native_fn_0205ff9c
    add sp, sp, #36
    ldmia sp!, {r3, r4, r5, r6, r7, r8, pc}
}
