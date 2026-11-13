/* ov000 row 0x021f9a18: 316 bytes.
 *
 * What it does: 76 instructions; 19 call(s) to 0x02215698, 0x02217440, 0x02215a8c, +16 more; loops (back edge at +0x38); returns through pop {r4, r5, r6, r7, r8, r9, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x130 -> native_data_0222f400 (image word 0x0222f400)
 *   pool +0x134 -> native_data_0222f414 (image word 0x0222f414)
 *   pool +0x138 -> native_data_0222f35c (image word 0x0222f35c)
 *   back edge +0x38 -> +0x20
 *   back edge +0xf8 -> +0x98
 *   test +0xf4 cmp r7, #12
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f9a18; the literal pool and
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

extern void ov000_display_context_02215698(void);
extern void native_fn_02217440(void);
extern void native_fn_02215a8c(void);
extern u8 native_data_0222f400[];
extern void native_fn_0203cc2c(void);
extern void native_fn_0204518c(void);
extern void native_fn_0221745c(void);
extern void native_fn_0202a498(void);
extern u8 native_data_0222f414[];
extern void native_fn_0201d444(void);
extern void native_fn_0205ff80(void);
extern u8 native_data_0222f35c[];
extern void native_fn_0221742c(void);
extern void native_fn_0221746c(void);
extern void native_fn_02065730(void);
extern void native_fn_02217500(void);
extern void native_fn_0205ff9c(void);
extern void native_fn_02219480(void);


asm u32 native_ov000_021f9a18 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, lr}
    sub sp, sp, #44
    bl ov000_display_context_02215698
    mov r4, r0
    bl native_fn_02217440
    add r3, sp, #12
    mov r2, #8
    mov r1, #0
ov000_021f9a18_L20:
    strb r1, [r3]
    strb r1, [r3, #0x1]
    strb r1, [r3, #0x2]
    strb r1, [r3, #0x3]
    add r3, r3, #4
    subs r2, r2, #1
    bne ov000_021f9a18_L20
    ldrsb r0, [r0, #16]
    bl native_fn_02215a8c
    ldr r0, =native_data_0222f400
    mov r1, #2
    bl native_fn_0203cc2c
    mov r5, r0
    add r0, sp, #4
    mov r1, r5
    mov r2, #13
    bl native_fn_0204518c
    ldr r1, [sp, #0x8]
    mov r0, #1
    bl native_fn_0221745c
    mov r1, r5
    mov r0, #2
    bl native_fn_0202a498
    ldr r1, =native_data_0222f414
    add r0, sp, #12
    bl native_fn_0201d444
    add r0, sp, #12
    bl native_fn_0205ff80
    ldr r5, =native_data_0222f35c
    mov r7, #0
ov000_021f9a18_L98:
    ldrb r8, [r5, #0x2]
    mov r0, r7, lsl #24
    mov r0, r0, asr #24
    mov r1, r8, lsl #24
    mov r9, r1, asr #24
    bl native_fn_0221742c
    mov r6, r0
    mov r0, r9
    bl native_fn_0221746c
    str r0, [sp]
    ldrsb r1, [r5]
    ldrb r2, [r5, #0x1]
    mov r3, r8
    mov r0, r6
    bl native_fn_02065730
    mov r6, r0
    mov r0, r9
    bl native_fn_0221746c
    add r1, r6, r0
    mov r0, r9
    bl native_fn_0221745c
    add r7, r7, #1
    add r5, r5, #3
    cmp r7, #12
    blt ov000_021f9a18_L98
    mov r0, #2
    bl native_fn_0221746c
    mov r0, r0, asr #5
    bl native_fn_02217500
    bl native_fn_0205ff9c
    mov r1, #1
    strb r1, [r4, #0x494]
    mov r0, #0
    strb r1, [r4, #0x49a]
    bl native_fn_02219480
    mov r0, #0
    add sp, sp, #44
    ldmia sp!, {r4, r5, r6, r7, r8, r9, pc}
}
