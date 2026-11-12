/* ov000 row 0x02228e54: 356 bytes.
 *
 * What it does: 89 instructions; 19 call(s) to 0x020449d4, 0x020449d4, 0x02228f98, +16 more; loops (back edge at +0x14); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x48 -> +0x144
 *   branch +0x50 -> +0x144
 *   branch +0x58 -> +0x144
 *   branch +0x68 -> +0x15c
 *   branch +0x74 -> +0x84
 *   branch +0xc8 -> +0xf4
 *   back edge +0xf8 -> +0x70
 *   back edge +0x118 -> +0x70
 *   back edge +0x128 -> +0x70
 *   back edge +0x13c -> +0x70
 *   branch +0x140 -> +0x15c
 *   test +0x34 cmp r4, #0
 *   test +0x4c cmp r10, #0
 *   test +0x54 cmp r8, #8
 *   test +0x64 cmp r0, #0
 *   test +0x70 cmp r6, #500
 *   test +0xc4 cmp r1, r0, lsr #19
 *   test +0xf4 cmp r10, r4
 *   test +0x114 cmp r8, r0
 *   test +0x124 cmp r0, #0
 *   test +0x138 cmp r7, r0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02228e54; the literal pool and
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

extern void native_fn_020449d4(void);
extern void native_fn_02228fdc(void);
extern void native_fn_02229f54(void);
extern void native_fn_02228924(void);
extern void native_fn_0222a1dc(void);


asm u32 native_ov000_02228e54 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r10, r0
    mov r9, r1
    mov r4, r2
    mov r11, r3
    bl native_fn_020449d4
    ldrh r1, [r0, #6]
    mov r0, r10
    mov r1, r1, lsl #19
    mov r6, r1, lsr #19
    bl native_fn_020449d4
    ldrh r0, [r0, #4]
    mov r7, #0
    cmp r4, #0
    mov r0, r0, lsl #24
    mov r0, r0, lsr #28
    strb r7, [r11]
    and r8, r0, #255
    bne ov000_02228e54_L144
    cmp r10, #0
    blt ov000_02228e54_L144
    cmp r8, #8
    beq ov000_02228e54_L144
    mov r0, r9
    bl native_fn_02228fdc
    cmp r0, #0
    ble ov000_02228e54_L15c
    mvn r4, #0
ov000_02228e54_L70:
    cmp r6, #500
    blo ov000_02228e54_L84
    mov r0, r8
    bl native_fn_02229f54
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov000_02228e54_L84:
    add r0, r6, #1
    mov r0, r0, lsl #16
    mov r6, r0, lsr #16
    mov r0, r6
    bl native_fn_02228924
    mov r10, r0
    bl native_fn_020449d4
    mov r5, r0
    mov r0, r8
    bl native_fn_02229f54
    bl native_fn_020449d4
    ldrh r1, [r5, #6]
    ldrh r0, [r0, #6]
    mov r1, r1, lsl #19
    mov r1, r1, lsr #19
    mov r0, r0, lsl #19
    cmp r1, r0, lsr #19
    bls ov000_02228e54_Lf4
    mov r0, r9
    bl native_fn_02228fdc
    sub r2, r0, r7
    ldrb r3, [r11]
    mov r1, #10
    mov r0, r8
    mla r1, r2, r1, r3
    strb r1, [r11]
    bl native_fn_02229f54
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov000_02228e54_Lf4:
    cmp r10, r4
    beq ov000_02228e54_L70
    mov r0, r10
    bl native_fn_020449d4
    ldrh r0, [r0, #4]
    mov r0, r0, lsl #24
    mov r0, r0, lsr #28
    and r0, r0, #255
    cmp r8, r0
    bne ov000_02228e54_L70
    mov r0, r10
    bl native_fn_0222a1dc
    cmp r0, #0
    bne ov000_02228e54_L70
    mov r0, r9
    add r7, r7, #1
    bl native_fn_02228fdc
    cmp r7, r0
    blt ov000_02228e54_L70
    b ov000_02228e54_L15c
ov000_02228e54_L144:
    mov r0, r9
    bl native_fn_02228fdc
    ldrb r2, [r11]
    mov r1, #10
    mla r1, r0, r1, r2
    strb r1, [r11]
ov000_02228e54_L15c:
    mov r0, r10
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
