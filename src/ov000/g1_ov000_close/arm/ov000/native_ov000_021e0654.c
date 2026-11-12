/* ov000 row 0x021e0654: 240 bytes.
 *
 * What it does: 59 instructions; 8 call(s) to 0x021e7f0c, 0x0220a514, 0x021e0498, +5 more; loops (back edge at +0x2c); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xec -> native_data_0222ebe8 (image word 0x0222ebe8)
 *   branch +0x60 -> +0x84
 *   branch +0x80 -> +0xd4
 *   branch +0x88 -> +0xa0
 *   branch +0x9c -> +0xd4
 *   branch +0xa4 -> +0xd4
 *   back edge +0xe0 -> +0x50
 *   test +0x30 cmp r10, #0
 *   test +0x58 cmp r0, #0
 *   test +0x68 cmp r8, r0
 *   test +0x84 cmp r0, #1
 *   test +0x90 cmp r8, r0
 *   test +0xa0 cmp r0, #2
 *   test +0xbc cmp r8, r1
 *   test +0xd8 cmp r6, r10
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e0654; the literal pool and
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

extern void native_fn_021e7f0c(void);
extern void native_fn_0220a514(void);
extern void native_fn_021e0498(void);
extern u8 native_data_0222ebe8[];
extern void native_fn_021e8c18(void);
extern void native_fn_02210f3c(void);
extern void native_fn_02044cdc(void);
extern void native_fn_02210864(void);


asm u32 native_ov000_021e0654 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #1120
    mov r8, #0
    add r1, sp, #0
    mov r0, r8
    bl native_fn_021e7f0c
    add r1, sp, #0
    bl native_fn_0220a514
    mov r10, r0
    add r0, sp, #0
    mov r1, r10
    bl native_fn_021e0498
    cmp r10, #0
    mov r6, r8
    addle sp, sp, #1120
    ldmleia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r11, #1
    ldr r4, =native_data_0222ebe8
    add r9, sp, #0
    mov r5, r11
ov000_021e0654_L50:
    ldr r0, [r9, #0x4]
    add r8, r8, #1
    cmp r0, #0
    ldr r7, [r9]
    bne ov000_021e0654_L84
    ldr r0, [r4]
    cmp r8, r0
    addgt sp, sp, #1120
    ldmgtia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r0, r7
    mov r1, r5
    bl native_fn_021e8c18
    b ov000_021e0654_Ld4
ov000_021e0654_L84:
    cmp r0, #1
    bne ov000_021e0654_La0
    ldr r0, [r4]
    cmp r8, r0
    addgt sp, sp, #1120
    ldmgtia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    b ov000_021e0654_Ld4
ov000_021e0654_La0:
    cmp r0, #2
    bne ov000_021e0654_Ld4
    mov r0, r7
    bl native_fn_02210f3c
    bl native_fn_02044cdc
    ldr r1, [r4]
    add r8, r8, r0
    cmp r8, r1
    addgt sp, sp, #1120
    ldmgtia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r0, r7
    mov r1, r11
    bl native_fn_02210864
ov000_021e0654_Ld4:
    add r6, r6, #1
    cmp r6, r10
    add r9, r9, #20
    blt ov000_021e0654_L50
    add sp, sp, #1120
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
