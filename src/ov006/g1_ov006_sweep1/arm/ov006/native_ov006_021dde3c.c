/* ov006 row 0x021dde3c: 204 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xb8 -> native_data_0220d0a8 (image word 0x0220d0a8)
 *   pool +0xbc -> native_data_0220d034 (image word 0x0220d034)
 *   pool +0xc0 -> constant 0x0220f510 (image word 0x0220f510)
 *   pool +0xc4 -> constant 0x0220f500 (image word 0x0220f500)
 *   pool +0xc8 -> constant 0x0220f4e8 (image word 0x0220f4e8)
 *   back edge +0x2c -> +0x14
 *   back edge +0x98 -> +0x54
 *   test +0x8c cmp r8, #11
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021dde3c; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity proves the instruction stream, not the meaning of the fields, blocks and callee contracts it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_0220d0a8[];
extern void native_fn_0201d444(void);
extern void native_fn_0205ff80(void);
extern u8 native_data_0220d034[];
extern void native_fn_0205ffcc(void);
extern void native_fn_0204976c(void);
extern void native_fn_0205ff9c(void);


asm u32 native_ov006_021dde3c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, lr}
    sub sp, sp, #36
    add r2, sp, #4
    mov r1, #8
    mov r0, #0
ov006_021dde3c_L14:
    strb r0, [r2]
    strb r0, [r2, #0x1]
    strb r0, [r2, #0x2]
    strb r0, [r2, #0x3]
    add r2, r2, #4
    subs r1, r1, #1
    bne ov006_021dde3c_L14
    ldr r1, =native_data_0220d0a8
    add r0, sp, #4
    bl native_fn_0201d444
    add r0, sp, #4
    bl native_fn_0205ff80
    ldr r5, =native_data_0220d034
    ldr r6, =0x0220f510
    ldr r4, =0x0220f500
    mov r8, #0
ov006_021dde3c_L54:
    ldrb r7, [r5, #0x2]
    mov r0, r6
    ldr r1, [r4, r7, lsl #2]
    mov r3, r7
    str r1, [sp]
    ldrsb r1, [r5]
    ldrb r2, [r5, #0x1]
    bl native_fn_0205ffcc
    add r1, r8, #1
    ldr r2, [r4, r7, lsl #2]
    mov r1, r1, lsl #24
    add r0, r2, r0
    mov r8, r1, asr #24
    str r0, [r4, r7, lsl #2]
    cmp r8, #11
    add r5, r5, #3
    add r6, r6, #12
    blt ov006_021dde3c_L54
    ldr r0, =0x0220f4e8
    ldr r0, [r0, #0x20]
    mov r0, r0, asr #5
    bl native_fn_0204976c
    bl native_fn_0205ff9c
    add sp, sp, #36
    ldmia sp!, {r3, r4, r5, r6, r7, r8, pc}
}
