/* ov001 row 0x021da814: 452 bytes.
 *
 * What it does: 112 instructions; 15 call(s) to 0x021eec7c, 0x022025a4, 0x021f949c, +12 more; loops (back edge at +0x74); returns through pop {r3, r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 15 calls (112 instructions, 15 calls, 18 branches, 4 back edges, 1 literal slot).
 *
 *   pool +0x1c0 -> constant 0xff7ffdff (image word 0xff7ffdff)
 *   branch +0x14 -> +0x1b8
 *   branch +0x18 -> +0x1b8
 *   branch +0x1c -> +0x30
 *   branch +0x20 -> +0xbc
 *   branch +0x24 -> +0x194
 *   branch +0x28 -> +0x1a8
 *   branch +0x2c -> +0x1b8
 *   branch +0x80 -> +0x90
 *   back edge +0x98 -> +0x70
 *   branch +0xb8 -> +0x1b8
 *   branch +0xd4 -> +0xec
 *   branch +0xe8 -> +0x100
 *   branch +0x114 -> +0x1b8
 *   branch +0x120 -> +0x138
 *   branch +0x134 -> +0x184
 *   branch +0x144 -> +0x168
 *   branch +0x150 -> +0x168
 *   branch +0x164 -> +0x184
 *   branch +0x190 -> +0x1b8
 *   branch +0x1a4 -> +0x1b8
 *   test +0x0c cmp r1, #5
 *   test +0x7c tst r0, #16
 *   test +0x94 cmp r5, #60
 *   test +0xc8 cmp r0, #2
 *   test +0x110 cmp r0, r5
 *   test +0x11c tst r0, #4
 *   test +0x140 cmp r0, #0
 *   test +0x14c tst r0, #32
 *   test +0x198 cmp r0, #0
 *   test +0x1ac cmp r0, #0
 *   0 block transfer(s), 11 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021da814; the literal pool and
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

extern void ov001_effect_resource_create_021eec7c(void);
extern void native_fn_022025a4(void);
extern void native_fn_021f949c(void);
extern void native_fn_021d8dec(void);
extern void native_fn_021dc940(void);
extern void native_fn_021e865c(void);
extern void native_fn_02044cdc(void);
extern void native_fn_021d96d4(void);
extern void native_fn_021e29e8(void);
extern void native_fn_021db410(void);
extern void native_fn_022177e0(void);
extern void native_fn_021f5d6c(void);


asm u32 native_ov001_021da814 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r4, r0
    ldrb r1, [r4, #0x326]
    cmp r1, #5
    addls pc, pc, r1, lsl #2
    b ov001_021da814_L1b8
    b ov001_021da814_L1b8
    b ov001_021da814_L30
    b ov001_021da814_Lbc
    b ov001_021da814_L194
    b ov001_021da814_L1a8
    b ov001_021da814_L1b8
ov001_021da814_L30:
    add r0, r4, #768
    mov r2, #0
    strh r2, [r0, #32]
    mov r0, #2
    strb r0, [r4, #0x326]
    mov r1, r4
    mov r0, #4
    bl ov001_effect_resource_create_021eec7c
    ldrb r0, [r4, #0x31e]
    ldrb r1, [r4, #0x31f]
    mov r2, #1
    bl native_fn_022025a4
    mov r0, #229
    mov r1, #0
    bl native_fn_021f949c
    mov r5, #0
ov001_021da814_L70:
    mov r0, r5
    bl native_fn_021d8dec
    ldrb r0, [r0, #0x3]
    tst r0, #16
    bne ov001_021da814_L90
    mov r0, r4
    mov r1, r5
    bl native_fn_021dc940
ov001_021da814_L90:
    add r5, r5, #1
    cmp r5, #60
    blt ov001_021da814_L70
    ldrb r0, [r4, #0x31e]
    ldrb r1, [r4, #0x31f]
    bl native_fn_021e865c
    ldr r1, [r4, #0x33c]
    ldr r0, =0xff7ffdff
    and r0, r1, r0
    str r0, [r4, #0x33c]
    b ov001_021da814_L1b8
ov001_021da814_Lbc:
    ldr r0, [r4, #0x1e8]
    ldrsh r0, [r0, #42]
    bl native_fn_02044cdc
    cmp r0, #2
    add r0, r4, #768
    ldrsh r0, [r0, #32]
    bne ov001_021da814_Lec
    rsbs r0, r0, #31
    movmi r0, #0
    and r1, r0, #255
    mov r5, #90
    b ov001_021da814_L100
ov001_021da814_Lec:
    mov r0, r0, lsl #1
    rsbs r0, r0, #31
    movmi r0, #0
    and r1, r0, #255
    mov r5, #48
ov001_021da814_L100:
    mov r0, r4
    bl native_fn_021d96d4
    add r0, r4, #768
    ldrsh r0, [r0, #32]
    cmp r0, r5
    ble ov001_021da814_L1b8
    ldr r0, [r4, #0x33c]
    tst r0, #4
    beq ov001_021da814_L138
    mov r0, #0
    strb r0, [r4, #0x327]
    mov r0, #3
    strb r0, [r4, #0x326]
    b ov001_021da814_L184
ov001_021da814_L138:
    add r0, r4, #512
    ldrsb r0, [r0, #83]
    cmp r0, #0
    beq ov001_021da814_L168
    bl native_fn_021e29e8
    tst r0, #32
    bne ov001_021da814_L168
    mov r0, #0
    strb r0, [r4, #0x327]
    mov r0, #4
    strb r0, [r4, #0x326]
    b ov001_021da814_L184
ov001_021da814_L168:
    mov r0, r4
    mov r1, #39
    bl native_fn_021dc940
    mov r0, #5
    strb r0, [r4, #0x326]
    mov r0, #1
    strb r0, [r4, #0x1ff]
ov001_021da814_L184:
    mov r0, r4
    mov r1, #0
    bl native_fn_021db410
    b ov001_021da814_L1b8
ov001_021da814_L194:
    bl native_fn_022177e0
    cmp r0, #0
    movne r0, #0
    strneb r0, [r4, #0x326]
    b ov001_021da814_L1b8
ov001_021da814_L1a8:
    bl native_fn_021f5d6c
    cmp r0, #0
    movne r0, #0
    strneb r0, [r4, #0x326]
ov001_021da814_L1b8:
    ldrb r0, [r4, #0x326]
    ldmia sp!, {r3, r4, r5, pc}
}
