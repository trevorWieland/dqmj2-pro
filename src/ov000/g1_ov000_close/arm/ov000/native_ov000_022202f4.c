/* ov000 row 0x022202f4: 300 bytes.
 *
 * What it does: 74 instructions; 12 call(s) to 0x02049ad0, 0x02049ffc, 0x02049f4c, +9 more; loops (back edge at +0x3c); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x128 -> constant 0x022463b0 (image word 0x022463b0)
 *   branch +0x18 -> +0xf0
 *   branch +0x58 -> +0xd8
 *   branch +0xa0 -> +0xb8
 *   branch +0xb4 -> +0xcc
 *   back edge +0xe0 -> +0x30
 *   test +0x14 cmp r0, #0
 *   test +0x54 cmp r0, #6
 *   test +0x94 cmp r10, r0
 *   test +0xdc cmp r4, #6
 *   test +0xf8 cmp r1, #0
 *   1 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022202f4; the literal pool and
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

extern void native_fn_02049ad0(void);
extern void native_fn_02049ffc(void);
extern void native_fn_02049f4c(void);
extern void native_fn_02228fb8(void);
extern void native_fn_020877bc(void);
extern void native_fn_02062b0c(void);
extern void native_fn_02087a48(void);
extern void native_fn_02086b14(void);
extern void native_fn_0221caf8(void);


asm u32 native_ov000_022202f4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #40
    ldr r1, =0x022463b0
    mov r6, r0
    ldrb r0, [r1]
    cmp r0, #0
    beq ov000_022202f4_Lf0
    mov r4, #0
    add r9, sp, #8
    mov r8, r4
    mov r11, #3
    mov r7, #1
ov000_022202f4_L30:
    add r0, r4, #20
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    mov r10, r0
    ldr r1, [r10]
    ldr r0, [r6, #0x4]
    ldr r5, [r1, #0x4]
    add r0, r4, r0
    cmp r0, #6
    bge ov000_022202f4_Ld8
    mov r0, r5
    bl native_fn_02049ffc
    mov r0, r10
    bl native_fn_02049f4c
    ldr r0, [r6, #0x4]
    add r0, r4, r0
    bl native_fn_02228fb8
    mov r10, r0
    mov r1, r9
    mov r2, #16
    mov r3, #6
    bl native_fn_020877bc
    strh r8, [sp, #20]
    bl native_fn_02062b0c
    cmp r10, r0
    mov r1, #0
    mov r2, #48
    bgt ov000_022202f4_Lb8
    mov r0, r5
    mov r3, r1
    stmia sp, {r7, r9}
    bl native_fn_02087a48
    b ov000_022202f4_Lcc
ov000_022202f4_Lb8:
    str r11, [sp]
    mov r0, r5
    mov r3, r1
    str r9, [sp, #0x4]
    bl native_fn_02087a48
ov000_022202f4_Lcc:
    mov r0, r5
    mov r1, #0
    bl native_fn_02086b14
ov000_022202f4_Ld8:
    add r4, r4, #1
    cmp r4, #6
    blt ov000_022202f4_L30
    ldr r0, =0x022463b0
    mov r1, #0
    strb r1, [r0]
ov000_022202f4_Lf0:
    ldr r0, =0x022463b0
    ldrb r1, [r0, #0x5]
    cmp r1, #0
    movne r1, #0
    strneb r1, [r0, #0x5]
    addne sp, sp, #40
    ldmneia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    ldr r0, [r6]
    bl native_fn_02228fb8
    ldr r1, =0x022463b0
    str r0, [r1, #0x20]
    bl native_fn_0221caf8
    add sp, sp, #40
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
