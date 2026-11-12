/* ov000 row 0x022276ac: 392 bytes.
 *
 * What it does: 93 instructions; 11 call(s) to 0x02063aa4, 0x02088a1c, 0x0204a858, +8 more; loops (back edge at +0x40); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 5 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x174 -> constant 0x022468cc (image word 0x022468cc)
 *   pool +0x178 -> constant 0x021c9698 (image word 0x021c9698)
 *   pool +0x17c -> native_data_0222ffa0 (image word 0x0222ffa0)
 *   pool +0x180 -> native_data_0222ffa4 (image word 0x0222ffa4)
 *   pool +0x184 -> native_data_0222ffa8 (image word 0x0222ffa8)
 *   branch +0x3c -> +0x48
 *   branch +0x44 -> +0x4c
 *   back edge +0x168 -> +0x24
 *   test +0x24 cmp r7, #0
 *   test +0x38 cmp r7, #0
 *   test +0x164 cmp r7, #2
 *   1 block transfer(s), 14 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022276ac; the literal pool and
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

extern void native_fn_02063aa4(void);
extern void native_fn_02088a1c(void);
extern void native_fn_0204a858(void);
extern u8 native_data_0222ffa0[];
extern void native_fn_0204a104(void);
extern void native_fn_0205dc70(void);
extern u8 native_data_0222ffa4[];
extern void native_fn_0204a154(void);
extern u8 native_data_0222ffa8[];


asm u32 native_ov000_022276ac (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #12
    mov r7, #0
    ldr r9, =0x022468cc
    ldr r5, =0x021c9698
    mov r8, r7
    add r4, sp, #8
    mov r11, #88
    mov r6, #8
ov000_022276ac_L24:
    cmp r7, #0
    moveq r10, #1
    movne r10, #0
    strh r6, [sp, #8]
    strh r8, [sp, #10]
    cmp r7, #0
    bne ov000_022276ac_L48
    bl native_fn_02063aa4
    b ov000_022276ac_L4c
ov000_022276ac_L48:
    bl native_fn_02088a1c
ov000_022276ac_L4c:
    stmia sp, {r0, r10}
    mov r0, #29
    mov r1, r5
    mov r2, r4
    mov r3, #1
    bl native_fn_0204a858
    ldr r3, =native_data_0222ffa0
    strh r11, [sp, #8]
    mov r0, #29
    mov r1, r4
    mov r2, #1
    bl native_fn_0204a104
    ldrsh r3, [sp, #8]
    mov r1, #7
    mov r2, #15
    add r0, r3, r0
    strh r0, [sp, #8]
    mov r0, #16
    bl native_fn_0205dc70
    str r0, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    mov r0, #29
    mov r1, r5
    mov r2, r4
    mov r3, #1
    bl native_fn_0204a858
    mov r0, #176
    strh r0, [sp, #8]
    ldr r3, =native_data_0222ffa4
    mov r0, #29
    mov r1, r4
    mov r2, #1
    bl native_fn_0204a104
    ldrsh r3, [sp, #8]
    mov r1, r4
    mov r2, #1
    add r0, r3, r0
    strh r0, [sp, #8]
    mov r0, #3
    str r0, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    ldrsb r3, [r9, #9]
    mov r0, #29
    bl native_fn_0204a154
    mov r0, #208
    strh r0, [sp, #8]
    ldr r3, =native_data_0222ffa8
    mov r0, #29
    mov r1, r4
    mov r2, #1
    bl native_fn_0204a104
    ldrsh r1, [sp, #8]
    mov r2, #1
    mov r3, #100
    add r0, r1, r0
    strh r0, [sp, #8]
    mov r0, #3
    str r0, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    mov r0, #29
    mov r1, r4
    bl native_fn_0204a154
    add r0, r7, #1
    mov r0, r0, lsl #24
    mov r7, r0, asr #24
    add r8, r8, #16
    add r9, r9, #1
    cmp r7, #2
    blt ov000_022276ac_L24
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
