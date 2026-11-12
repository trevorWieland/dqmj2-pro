/* ov001 row 0x022086b4: 1676 bytes.
 *
 * What it does: 411 instructions; 49 call(s) to 0x02207938, 0x020852d0, 0x02008be0, +46 more; loops (back edge at +0x08); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 8 literal slot(s) in the extent
 *
 * Decoded shape: block fill (411 instructions, 49 calls, 32 branches, 47 back edges, 8 literal slots).
 *
 *   pool +0x66c -> native_data_0222f050 (image word 0x0222f050)
 *   pool +0x670 -> native_data_0222f094 (image word 0x0222f094)
 *   pool +0x674 -> constant 0x00002710 (image word 0x00002710)
 *   pool +0x678 -> native_data_0222f098 (image word 0x0222f098)
 *   pool +0x67c -> native_data_0222f09c (image word 0x0222f09c)
 *   pool +0x680 -> native_data_0222f0a0 (image word 0x0222f0a0)
 *   pool +0x684 -> native_data2_0222f050 (image word 0x0222f050)
 *   pool +0x688 -> native_data_0222f0a4 (image word 0x0222f0a4)
 *   branch +0x64 -> +0x364
 *   branch +0x110 -> +0x24c
 *   branch +0x114 -> +0x130
 *   branch +0x118 -> +0x180
 *   branch +0x11c -> +0x1e8
 *   branch +0x120 -> +0x210
 *   branch +0x124 -> +0x220
 *   branch +0x128 -> +0x230
 *   branch +0x12c -> +0x240
 *   branch +0x16c -> +0x24c
 *   branch +0x17c -> +0x24c
 *   branch +0x1c0 -> +0x24c
 *   branch +0x1e4 -> +0x24c
 *   branch +0x20c -> +0x24c
 *   branch +0x21c -> +0x24c
 *   branch +0x22c -> +0x24c
 *   branch +0x23c -> +0x24c
 *   branch +0x260 -> +0x278
 *   branch +0x26c -> +0x278
 *   branch +0x280 -> +0x294
 *   branch +0x288 -> +0x294
 *   branch +0x290 -> +0x364
 *   branch +0x2f0 -> +0x364
 *   back edge +0x380 -> +0x58
 *   branch +0x390 -> +0x49c
 *   branch +0x414 -> +0x478
 *   branch +0x474 -> +0x49c
 *   branch +0x4c8 -> +0x5c4
 *   branch +0x52c -> +0x590
 *   branch +0x538 -> +0x55c
 *   branch +0x558 -> +0x5c4
 *   branch +0x58c -> +0x5c4
 *   branch +0x618 -> +0x634
 *   branch +0x630 -> +0x64c
 *   branch +0x634 -> +0x64c
 *   back edge +0x660 -> +0x5d4
 *   test +0x20 cmp r1, #0
 *   test +0x58 cmp r9, #7
 *   test +0x100 cmp r9, #6
 *   test +0x154 cmp r0, #0
 *   test +0x164 cmp r10, #1
 *   test +0x168 cmpeq r7, #0
 *   test +0x174 cmp r0, r4
 *   test +0x1a8 cmp r0, #0
 *   test +0x1b8 cmp r10, #1
 *   test +0x1bc cmpeq r7, #0
 *   test +0x1dc cmp r0, #0
 *   test +0x204 cmp r4, r0
 *   test +0x254 cmp r9, #4
 *   test +0x258 cmpne r9, #5
 *   test +0x25c cmpne r9, #6
 *   test +0x264 cmp r0, #0
 *   test +0x278 cmp r5, #1
 *   test +0x27c cmpeq r7, #0
 *   test +0x284 cmp r9, #0
 *   test +0x28c cmp r4, #100
 *   test +0x2e0 cmp r9, #1
 *   test +0x2e4 cmpne r9, #2
 *   test +0x37c cmp r9, #8
 *   test +0x388 cmp r0, #0
 *   test +0x38c cmpne r0, #2
 *   test +0x40c cmp r1, r0
 *   test +0x4c4 cmp r0, #0
 *   test +0x51c cmp r5, #1
 *   test +0x534 cmp r0, #0
 *   test +0x614 cmp r0, #0
 *   test +0x658 cmp r7, #8
 *   3 block transfer(s), 54 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022086b4; the literal pool and
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
extern u8 native_data_0222f050[];
extern void native_fn_02008be0(void);
extern void native_fn_0204a574(void);
extern u8 native_data_0222f094[];
extern void native_fn_0204a808(void);
extern void native_fn_020630b0(void);
extern void native_fn_020656c0(void);
extern void native_fn_02044424(void);
extern void native_fn_021dbd24(void);
extern void native_fn_021dbcbc(void);
extern void native_fn_0207c164(void);
extern void native_fn_021dbd30(void);
extern void native_fn_021dbcf0(void);
extern void native_fn_021dbd3c(void);
extern void native_fn_021dbd8c(void);
extern void native_fn_021dbe5c(void);
extern void native_fn_021dbe68(void);
extern void native_fn_02208670(void);
extern void native_fn_02208608(void);
extern u8 native_data_0222f098[];
extern u8 native_data_0222f09c[];
extern void native_fn_0204a154(void);
extern u8 native_data_0222f0a0[];
extern u8 native_data2_0222f050[];
extern void native_fn_0206259c(void);
extern u8 native_data_0222f0a4[];
extern void native_fn_0204a448(void);
extern void native_fn_021fe738(void);
extern void native_fn_02065818(void);


asm u32 native_ov001_022086b4 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #108
    bl native_fn_02207938
    ldr r8, [r0, #0x10]
    ldr r2, [r0, #0x8]
    add r1, r8, #512
    ldrsb r1, [r1, #86]
    ldr r2, [r2]
    cmp r1, #0
    ldr r1, [r2, #0x4]
    movne r10, #0
    str r1, [sp, #0x24]
    ldreq r10, [r0, #0x24]
    ldrb r2, [r8, #0x1fd]
    ldr r0, [sp, #0x24]
    mov r1, #1
    str r2, [sp, #0x14]
    bl native_fn_020852d0
    ldr r0, =native_data_0222f050
    mov r9, #0
    str r0, [sp, #0xc]
    add r11, sp, #44
ov001_022086b4_L58:
    cmp r9, #7
    mov r5, r10
    mov r7, #0
    beq ov001_022086b4_L364
    mov r0, r7
    mov r1, r11
    mov r2, #64
    mov r6, #1
    bl native_fn_02008be0
    ldr r0, [sp, #0xc]
    ldr r1, [sp, #0xc]
    ldrb r0, [r0]
    mov r3, r6
    str r0, [sp, #0x1c]
    ldr r0, [sp, #0xc]
    ldrb r0, [r0, #0x3]
    str r0, [sp, #0x18]
    ldrb r2, [r1, #0x1]
    ldr r0, [sp, #0xc]
    ldrb r1, [r1, #0x4]
    ldrb r0, [r0, #0x2]
    strh r2, [sp, #42]
    mov r2, #5
    strh r0, [sp, #40]
    str r1, [sp]
    mov r0, r6
    str r0, [sp, #0x4]
    mov r0, r7
    str r0, [sp, #0x8]
    mov r0, #26
    add r1, sp, #40
    bl native_fn_0204a574
    ldr r0, [sp, #0x1c]
    ldr r3, =native_data_0222f094
    strh r0, [sp, #40]
    mov r0, r7
    str r0, [sp]
    mov r0, #26
    add r1, sp, #40
    mov r2, r6
    bl native_fn_0204a808
    ldr r0, [sp, #0x1c]
    cmp r9, #6
    add r0, r0, #8
    strh r0, [sp, #40]
    addls pc, pc, r9, lsl #2
    b ov001_022086b4_L24c
    b ov001_022086b4_L130
    b ov001_022086b4_L180
    b ov001_022086b4_L1e8
    b ov001_022086b4_L210
    b ov001_022086b4_L220
    b ov001_022086b4_L230
    b ov001_022086b4_L240
ov001_022086b4_L130:
    ldr r0, [r8, #0x1e8]
    ldrb r0, [r0, #0xab]
    bl native_fn_020630b0
    str r0, [sp, #0x10]
    ldrb r4, [r8, #0x1fc]
    bl native_fn_020656c0
    mov r7, r0
    mov r0, #1073741824
    bl native_fn_02044424
    cmp r0, #0
    moveq r0, r6
    movne r0, #0
    and r7, r7, r0
    cmp r10, #1
    cmpeq r7, #0
    beq ov001_022086b4_L24c
    ldr r0, [sp, #0x10]
    cmp r0, r4
    moveq r6, #5
    b ov001_022086b4_L24c
ov001_022086b4_L180:
    mov r0, r8
    bl native_fn_021dbd24
    mov r4, r0
    mov r0, r8
    bl native_fn_021dbcbc
    str r0, [sp, #0x20]
    bl native_fn_020656c0
    mov r7, r0
    mov r0, #1073741824
    bl native_fn_02044424
    cmp r0, #0
    moveq r0, r6
    movne r0, #0
    and r7, r7, r0
    cmp r10, #1
    cmpeq r7, #0
    beq ov001_022086b4_L24c
    ldr r1, [sp, #0x20]
    mov r0, r4, lsl #16
    mov r1, r1, lsl #16
    mov r0, r0, asr #16
    mov r1, r1, asr #16
    bl native_fn_0207c164
    cmp r0, #0
    movne r6, #7
    b ov001_022086b4_L24c
ov001_022086b4_L1e8:
    mov r0, r8
    bl native_fn_021dbd30
    mov r4, r0
    mov r0, r8
    bl native_fn_021dbcf0
    str r0, [sp, #0x20]
    ldr r0, =0x00002710
    cmp r4, r0
    movge r5, r6
    b ov001_022086b4_L24c
ov001_022086b4_L210:
    mov r0, r8
    bl native_fn_021dbd3c
    mov r4, r0
    b ov001_022086b4_L24c
ov001_022086b4_L220:
    mov r0, r8
    bl native_fn_021dbd8c
    mov r4, r0
    b ov001_022086b4_L24c
ov001_022086b4_L230:
    mov r0, r8
    bl native_fn_021dbe5c
    mov r4, r0
    b ov001_022086b4_L24c
ov001_022086b4_L240:
    mov r0, r8
    bl native_fn_021dbe68
    mov r4, r0
ov001_022086b4_L24c:
    mov r0, r9
    bl native_fn_02208670
    cmp r9, #4
    cmpne r9, #5
    cmpne r9, #6
    bne ov001_022086b4_L278
    cmp r0, #0
    movlt r6, #7
    blt ov001_022086b4_L278
    movgt r6, #9
    movle r6, #1
ov001_022086b4_L278:
    cmp r5, #1
    cmpeq r7, #0
    beq ov001_022086b4_L294
    cmp r9, #0
    bne ov001_022086b4_L294
    cmp r4, #100
    bge ov001_022086b4_L364
ov001_022086b4_L294:
    mov r0, #0
    mov r1, r11
    mov r2, #64
    bl native_fn_02008be0
    ldr r0, [sp, #0x18]
    mov r1, r4
    stmia sp, {r0, r7}
    mov r0, r5
    mov r2, r11
    mov r3, #64
    bl native_fn_02208608
    mov r0, #0
    str r0, [sp]
    mov r2, r6
    mov r0, #26
    add r1, sp, #40
    mov r3, r11
    bl native_fn_0204a808
    ldrsh r0, [sp, #40]
    cmp r9, #1
    cmpne r9, #2
    add r0, r0, #32
    strh r0, [sp, #40]
    bne ov001_022086b4_L364
    mov r0, #0
    str r0, [sp]
    ldr r3, =native_data_0222f098
    mov r0, #26
    add r1, sp, #40
    mov r2, #1
    bl native_fn_0204a808
    ldrsh r3, [sp, #40]
    mov r1, r11
    mov r2, #64
    add r0, r3, r0
    strh r0, [sp, #40]
    mov r0, #0
    bl native_fn_02008be0
    ldr r0, [sp, #0x18]
    ldr r1, [sp, #0x20]
    stmia sp, {r0, r7}
    mov r0, r5
    mov r2, r11
    mov r3, #64
    bl native_fn_02208608
    mov r0, #0
    str r0, [sp]
    mov r0, #26
    add r1, sp, #40
    mov r2, #1
    mov r3, r11
    bl native_fn_0204a808
ov001_022086b4_L364:
    ldr r0, [sp, #0xc]
    add r0, r0, #5
    str r0, [sp, #0xc]
    add r0, r9, #1
    mov r0, r0, lsl #24
    mov r9, r0, asr #24
    cmp r9, #8
    blt ov001_022086b4_L58
    ldrb r0, [r8, #0x31e]
    cmp r0, #0
    cmpne r0, #2
    bne ov001_022086b4_L49c
    mov r1, #8
    mov r0, #80
    strh r1, [sp, #40]
    strh r0, [sp, #42]
    mov r2, #0
    str r2, [sp]
    mov r0, #1
    stmib sp, {r0, r2}
    add r1, sp, #40
    mov r0, #26
    mov r2, #5
    mov r3, #2
    bl native_fn_0204a574
    ldrsh r3, [sp, #40]
    mov r2, #0
    add r1, sp, #40
    add r0, r3, r0
    strh r0, [sp, #40]
    str r2, [sp]
    ldr r3, =native_data_0222f09c
    mov r0, #26
    mov r2, #1
    bl native_fn_0204a808
    ldrsh r1, [sp, #40]
    add r0, r1, r0
    strh r0, [sp, #40]
    ldr r0, [r8, #0x1e8]
    ldrb r0, [r0, #0xab]
    bl native_fn_020630b0
    ldrb r1, [r8, #0x1fc]
    cmp r1, r0
    add r1, sp, #40
    bhs ov001_022086b4_L478
    mov r0, #1
    str r0, [sp]
    str r0, [sp, #0x4]
    mov r0, #0
    str r0, [sp, #0x8]
    mov r0, #26
    mov r2, #5
    mov r3, #2
    bl native_fn_0204a574
    ldrsh r3, [sp, #40]
    mov r2, #7
    mov r1, #0
    add r0, r3, r0
    strh r0, [sp, #40]
    str r2, [sp]
    str r1, [sp, #0x4]
    ldr r2, [r8, #0x204]
    ldr r0, [r8, #0x200]
    add r1, sp, #40
    sub r3, r2, r0
    mov r0, #26
    mov r2, #1
    bl native_fn_0204a154
    b ov001_022086b4_L49c
ov001_022086b4_L478:
    ldrsh r0, [sp, #40]
    ldr r3, =native_data_0222f0a0
    mov r4, #0
    add r0, r0, #8
    strh r0, [sp, #40]
    mov r0, #26
    mov r2, #1
    str r4, [sp]
    bl native_fn_0204a808
ov001_022086b4_L49c:
    ldr r0, =native_data2_0222f050
    add r1, sp, #44
    ldrb r4, [r0, #0x25]
    mov r0, #0
    mov r2, #64
    bl native_fn_02008be0
    mov r0, #0
    strh r4, [sp, #40]
    strh r0, [sp, #42]
    bl native_fn_0206259c
    cmp r0, #0
    beq ov001_022086b4_L5c4
    mov r0, #19
    str r0, [sp]
    mov r3, #1
    str r3, [sp, #0x4]
    add r1, sp, #40
    str r3, [sp, #0x8]
    mov r0, #28
    mov r2, #5
    bl native_fn_0204a574
    ldrsh r3, [sp, #40]
    mov r2, #0
    add r1, sp, #40
    add r0, r3, r0
    strh r0, [sp, #40]
    str r2, [sp]
    ldr r3, =native_data_0222f0a4
    mov r0, #28
    mov r2, #1
    bl native_fn_0204a808
    ldrsh r1, [sp, #40]
    cmp r5, #1
    add r0, r1, r0
    strh r0, [sp, #40]
    add r1, sp, #40
    beq ov001_022086b4_L590
    ldr r0, [sp, #0x14]
    cmp r0, #0
    beq ov001_022086b4_L55c
    mov r4, #0
    str r4, [sp]
    ldr r3, [sp, #0x14]
    mov r0, #28
    mov r2, #1
    str r4, [sp, #0x4]
    bl native_fn_0204a448
    b ov001_022086b4_L5c4
ov001_022086b4_L55c:
    mov r0, #20
    str r0, [sp]
    mov r3, #1
    str r3, [sp, #0x4]
    mov r0, #0
    str r0, [sp, #0x8]
    mov r0, #28
    mov r2, #5
    bl native_fn_0204a574
    ldrsh r1, [sp, #40]
    add r0, r1, r0
    strh r0, [sp, #40]
    b ov001_022086b4_L5c4
ov001_022086b4_L590:
    mov r0, #42
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    mov r0, #0
    str r0, [sp, #0x8]
    mov r0, #28
    mov r2, #5
    mov r3, #7
    bl native_fn_0204a574
    ldrsh r1, [sp, #40]
    add r0, r1, r0
    strh r0, [sp, #40]
ov001_022086b4_L5c4:
    ldr r6, =native_data_0222f050
    mov r7, #0
    mov r4, #7
    mov r5, #6
ov001_022086b4_L5d4:
    ldr r0, [sp, #0x24]
    ldrb r3, [r6]
    ldrb r8, [r0, #0x1c]
    ldrb r2, [r6, #0x3]
    ldrb r1, [r0, #0x1d]
    ldrb r0, [r6, #0x1]
    add r3, r8, r3, asr #3
    add r2, r3, r2
    add r2, r2, #1
    add r0, r1, r0, asr #3
    mov r1, r2, lsl #24
    mov r2, r0, lsl #24
    mov r0, r7
    mov r8, r1, asr #24
    mov r9, r2, asr #24
    bl native_fn_02208670
    cmp r0, #0
    ble ov001_022086b4_L634
    mov r0, r5
    bl native_fn_021fe738
    mov r1, r8
    mov r2, r9
    bl native_fn_02065818
    b ov001_022086b4_L64c
ov001_022086b4_L634:
    bge ov001_022086b4_L64c
    mov r0, r4
    bl native_fn_021fe738
    mov r1, r8
    mov r2, r9
    bl native_fn_02065818
ov001_022086b4_L64c:
    add r0, r7, #1
    mov r0, r0, lsl #24
    mov r7, r0, asr #24
    cmp r7, #8
    add r6, r6, #5
    blt ov001_022086b4_L5d4
    add sp, sp, #108
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
