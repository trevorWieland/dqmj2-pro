/* ov000 row 0x02228650: 724 bytes.
 *
 * What it does: 181 instructions; 31 call(s) to 0x020449d4, 0x020449d4, 0x020449d4, +28 more; loops (back edge at +0x20); returns through pop {r4, r5, r6, r7, r8, r9, r10, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x1c -> +0x3c
 *   branch +0x40 -> +0x64
 *   branch +0x68 -> +0xac
 *   branch +0x84 -> +0xa4
 *   branch +0xa0 -> +0xac
 *   branch +0x120 -> +0x170
 *   branch +0x128 -> +0x168
 *   branch +0x130 -> +0x14c
 *   branch +0x148 -> +0x18c
 *   branch +0x164 -> +0x18c
 *   branch +0x174 -> +0x184
 *   branch +0x180 -> +0x18c
 *   branch +0x190 -> +0x1a8
 *   branch +0x198 -> +0x1c0
 *   branch +0x1a0 -> +0x1d8
 *   branch +0x1a4 -> +0x20c
 *   branch +0x1bc -> +0x20c
 *   branch +0x1d4 -> +0x20c
 *   branch +0x224 -> +0x234
 *   branch +0x254 -> +0x2c4
 *   branch +0x268 -> +0x2c4
 *   branch +0x278 -> +0x2c4
 *   branch +0x2ac -> +0x2bc
 *   back edge +0x2c8 -> +0x238
 *   test +0x18 cmp r9, #0
 *   test +0x30 cmp r0, #8
 *   test +0x3c cmp r9, #1
 *   test +0x58 cmp r0, #8
 *   test +0x64 cmp r9, #2
 *   test +0x80 cmp r0, #8
 *   test +0x9c cmp r0, #8
 *   test +0x11c cmp r1, r0, lsr #28
 *   test +0x124 cmp r9, #0
 *   test +0x12c cmp r7, r6
 *   test +0x170 cmp r9, #2
 *   test +0x178 cmp r7, r6
 *   test +0x184 cmp r7, r6
 *   test +0x18c cmp r9, #0
 *   test +0x194 cmp r9, #1
 *   test +0x19c cmp r9, #2
 *   test +0x220 cmp r7, r0, lsr #19
 *   test +0x250 cmp r4, r5
 *   test +0x264 cmp r8, r0, lsr #28
 *   test +0x274 cmp r0, #0
 *   test +0x2a8 cmp r1, r0, lsr #19
 *   test +0x2c4 cmp r7, #1000
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02228650; the literal pool and
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
extern void native_fn_02228624(void);
extern void native_fn_022289fc(void);
extern void native_fn_02229f54(void);
extern void native_fn_02228924(void);
extern void native_fn_0222a1dc(void);


asm u32 native_ov000_02228650 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, lr}
    ldr r9, [sp, #0x20]
    mov r5, r0
    mov r4, r1
    mov r7, r2
    mov r6, r3
    cmp r9, #0
    bne ov000_02228650_L3c
    bl native_fn_020449d4
    ldrh r0, [r0, #4]
    mov r0, r0, lsl #24
    mov r0, r0, lsr #28
    cmp r0, #8
    moveq r0, r5
    ldmeqia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
ov000_02228650_L3c:
    cmp r9, #1
    bne ov000_02228650_L64
    mov r0, r4
    bl native_fn_020449d4
    ldrh r0, [r0, #4]
    mov r0, r0, lsl #24
    mov r0, r0, lsr #28
    cmp r0, #8
    moveq r0, r4
    ldmeqia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
ov000_02228650_L64:
    cmp r9, #2
    bne ov000_02228650_Lac
    mov r0, r5
    bl native_fn_020449d4
    ldrh r0, [r0, #4]
    mov r0, r0, lsl #24
    mov r0, r0, lsr #28
    cmp r0, #8
    beq ov000_02228650_La4
    mov r0, r4
    bl native_fn_020449d4
    ldrh r0, [r0, #4]
    mov r0, r0, lsl #24
    mov r0, r0, lsr #28
    cmp r0, #8
    bne ov000_02228650_Lac
ov000_02228650_La4:
    mvn r0, #0
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
ov000_02228650_Lac:
    mov r0, r5
    bl native_fn_020449d4
    ldrh r0, [r0, #6]
    mov r1, r5
    mov r2, r7
    mov r0, r0, lsl #19
    mov r0, r0, lsr #19
    bl native_fn_02228624
    mov r7, r0
    mov r0, r4
    bl native_fn_020449d4
    mov r2, r6
    ldrh r0, [r0, #6]
    mov r1, r4
    mov r0, r0, lsl #19
    mov r0, r0, lsr #19
    bl native_fn_02228624
    mov r6, r0
    mov r0, r5
    bl native_fn_020449d4
    mov r10, r0
    mov r0, r4
    bl native_fn_020449d4
    ldrh r1, [r10, #4]
    ldrh r0, [r0, #4]
    mov r1, r1, lsl #24
    mov r1, r1, lsr #28
    mov r0, r0, lsl #24
    cmp r1, r0, lsr #28
    bne ov000_02228650_L170
    cmp r9, #0
    bne ov000_02228650_L168
    cmp r7, r6
    bls ov000_02228650_L14c
    mov r0, r5
    bl native_fn_020449d4
    ldrh r0, [r0, #4]
    mov r0, r0, lsl #24
    mov r8, r0, lsr #28
    b ov000_02228650_L18c
ov000_02228650_L14c:
    mov r0, r4
    mov r7, r6
    bl native_fn_020449d4
    ldrh r0, [r0, #4]
    mov r0, r0, lsl #24
    mov r8, r0, lsr #28
    b ov000_02228650_L18c
ov000_02228650_L168:
    mvn r0, #0
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
ov000_02228650_L170:
    cmp r9, #2
    bhs ov000_02228650_L184
    cmp r7, r6
    movls r7, r6
    b ov000_02228650_L18c
ov000_02228650_L184:
    cmp r7, r6
    movhs r7, r6
ov000_02228650_L18c:
    cmp r9, #0
    beq ov000_02228650_L1a8
    cmp r9, #1
    beq ov000_02228650_L1c0
    cmp r9, #2
    beq ov000_02228650_L1d8
    b ov000_02228650_L20c
ov000_02228650_L1a8:
    mov r0, r5
    bl native_fn_020449d4
    ldrh r0, [r0, #4]
    mov r0, r0, lsl #24
    mov r8, r0, lsr #28
    b ov000_02228650_L20c
ov000_02228650_L1c0:
    mov r0, r4
    bl native_fn_020449d4
    ldrh r0, [r0, #4]
    mov r0, r0, lsl #24
    mov r8, r0, lsr #28
    b ov000_02228650_L20c
ov000_02228650_L1d8:
    mov r0, r5
    bl native_fn_020449d4
    mov r5, r0
    mov r0, r4
    bl native_fn_020449d4
    ldrh r1, [r5, #4]
    ldrh r0, [r0, #4]
    mov r2, r1, lsl #24
    mov r1, r0, lsl #24
    mov r0, r2, lsr #28
    mov r1, r1, lsr #28
    bl native_fn_022289fc
    mov r8, r0
ov000_02228650_L20c:
    mov r0, r8
    bl native_fn_02229f54
    bl native_fn_020449d4
    ldrh r0, [r0, #6]
    mov r0, r0, lsl #19
    cmp r7, r0, lsr #19
    blo ov000_02228650_L234
    mov r0, r8
    bl native_fn_02229f54
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
ov000_02228650_L234:
    mvn r5, #0
ov000_02228650_L238:
    add r0, r7, #1
    mov r0, r0, lsl #16
    mov r7, r0, lsr #16
    mov r0, r7
    bl native_fn_02228924
    mov r4, r0
    cmp r4, r5
    beq ov000_02228650_L2c4
    bl native_fn_020449d4
    ldrh r0, [r0, #4]
    mov r0, r0, lsl #24
    cmp r8, r0, lsr #28
    bne ov000_02228650_L2c4
    mov r0, r4
    bl native_fn_0222a1dc
    cmp r0, #0
    bne ov000_02228650_L2c4
    mov r0, r4
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
    blo ov000_02228650_L2bc
    mov r0, r8
    bl native_fn_02229f54
    mov r4, r0
ov000_02228650_L2bc:
    mov r0, r4
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
ov000_02228650_L2c4:
    cmp r7, #1000
    bls ov000_02228650_L238
    mvn r0, #0
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
}
