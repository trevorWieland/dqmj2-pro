/* ov000 row 0x021fe4b0: 336 bytes.
 *
 * What it does: 82 instructions; 9 call(s) to 0x02049008, 0x021fe5ec, 0x02063bbc, +6 more; loops (back edge at +0x38); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x148 -> constant 0x022372c4 (image word 0x022372c4)
 *   pool +0x14c -> native_data_0222f45c (image word 0x0222f45c)
 *   branch +0x1c -> +0x13c
 *   branch +0x48 -> +0x13c
 *   branch +0x64 -> +0x13c
 *   branch +0x7c -> +0x8c
 *   back edge +0x138 -> +0x58
 *   test +0x18 cmp r0, #1
 *   test +0x44 cmp r0, #0
 *   test +0x60 cmp r9, #47
 *   test +0x74 cmp r0, #0
 *   test +0x134 cmp r1, r0, asr #24
 *   0 block transfer(s), 12 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021fe4b0; the literal pool and
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

extern void native_fn_02049008(void);
extern void native_fn_02063bbc(void);
extern void native_fn_02049ad0(void);
extern void native_fn_02049f4c(void);
extern void native_fn_0204a154(void);
extern u8 native_data_0222f45c[];
extern void native_fn_0204a808(void);
extern void native_fn_0204a574(void);
extern void native_fn_02217dbc(void);


asm u32 native_ov000_021fe4b0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #16
    add r1, sp, #12
    mov r2, #0
    strh r2, [r1]
    strh r2, [r1, #2]
    cmp r0, #1
    bne ov000_021fe4b0_L13c
    ldr r6, =0x022372c4
    mov r1, #2
    mov r0, r6
    str r1, [sp]
    mov r1, #5
    mov r3, #1
    bl native_fn_02049008
    ldrh r0, [r6, #12]
    mov r7, #0
    cmp r0, #0
    ble ov000_021fe4b0_L13c
    mov r5, #16
    mov r11, r7
    add r4, sp, #12
ov000_021fe4b0_L58:
    ldr r0, [r6, #0x4]
    add r9, r0, r7
    cmp r9, #47
    bge ov000_021fe4b0_L13c
    mov r0, r9
    strh r5, [sp, #12]
    bl native_fn_02063bbc
    cmp r0, #0
    moveq r10, #0
    beq ov000_021fe4b0_L8c
    add r0, r9, #1
    mov r0, r0, lsl #16
    mov r10, r0, lsr #16
ov000_021fe4b0_L8c:
    add r0, r7, #5
    mov r0, r0, lsl #24
    mov r8, r0, asr #24
    mov r0, r8
    bl native_fn_02049ad0
    bl native_fn_02049f4c
    add r0, r9, #1
    mov r0, r0, lsl #16
    mov r3, r0, lsr #16
    str r11, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    mov r0, r8
    mov r1, r4
    mov r2, #1
    bl native_fn_0204a154
    ldrsh r3, [sp, #12]
    mov r1, r4
    mov r2, #1
    add r0, r3, r0
    strh r0, [sp, #12]
    mov r0, #0
    str r0, [sp]
    ldr r3, =native_data_0222f45c
    mov r0, r8
    bl native_fn_0204a808
    mov r1, #40
    strh r1, [sp, #12]
    str r10, [sp]
    mov r1, #1
    str r1, [sp, #0x4]
    mov r1, #0
    str r1, [sp, #0x8]
    mov r0, r8
    mov r1, r4
    mov r2, #18
    mov r3, #0
    bl native_fn_0204a574
    add r0, r7, #1
    mov r0, r0, lsl #24
    ldrh r1, [r6, #12]
    mov r7, r0, asr #24
    cmp r1, r0, asr #24
    bgt ov000_021fe4b0_L58
ov000_021fe4b0_L13c:
    bl native_fn_02217dbc
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
