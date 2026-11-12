/* ov001 row 0x02208e70: 876 bytes.
 *
 * What it does: 217 instructions; 18 call(s) to 0x02207938, 0x020852d0, 0x02008be0, +15 more; loops (back edge at +0x08); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 18 calls (217 instructions, 18 calls, 19 branches, 17 back edges, 2 literal slots).
 *
 *   pool +0x364 -> native_data_0222f0a8 (image word 0x0222f0a8)
 *   pool +0x368 -> native_data_0222f0ac (image word 0x0222f0ac)
 *   branch +0x74 -> +0xa8
 *   branch +0xa4 -> +0x334
 *   branch +0xb4 -> +0x334
 *   branch +0xe0 -> +0x334
 *   branch +0x110 -> +0x220
 *   branch +0x114 -> +0x220
 *   branch +0x118 -> +0x138
 *   branch +0x11c -> +0x138
 *   branch +0x120 -> +0x138
 *   branch +0x124 -> +0x138
 *   branch +0x128 -> +0x138
 *   branch +0x12c -> +0x1d4
 *   branch +0x130 -> +0x220
 *   branch +0x134 -> +0x138
 *   branch +0x154 -> +0x19c
 *   branch +0x164 -> +0x178
 *   branch +0x174 -> +0x184
 *   back edge +0x198 -> +0x15c
 *   branch +0x1d0 -> +0x254
 *   branch +0x21c -> +0x254
 *   branch +0x25c -> +0x310
 *   back edge +0x330 -> +0xc0
 *   back edge +0x358 -> +0x30
 *   test +0x54 cmp r0, #0
 *   test +0x70 cmp r1, r0
 *   test +0xb0 cmp r11, r0
 *   test +0xdc cmp r0, #0
 *   test +0xe8 cmp r0, #0
 *   test +0x108 cmp r9, #8
 *   test +0x140 cmp r0, #0
 *   test +0x150 cmp r6, #0
 *   test +0x160 cmp r0, #0
 *   test +0x190 cmp r6, r0, asr #24
 *   test +0x1e0 cmp r0, #1
 *   test +0x258 cmp r5, #0
 *   test +0x2a4 cmp r0, #54
 *   test +0x32c cmp r0, r1, asr #16
 *   test +0x348 cmp r0, #2
 *   0 block transfer(s), 35 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02208e70; the literal pool and
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

extern void native_fn_02207938(void);
extern void native_fn_020852d0(void);
extern void native_fn_02008be0(void);
extern void native_fn_0204a574(void);
extern void native_fn_0206092c(void);
extern u8 native_data_0222f0a8[];
extern void native_fn_02087a48(void);
extern void native_fn_020877bc(void);
extern u8 native_data_0222f0ac[];


asm u32 native_ov001_02208e70 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #104
    bl native_fn_02207938
    str r0, [sp, #0x14]
    ldr r0, [r0, #0x8]
    mov r1, #0
    ldr r0, [r0]
    ldr r0, [r0, #0x4]
    str r0, [sp, #0x1c]
    bl native_fn_020852d0
    mov r0, #0
    str r0, [sp, #0x18]
ov001_02208e70_L30:
    ldr r0, [sp, #0x14]
    add r1, sp, #40
    ldrsh r11, [r0, #112]
    mov r0, #0
    mov r2, #64
    bl native_fn_02008be0
    mov r0, #0
    strh r0, [sp, #34]
    ldr r0, [sp, #0x18]
    cmp r0, #0
    moveq r0, #8
    movne r0, #128
    strh r0, [sp, #32]
    ldr r0, [sp, #0x14]
    ldrsh r1, [r0, #110]
    ldrsh r0, [r0, #112]
    cmp r1, r0
    bgt ov001_02208e70_La8
    mov r0, #63
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    mov r4, #0
    add r1, sp, #32
    mov r0, #26
    mov r2, #5
    mov r3, #3
    str r4, [sp, #0x8]
    bl native_fn_0204a574
    b ov001_02208e70_L334
ov001_02208e70_La8:
    add r0, r11, #6
    str r0, [sp, #0x10]
    cmp r11, r0
    bge ov001_02208e70_L334
    mov r10, #37
    mov r4, #36
ov001_02208e70_Lc0:
    mov r0, #0
    add r1, sp, #40
    mov r2, #64
    bl native_fn_02008be0
    ldr r0, [sp, #0x14]
    add r8, r0, r11
    ldrsb r0, [r8, #44]
    cmp r0, #0
    beq ov001_02208e70_L334
    ldr r0, [sp, #0x18]
    cmp r0, #0
    moveq r0, #8
    movne r0, #128
    strh r0, [sp, #32]
    ldr r0, [sp, #0x14]
    add r0, r0, r11
    ldrsb r9, [r0, #44]
    str r0, [sp, #0xc]
    cmp r9, #8
    addls pc, pc, r9, lsl #2
    b ov001_02208e70_L220
    b ov001_02208e70_L220
    b ov001_02208e70_L138
    b ov001_02208e70_L138
    b ov001_02208e70_L138
    b ov001_02208e70_L138
    b ov001_02208e70_L138
    b ov001_02208e70_L1d4
    b ov001_02208e70_L220
    b ov001_02208e70_L138
ov001_02208e70_L138:
    ldrsb r0, [r8, #66]
    mov r5, #0
    cmp r0, #0
    rsble r0, r0, #0
    mov r0, r0, lsl #24
    mov r6, r0, asr #24
    cmp r6, #0
    ble ov001_02208e70_L19c
    mov r7, r5
ov001_02208e70_L15c:
    ldrsb r0, [r8, #66]
    cmp r0, #0
    ble ov001_02208e70_L178
    mov r0, r4
    mov r1, r7
    bl native_fn_0206092c
    b ov001_02208e70_L184
ov001_02208e70_L178:
    mov r0, r10
    mov r1, r7
    bl native_fn_0206092c
ov001_02208e70_L184:
    add r7, r7, #2
    add r0, r5, #1
    mov r0, r0, lsl #24
    cmp r6, r0, asr #24
    mov r5, r0, asr #24
    bgt ov001_02208e70_L15c
ov001_02208e70_L19c:
    str r9, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    mov r0, #0
    str r0, [sp, #0x8]
    mov r0, #26
    add r1, sp, #32
    mov r2, #5
    mov r3, #3
    bl native_fn_0204a574
    ldrsh r1, [sp, #32]
    add r0, r1, r0
    strh r0, [sp, #32]
    b ov001_02208e70_L254
ov001_02208e70_L1d4:
    ldrsb r0, [r8, #66]
    add r1, sp, #32
    mov r2, #5
    cmp r0, #1
    movne r9, #62
    mov r0, r9, lsl #16
    mov r0, r0, lsr #16
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    mov r0, #0
    str r0, [sp, #0x8]
    mov r0, #26
    mov r3, #3
    bl native_fn_0204a574
    ldrsh r1, [sp, #32]
    add r0, r1, r0
    strh r0, [sp, #32]
    b ov001_02208e70_L254
ov001_02208e70_L220:
    str r9, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    mov r0, #0
    str r0, [sp, #0x8]
    mov r0, #26
    add r1, sp, #32
    mov r2, #5
    mov r3, #3
    bl native_fn_0204a574
    ldrsh r1, [sp, #32]
    add r0, r1, r0
    strh r0, [sp, #32]
ov001_02208e70_L254:
    ldrsb r5, [r8, #88]
    cmp r5, #0
    ble ov001_02208e70_L310
    mov r0, #1
    str r0, [sp]
    ldr r0, =native_data_0222f0a8
    mov r1, #0
    str r0, [sp, #0x4]
    ldrsh r2, [sp, #32]
    ldrsh r3, [sp, #34]
    ldr r0, [sp, #0x1c]
    bl native_fn_02087a48
    ldrsh r1, [sp, #32]
    mov r2, #4
    mov r3, #0
    add r0, r1, r0
    strh r0, [sp, #32]
    ldr r0, [sp, #0xc]
    add r1, sp, #36
    ldrsb r0, [r0, #44]
    cmp r0, #54
    subeq r5, r5, #1
    mov r0, r5
    bl native_fn_020877bc
    mov r1, #1
    str r1, [sp]
    str r0, [sp, #0x4]
    ldrsh r2, [sp, #32]
    ldrsh r3, [sp, #34]
    ldr r0, [sp, #0x1c]
    mov r1, #0
    bl native_fn_02087a48
    ldrsh r2, [sp, #32]
    mov r1, #0
    add r0, r2, r0
    strh r0, [sp, #32]
    mov r0, #1
    str r0, [sp]
    ldr r0, =native_data_0222f0ac
    str r0, [sp, #0x4]
    ldrsh r2, [sp, #32]
    ldrsh r3, [sp, #34]
    ldr r0, [sp, #0x1c]
    bl native_fn_02087a48
    ldrsh r1, [sp, #32]
    add r0, r1, r0
    strh r0, [sp, #32]
ov001_02208e70_L310:
    ldrsh r2, [sp, #34]
    add r0, r11, #1
    mov r1, r0, lsl #16
    add r0, r2, #16
    strh r0, [sp, #34]
    ldr r0, [sp, #0x10]
    mov r11, r1, asr #16
    cmp r0, r1, asr #16
    bgt ov001_02208e70_Lc0
ov001_02208e70_L334:
    ldr r0, [sp, #0x18]
    add r0, r0, #1
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    str r0, [sp, #0x18]
    cmp r0, #2
    ldr r0, [sp, #0x14]
    add r0, r0, #70
    str r0, [sp, #0x14]
    blt ov001_02208e70_L30
    add sp, sp, #104
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
