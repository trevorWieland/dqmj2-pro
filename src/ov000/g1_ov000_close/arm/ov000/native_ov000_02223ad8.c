/* ov000 row 0x02223ad8: 300 bytes.
 *
 * What it does: 69 instructions; 13 call(s) to 0x0201d444, 0x0205ff80, 0x02065730, +10 more; loops (back edge at +0x2c); returns through pop {r3, r4, r5, r6, r7, r8, pc}; 6 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x114 -> native_data_0222fdac (image word 0x0222fdac)
 *   pool +0x118 -> native_data_0222fd68 (image word 0x0222fd68)
 *   pool +0x11c -> constant 0x022465e8 (image word 0x022465e8)
 *   pool +0x120 -> constant 0x022465a8 (image word 0x022465a8)
 *   pool +0x124 -> native_data_0222fdc4 (image word 0x0222fdc4)
 *   pool +0x128 -> constant 0x02246594 (image word 0x02246594)
 *   back edge +0x2c -> +0x14
 *   back edge +0x98 -> +0x54
 *   branch +0xb4 -> +0xf8
 *   test +0x8c cmp r8, #6
 *   test +0xb0 cmp r0, #0
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02223ad8; the literal pool and
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

extern u8 native_data_0222fdac[];
extern void native_fn_0201d444(void);
extern void native_fn_0205ff80(void);
extern u8 native_data_0222fd68[];
extern void native_fn_02065730(void);
extern u8 native_data_0222fdc4[];
extern void native_fn_0202a8e0(void);
extern void native_fn_0203cc2c(void);
extern void native_fn_0204820c(void);
extern void native_fn_02048308(void);
extern void native_fn_0202a498(void);
extern void native_fn_0204976c(void);
extern void native_fn_0205ff9c(void);


asm u32 native_ov000_02223ad8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, lr}
    sub sp, sp, #36
    add r2, sp, #4
    mov r1, #8
    mov r0, #0
ov000_02223ad8_L14:
    strb r0, [r2]
    strb r0, [r2, #0x1]
    strb r0, [r2, #0x2]
    strb r0, [r2, #0x3]
    add r2, r2, #4
    subs r1, r1, #1
    bne ov000_02223ad8_L14
    ldr r1, =native_data_0222fdac
    add r0, sp, #4
    bl native_fn_0201d444
    add r0, sp, #4
    bl native_fn_0205ff80
    ldr r5, =native_data_0222fd68
    ldr r6, =0x022465e8
    ldr r4, =0x022465a8
    mov r8, #4
ov000_02223ad8_L54:
    ldrb r7, [r5, #0x2]
    mov r0, r6
    ldr r1, [r4, r7, lsl #2]
    mov r3, r7
    str r1, [sp]
    ldrsb r1, [r5]
    ldrb r2, [r5, #0x1]
    bl native_fn_02065730
    add r1, r8, #1
    ldr r2, [r4, r7, lsl #2]
    mov r1, r1, lsl #24
    add r0, r2, r0
    mov r8, r1, asr #24
    str r0, [r4, r7, lsl #2]
    cmp r8, #6
    add r5, r5, #3
    add r6, r6, #12
    blt ov000_02223ad8_L54
    ldr r1, =native_data_0222fdc4
    add r0, sp, #4
    bl native_fn_0201d444
    add r0, sp, #4
    bl native_fn_0202a8e0
    cmp r0, #0
    beq ov000_02223ad8_Lf8
    add r0, sp, #4
    mov r1, #2
    bl native_fn_0203cc2c
    mov r4, r0
    add r0, r4, #256
    mov r1, #160
    mov r2, #32
    bl native_fn_0204820c
    add r0, r4, #384
    mov r1, #256
    mov r2, #32
    bl native_fn_0204820c
    bl native_fn_02048308
    mov r1, r4
    mov r0, #2
    bl native_fn_0202a498
ov000_02223ad8_Lf8:
    ldr r0, =0x02246594
    ldr r0, [r0, #0x1c]
    mov r0, r0, asr #5
    bl native_fn_0204976c
    bl native_fn_0205ff9c
    add sp, sp, #36
    ldmia sp!, {r3, r4, r5, r6, r7, r8, pc}
}
