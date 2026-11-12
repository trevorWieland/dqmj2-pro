/* ov001 row 0x02207610: 492 bytes.
 *
 * What it does: 119 instructions; 11 call(s) to 0x022068a0, 0x02207640, 0x02085284, +8 more; loops (back edge at +0x0c); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: block fill (119 instructions, 11 calls, 12 branches, 11 back edges, 4 literal slots).
 *
 *   pool +0x1dc -> native_data_0222f028 (image word 0x0222f028)
 *   pool +0x1e0 -> native_data_0222f03c (image word 0x0222f03c)
 *   pool +0x1e4 -> constant 0x021c9698 (image word 0x021c9698)
 *   pool +0x1e8 -> native_data_0222f04c (image word 0x0222f04c)
 *   branch +0x38 -> +0x98
 *   branch +0x3c -> +0x54
 *   branch +0x40 -> +0x60
 *   branch +0x44 -> +0x6c
 *   branch +0x48 -> +0x78
 *   branch +0x4c -> +0x84
 *   branch +0x50 -> +0x90
 *   branch +0x5c -> +0x98
 *   branch +0x68 -> +0x98
 *   branch +0x74 -> +0x98
 *   branch +0x80 -> +0x98
 *   branch +0x8c -> +0x98
 *   back edge +0xa0 -> +0x30
 *   back edge +0x1d0 -> +0xbc
 *   test +0x30 cmp r3, #5
 *   test +0x9c cmp r3, #6
 *   test +0x1b8 cmp r7, #2
 *   test +0x1cc cmp r10, #6
 *   1 block transfer(s), 13 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02207610; the literal pool and
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

extern void native_fn_022068a0(void);
extern u8 native_data_0222f028[];
extern u8 native_data_0222f03c[];
extern void native_fn_02085284(void);
extern void native_fn_02046af4(void);
extern void native_fn_02087a48(void);
extern void native_fn_02087720(void);
extern u8 native_data_0222f04c[];
extern void native_fn_02008be0(void);
extern void native_fn_020877bc(void);


asm u32 native_ov001_02207610 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #68
    mov r4, r0
    bl native_fn_022068a0
    add r0, r0, r4, lsl #5
    ldr r1, [r0, #0x1c]
    ldr r0, [r0, #0x24]
    ldr r1, [r1]
    add r2, r0, #524
    ldr r4, [r1, #0x4]
    mov r3, #0
    add r1, sp, #44
ov001_02207610_L30:
    cmp r3, #5
    addls pc, pc, r3, lsl #2
    b ov001_02207610_L98
    b ov001_02207610_L54
    b ov001_02207610_L60
    b ov001_02207610_L6c
    b ov001_02207610_L78
    b ov001_02207610_L84
    b ov001_02207610_L90
ov001_02207610_L54:
    ldrsh r0, [r2]
    str r0, [r1, r3, lsl #2]
    b ov001_02207610_L98
ov001_02207610_L60:
    ldrsh r0, [r2, #2]
    str r0, [r1, r3, lsl #2]
    b ov001_02207610_L98
ov001_02207610_L6c:
    ldrsh r0, [r2, #4]
    str r0, [r1, r3, lsl #2]
    b ov001_02207610_L98
ov001_02207610_L78:
    ldrsh r0, [r2, #6]
    str r0, [r1, r3, lsl #2]
    b ov001_02207610_L98
ov001_02207610_L84:
    ldrsh r0, [r2, #8]
    str r0, [r1, r3, lsl #2]
    b ov001_02207610_L98
ov001_02207610_L90:
    ldrsh r0, [r2, #10]
    str r0, [r1, r3, lsl #2]
ov001_02207610_L98:
    add r3, r3, #1
    cmp r3, #6
    blt ov001_02207610_L30
    ldr r8, =native_data_0222f028
    mov r7, #0
    ldr r9, =native_data_0222f03c
    mov r10, r7
    str r8, [sp, #0x8]
    add r11, sp, #12
ov001_02207610_Lbc:
    ldr r0, [sp, #0x8]
    ldrb r5, [r8]
    add r0, r0, r7
    ldrb r6, [r0, #0x3]
    ldrb r3, [r9]
    add r0, r4, #60
    mov r1, #5
    mov r2, #1
    bl native_fn_02085284
    str r11, [sp]
    mov r0, #255
    str r0, [sp, #0x4]
    ldr r0, =0x021c9698
    ldr r1, [r4, #0x68]
    mov r2, #16
    mov r3, #0
    bl native_fn_02046af4
    mov r0, #1
    stmia sp, {r0, r11}
    mov r0, r4
    mov r1, #0
    mov r2, r5
    mov r3, r6
    bl native_fn_02087a48
    ldr r0, =0x021c9698
    mov r1, r11
    mov r2, #16
    bl native_fn_02087720
    mov r1, #1
    add r0, r5, r0
    str r1, [sp]
    ldr r1, =native_data_0222f04c
    mov r0, r0, lsl #16
    mov r5, r0, asr #16
    str r1, [sp, #0x4]
    mov r0, r4
    mov r1, #0
    mov r2, r5
    mov r3, r6
    bl native_fn_02087a48
    mov r0, #0
    mov r1, r11
    mov r2, #32
    bl native_fn_02008be0
    add r0, sp, #44
    ldr r0, [r0, r10, lsl #2]
    mov r1, r11
    mov r2, #32
    mov r3, #0
    bl native_fn_020877bc
    add r1, r5, #8
    mov r1, r1, lsl #16
    mov r2, r1, asr #16
    mov r1, #1
    str r1, [sp]
    str r0, [sp, #0x4]
    mov r3, r6
    mov r0, r4
    mov r1, #0
    bl native_fn_02087a48
    add r0, r7, #1
    mov r0, r0, lsl #16
    mov r7, r0, asr #16
    cmp r7, #2
    add r10, r10, #1
    addgt r8, r8, #1
    movgt r7, #0
    add r9, r9, #1
    cmp r10, #6
    blt ov001_02207610_Lbc
    add sp, sp, #68
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
