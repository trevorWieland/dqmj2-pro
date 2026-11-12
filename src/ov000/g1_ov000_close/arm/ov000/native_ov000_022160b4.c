/* ov000 row 0x022160b4: 408 bytes.
 *
 * What it does: 93 instructions; 15 call(s) to 0x02215a8c, 0x0203cc2c, 0x0204518c, +12 more; loops (back edge at +0x2c); returns through pop {r3, r4, r5, r6, r7, r8, pc}; 9 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x174 -> native_data_0222f9b8 (image word 0x0222f9b8)
 *   pool +0x178 -> constant 0x0224532c (image word 0x0224532c)
 *   pool +0x17c -> native_data_0222f9cc (image word 0x0222f9cc)
 *   pool +0x180 -> native_data_0222f937 (image word 0x0222f937)
 *   pool +0x184 -> constant 0x022455dc (image word 0x022455dc)
 *   pool +0x188 -> constant 0x0224535c (image word 0x0224535c)
 *   pool +0x18c -> native_data_0222f91c (image word 0x0222f91c)
 *   pool +0x190 -> constant 0x0224545c (image word 0x0224545c)
 *   pool +0x194 -> native_data_0222f918 (image word 0x0222f918)
 *   back edge +0x2c -> +0x14
 *   back edge +0xf4 -> +0xb8
 *   back edge +0x144 -> +0x108
 *   test +0x74 cmp r5, r0
 *   test +0xe8 cmp r5, #14
 *   test +0x138 cmp r8, #9
 *   0 block transfer(s), 10 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022160b4; the literal pool and
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

extern void native_fn_02215a8c(void);
extern u8 native_data_0222f9b8[];
extern void native_fn_0203cc2c(void);
extern void native_fn_0204518c(void);
extern void native_fn_0202a498(void);
extern void native_fn_02048308(void);
extern u8 native_data_0222f9cc[];
extern void native_fn_0201d444(void);
extern void native_fn_0205ff80(void);
extern u8 native_data_0222f937[];
extern void native_fn_0205ffcc(void);
extern u8 native_data_0222f91c[];
extern void native_fn_02065730(void);
extern void native_fn_02078e1c(void);
extern void native_fn_02217500(void);
extern void native_fn_0205ff9c(void);
extern u8 native_data_0222f918[];


asm u32 native_ov000_022160b4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, lr}
    sub sp, sp, #44
    add r3, sp, #12
    mov r2, #8
    mov r1, #0
ov000_022160b4_L14:
    strb r1, [r3]
    strb r1, [r3, #0x1]
    strb r1, [r3, #0x2]
    strb r1, [r3, #0x3]
    add r3, r3, #4
    subs r2, r2, #1
    bne ov000_022160b4_L14
    bl native_fn_02215a8c
    ldr r0, =native_data_0222f9b8
    mov r1, #2
    bl native_fn_0203cc2c
    mov r4, r0
    add r0, sp, #4
    mov r1, r4
    mov r2, #1
    bl native_fn_0204518c
    add r0, sp, #4
    mov r1, r4
    mov r2, #13
    ldr r5, [sp, #0x8]
    bl native_fn_0204518c
    ldr r2, =0x0224532c
    ldr r0, [sp, #0x8]
    ldr r3, [r2, #0x34]
    cmp r5, r0
    movlo r5, r0
    add r3, r3, r5
    mov r1, r4
    mov r0, #2
    str r3, [r2, #0x34]
    bl native_fn_0202a498
    bl native_fn_02048308
    ldr r1, =native_data_0222f9cc
    add r0, sp, #12
    bl native_fn_0201d444
    add r0, sp, #12
    bl native_fn_0205ff80
    ldr r6, =native_data_0222f937
    ldr r7, =0x022455dc
    ldr r4, =0x0224535c
    mov r5, #0
ov000_022160b4_Lb8:
    ldrb r8, [r6, #0x2]
    mov r0, r7
    ldr r1, [r4, r8, lsl #2]
    mov r3, r8
    str r1, [sp]
    ldrsb r1, [r6]
    ldrb r2, [r6, #0x1]
    bl native_fn_0205ffcc
    ldr r1, [r4, r8, lsl #2]
    add r5, r5, #1
    add r0, r1, r0
    str r0, [r4, r8, lsl #2]
    cmp r5, #14
    add r6, r6, #3
    add r7, r7, #12
    blt ov000_022160b4_Lb8
    ldr r5, =native_data_0222f91c
    ldr r6, =0x0224545c
    ldr r4, =0x0224535c
    mov r8, #0
ov000_022160b4_L108:
    ldrb r7, [r5, #0x2]
    mov r0, r6
    ldr r1, [r4, r7, lsl #2]
    mov r3, r7
    str r1, [sp]
    ldrsb r1, [r5]
    ldrb r2, [r5, #0x1]
    bl native_fn_02065730
    ldr r1, [r4, r7, lsl #2]
    add r8, r8, #1
    add r0, r1, r0
    str r0, [r4, r7, lsl #2]
    cmp r8, #9
    add r5, r5, #3
    add r6, r6, #12
    blt ov000_022160b4_L108
    bl native_fn_02078e1c
    ldr r0, =0x0224532c
    ldr r0, [r0, #0x38]
    mov r0, r0, asr #5
    bl native_fn_02217500
    bl native_fn_0205ff9c
    ldr r0, =native_data_0222f918
    mov r1, #18
    strh r1, [r0, #2]
    add sp, sp, #44
    ldmia sp!, {r3, r4, r5, r6, r7, r8, pc}
}
