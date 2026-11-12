/* ov000 row 0x022008d8: 2780 bytes.
 *
 * What it does: 690 instructions and 74 call(s), then a 8-entry dispatch through an inline branch table at 0x02200920 (dispatch word at 0x02200918)
 *
 * Carrier: mwccarm asm with dcd data runs.
 * The measured extent is code plus data inside the function. The data
 * runs are emitted as data, not decoded as instructions; every
 * instruction, branch target, pool word and table entry is read from
 * the image.
 *
 * Unknowns: the field roles, the meaning of the table entries and every callee contract are not established by byte identity; the dispatch range and the table bounds are measured.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02062aa0(void);
extern void native_fn_02062ad0(void);
extern void native_fn_02216434(void);
extern void native_fn_0204a644(void);
extern void native_fn_02049008(void);
extern void native_fn_022014e8(void);
extern void native_fn_0221742c(void);
extern void native_fn_02049ad0(void);
extern void native_fn_02049f4c(void);
extern void native_fn_020602ec(void);
extern void native_fn_02065818(void);
extern void native_fn_0207b460(void);
extern void native_fn_02210f84(void);
extern void native_fn_0204a288(void);
extern void native_fn_02217f14(void);
extern void native_fn_0207b244(void);
extern void native_fn_02008be0(void);
extern void native_fn_022007d4(void);
extern void native_fn_0204a3ec(void);
extern void native_fn_0204a154(void);
extern void native_fn_0207afec(void);
extern void native_fn_02215d94(void);
extern void native_fn_02210f74(void);
extern void native_fn_02049ffc(void);
extern void native_fn_02062a50(void);
extern void native_fn_02062a88(void);
extern void native_fn_0204a4ac(void);
extern void native_fn_0204a574(void);
extern void native_fn_02217dbc(void);
extern void native_fn_02217f78(void);


asm u32 native_ov000_022008d8 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #188
    str r0, [sp, #0x10]
    bl native_fn_02062aa0
    str r0, [sp, #0x28]
    bl native_fn_02062ad0
    bl native_fn_02216434
    mov r1, #0
    mov r11, r0
    str r1, [sp, #0x20]
    mov r0, r1
    strh r0, [sp, #56]
    ldr r0, [sp, #0x20]
    strh r0, [sp, #58]
    ldr r0, [sp, #0x10]
    cmp r0, #7
    addls pc, pc, r0, lsl #2
    b L_02201330
    dcd 0xea000282
    dcd 0xea000005
    dcd 0xea000280
    dcd 0xea00009c
    dcd 0xea00027e
    dcd 0xea000124
    dcd 0xea00027c
    dcd 0xea00027b
    ldr r0, [sp, #0x20]
    add r1, sp, #56
    strh r0, [sp, #56]
    ldrh r2, [r11, #2]
    mov r0, #1
    ldr r5, [pc, #0xa44]
    str r2, [sp]
    str r0, [sp, #0x4]
    str r0, [sp, #0x8]
    ldrb r2, [r11]
    ldrb r3, [r11, #0x1]
    mov r0, #23
    bl native_fn_0204a644
    ldrsh r3, [sp, #56]
    mov r1, #5
    mov r2, r1
    add r3, r3, r0
    strh r3, [sp, #56]
    mov r4, #0
    mov r0, r5
    mov r3, #7
    str r4, [sp]
    bl native_fn_02049008
    mov r1, #1
    str r1, [sp]
    mov r0, r5
    mov r1, #12
    mov r2, #6
    mov r3, #8
    bl native_fn_02049008
    ldrh r0, [r5, #12]
    mov r9, r4
    sub r2, r0, #1
    cmp r2, #0
    ble L_02200a34
    ldr r10, [pc, #0x9d0]
    mov r4, #1
    mov r8, r10
    mov r6, #2
    mov r7, r9
L_022009e0:
    add r0, r8, r9, lsl #2
    ldr r1, [r0, #0x5f8]
    strb r7, [r10, #0x5eb]
    ldrb r0, [r10, #0x5dc]
    cmp r0, #0
    streqb r6, [r10, #0x5eb]
    beq L_02200a14
    ldrb r0, [r1, #0x33]
    cmp r0, #0
    strneb r4, [r10, #0x5eb]
    bne L_02200a14
    and r0, r9, #255
    bl native_fn_022014e8
L_02200a14:
    ldrh r0, [r5, #12]
    add r1, r9, #1
    mov r1, r1, lsl #24
    sub r2, r0, #1
    cmp r2, r1, asr #24
    add r10, r10, #1
    mov r9, r1, asr #24
    bgt L_022009e0
L_02200a34:
    cmp r2, #0
    mov r7, #0
    ble L_02200b74
    ldr r4, [pc, #0x95c]
    mov r6, #5
    str r4, [sp, #0x2c]
L_02200a4c:
    ldrb r0, [r4, #0x5eb]
    cmp r0, #0
    moveq r9, #1
    ldr r0, [sp, #0x28]
    movne r9, #3
    cmp r7, r0
    bge L_02200a74
    mov r0, #7
    bl native_fn_0221742c
    b L_02200a7c
L_02200a74:
    mov r0, #8
    bl native_fn_0221742c
L_02200a7c:
    mov r10, r0
    ldr r0, [sp, #0x2c]
    add r0, r0, r7, lsl #2
    ldr r8, [r0, #0x5f8]
    add r0, r7, #5
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    mov r11, r0
    bl native_fn_02049f4c
    mov r0, #24
    strh r0, [sp, #56]
    cmp r8, #0
    beq L_02200ad0
    mov r0, #0
    stmia sp, {r0, r9}
    ldrsh r1, [r8, #24]
    ldrsh r3, [sp, #56]
    ldr r0, [r11]
    mov r2, r8
    bl native_fn_020602ec
L_02200ad0:
    mov r2, r6, lsl #24
    mov r0, r10
    mov r1, #4
    mov r2, r2, asr #24
    bl native_fn_02065818
    ldrsh r0, [r8, #24]
    ldrb r1, [r8, #0x1a]
    add r2, r8, #122
    add r3, sp, #60
    bl native_fn_0207b460
    mov r0, r8
    add r1, sp, #60
    bl native_fn_02210f84
    mov r1, #16
    strh r1, [sp, #56]
    ldrsh r2, [r8, #38]
    add r1, r7, #12
    mov r1, r1, lsl #24
    str r2, [sp]
    str r0, [sp, #0x4]
    mov r0, r1, asr #24
    mov r1, #4
    str r1, [sp, #0x8]
    mov r1, #1
    str r1, [sp, #0xc]
    add r1, sp, #56
    mov r2, r9
    mov r3, r9
    bl native_fn_0204a288
    ldrsh r1, [sp, #56]
    add r4, r4, #1
    add r6, r6, #2
    add r0, r1, r0
    strh r0, [sp, #56]
    add r0, r7, #1
    mov r1, r0, lsl #24
    ldrh r0, [r5, #12]
    mov r7, r1, asr #24
    sub r2, r0, #1
    cmp r2, r1, asr #24
    bgt L_02200a4c
L_02200b74:
    add r0, r0, #4
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    mov r1, #5
    mov r2, #2
    mov r3, #34
    bl native_fn_02217f14
    mov r1, #28
    ldr r2, [pc, #0x808]
    str r1, [sp, #0x20]
    str r0, [r2, #0x5f4]
    b L_02201330
    ldr r5, [pc, #0x7fc]
    ldr r8, [pc, #0x7f4]
    ldrh r0, [r5, #12]
    ldr r1, [r8, #0x8]
    ldr r9, [sp, #0x20]
    cmp r0, #0
    and r0, r1, #255
    str r0, [sp, #0x24]
    ldr r10, [r8, #0x2d8]
    ble L_02200c40
    ldr r0, [sp, #0x24]
    add r4, sp, #60
    add r6, r8, r0, lsl #7
L_02200bd8:
    add r0, r6, r9, lsl #2
    ldr r0, [r0, #0x2dc]
    mov r3, r4
    mov r0, r0, lsl #16
    mov r7, r0, lsr #16
    mov r0, #0
    strb r0, [r8, #0x5eb]
    ldrsh r0, [r10, #24]
    ldrb r1, [r10, #0x1a]
    add r2, r10, #122
    bl native_fn_0207b460
    ldrsh r1, [r10, #38]
    mov r0, r7
    mov r2, r4
    bl native_fn_0207b244
    ldrsh r1, [r10, #38]
    cmp r1, r0
    movlt r0, #1
    strltb r0, [r8, #0x5eb]
    add r0, r9, #1
    mov r0, r0, lsl #24
    ldrh r1, [r5, #12]
    add r8, r8, #1
    mov r9, r0, asr #24
    cmp r1, r0, asr #24
    bgt L_02200bd8
L_02200c40:
    mov r1, #5
    mov r4, #0
    mov r0, r5
    mov r2, r1
    mov r3, #7
    str r4, [sp]
    bl native_fn_02049008
    mov r3, #1
    str r3, [sp]
    mov r0, r5
    mov r1, #12
    mov r2, #6
    mov r3, #8
    bl native_fn_02049008
    mov r0, r4
    strh r0, [sp, #56]
    strh r0, [sp, #58]
    ldrh r2, [r11, #2]
    mov r1, #1
    mov r0, #23
    str r2, [sp]
    str r1, [sp, #0x4]
    str r1, [sp, #0x8]
    ldrb r2, [r11]
    ldrb r3, [r11, #0x1]
    add r1, sp, #56
    bl native_fn_0204a644
    ldrsh r3, [sp, #56]
    add r1, sp, #124
    mov r2, #64
    add r0, r3, r0
    strh r0, [sp, #56]
    mov r0, r4
    bl native_fn_02008be0
    ldr r1, [sp, #0x24]
    mov r0, r10
    bl native_fn_022007d4
    ldrh r0, [r5, #12]
    mov r9, r4
    cmp r0, #0
    ble L_02201330
    ldr r7, [pc, #0x6b8]
    ldr r0, [sp, #0x24]
    add r11, sp, #60
    add r6, r7, r0, lsl #7
L_02200cf4:
    ldrb r0, [r7, #0x5eb]
    add r2, r10, #122
    mov r3, r11
    cmp r0, #0
    add r0, r6, r9, lsl #2
    ldr r1, [r0, #0x2dc]
    moveq r8, #1
    mov r1, r1, lsl #16
    mov r4, r1, lsr #16
    ldrsh r0, [r10, #24]
    ldrb r1, [r10, #0x1a]
    movne r8, #3
    bl native_fn_0207b460
    ldrsh r1, [r10, #38]
    mov r0, r4
    mov r2, r11
    bl native_fn_0207b244
    mov r3, r4
    mov r1, #16
    mov r4, r0
    add r0, r9, #5
    and r8, r8, #255
    strh r1, [sp, #56]
    mov r1, #1
    mov r0, r0, lsl #24
    str r1, [sp]
    mov r0, r0, asr #24
    add r1, sp, #56
    mov r2, r8
    bl native_fn_0204a3ec
    mov r0, #56
    strh r0, [sp, #56]
    mov r0, #4
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    add r0, r9, #12
    mov r0, r0, lsl #24
    mov r2, r8
    mov r3, r4
    mov r0, r0, asr #24
    add r1, sp, #56
    bl native_fn_0204a154
    ldrsh r2, [sp, #56]
    add r1, r9, #1
    add r7, r7, #1
    add r0, r2, r0
    strh r0, [sp, #56]
    mov r0, r1, lsl #24
    ldrh r1, [r5, #12]
    mov r9, r0, asr #24
    cmp r1, r0, asr #24
    bgt L_02200cf4
    b L_02201330
    ldr r0, [pc, #0x5d0]
    ldr r1, [pc, #0x5d4]
    ldr r3, [r0, #0x8]
    ldr r2, [r0, #0xf8]
    and r7, r3, #255
    ldr r4, [r0, #0x2d8]
    and r6, r2, #255
    add r0, r1, r7, lsl #7
    ldr r1, [r0, r6, lsl #2]
    ldrsh r0, [r4, #24]
    mov r5, r1, lsl #16
    mov r8, r5, lsr #16
    ldrb r1, [r4, #0x1a]
    add r3, sp, #60
    add r2, r4, #122
    ldr r5, [pc, #0x5a0]
    bl native_fn_0207b460
    ldrsh r1, [r4, #38]
    add r2, sp, #60
    mov r0, r8
    bl native_fn_0207b244
    mov r4, r0
    ldr r0, [pc, #0x578]
    mov r1, r7
    ldr r0, [r0, #0x2d8]
    bl native_fn_022007d4
    mov r0, #16
    strh r0, [sp, #56]
    mov r2, #1
    mov r3, r8
    mov r0, #2
    add r1, sp, #56
    str r2, [sp]
    bl native_fn_0204a3ec
    mov r0, #176
    strh r0, [sp, #56]
    mov r0, #4
    str r0, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    mov r3, r4
    mov r0, #2
    add r1, sp, #56
    mov r2, #1
    bl native_fn_0204a154
    ldr r0, [pc, #0x51c]
    ldrb r0, [r0, #0x5e8]
    cmp r0, #0
    bne L_02201118
    mov r0, #0
    strh r0, [sp, #56]
    strh r0, [sp, #58]
    ldrh r2, [r11, #2]
    mov r0, #1
    add r1, sp, #56
    str r2, [sp]
    str r0, [sp, #0x4]
    str r0, [sp, #0x8]
    ldrb r2, [r11]
    ldrb r3, [r11, #0x1]
    mov r0, #23
    bl native_fn_0204a644
    ldrsh r3, [sp, #56]
    mov r1, #5
    mov r2, r1
    add r3, r3, r0
    strh r3, [sp, #56]
    mov r3, #0
    str r3, [sp]
    mov r0, r5
    mov r3, #7
    bl native_fn_02049008
    mov r0, #1
    str r0, [sp]
    mov r0, r5
    mov r1, #12
    mov r2, #6
    mov r3, #8
    bl native_fn_02049008
    ldrh r1, [r5, #12]
    mov r9, #0
    cmp r1, #0
    ble L_02200fbc
    ldr r8, [pc, #0x484]
    mov r11, #1
    add r0, r8, r7, lsl #7
    mov r7, r8
    add r6, r0, r6, lsl #2
    mov r4, r9
L_02200f30:
    add r0, r7, r9, lsl #2
    ldr r1, [r6, #0x2dc]
    ldr r10, [r0, #0x5f8]
    mov r0, r1, lsl #16
    mov r0, r0, lsr #16
    strb r4, [r8, #0x5eb]
    bl native_fn_0207afec
    ldrh r0, [r0, #8]
    mov r0, r0, lsl #20
    mov r0, r0, lsr #28
    cmp r0, #2
    ldrb r0, [r10, #0x33]
    bne L_02200f70
    cmp r0, #0
    strneb r11, [r8, #0x5eb]
    b L_02200f7c
L_02200f70:
    cmp r0, #0
    moveq r0, #1
    streqb r0, [r8, #0x5eb]
L_02200f7c:
    and r0, r9, #255
    bl native_fn_02215d94
    mov r1, r0
    mov r0, r10
    bl native_fn_02210f74
    ldrsh r1, [r10, #36]
    cmp r1, r0
    movge r0, #1
    strgeb r0, [r8, #0x5eb]
    add r0, r9, #1
    mov r0, r0, lsl #24
    ldrh r1, [r5, #12]
    mov r9, r0, asr #24
    add r8, r8, #1
    cmp r1, r0, asr #24
    bgt L_02200f30
L_02200fbc:
    cmp r1, #0
    mov r9, #0
    ble L_02201330
    ldr r6, [pc, #0x3d4]
    mov r7, #10
    str r6, [sp, #0x30]
L_02200fd4:
    ldr r0, [sp, #0x28]
    cmp r9, r0
    ldr r0, [sp, #0x30]
    add r0, r0, r9, lsl #2
    ldr r10, [r0, #0x5f8]
    bge L_02200ff8
    mov r0, #7
    bl native_fn_0221742c
    b L_02201000
L_02200ff8:
    mov r0, #8
    bl native_fn_0221742c
L_02201000:
    mov r11, r0
    ldrb r0, [r6, #0x5eb]
    cmp r0, #0
    movne r8, #3
    movne r4, r8
    bne L_02201044
    and r0, r9, #255
    mov r8, #1
    bl native_fn_02215d94
    mov r1, r0
    mov r0, r10
    bl native_fn_02210f74
    ldrsh r1, [r10, #36]
    add r1, r1, r1, lsl #2
    cmp r1, r0
    movlt r4, #7
    movge r4, r8
L_02201044:
    add r0, r9, #5
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    str r0, [sp, #0x34]
    bl native_fn_02049f4c
    mov r0, #24
    strh r0, [sp, #56]
    cmp r10, #0
    beq L_0220108c
    mov r0, #0
    stmia sp, {r0, r8}
    ldr r0, [sp, #0x34]
    ldrsh r1, [r10, #24]
    ldrsh r3, [sp, #56]
    ldr r0, [r0]
    mov r2, r10
    bl native_fn_020602ec
L_0220108c:
    mov r2, r7, lsl #24
    mov r0, r11
    mov r1, #4
    mov r2, r2, asr #24
    bl native_fn_02065818
    mov r0, #16
    strh r0, [sp, #56]
    and r0, r9, #255
    bl native_fn_02215d94
    mov r1, r0
    mov r0, r10
    bl native_fn_02210f74
    ldrsh r1, [r10, #36]
    mov r2, r4
    mov r3, r8
    str r1, [sp]
    str r0, [sp, #0x4]
    mov r0, #4
    str r0, [sp, #0x8]
    mov r0, #1
    str r0, [sp, #0xc]
    add r0, r9, #12
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    add r1, sp, #56
    bl native_fn_0204a288
    add r0, r9, #1
    mov r0, r0, lsl #24
    ldrh r1, [r5, #12]
    add r6, r6, #1
    add r7, r7, #2
    mov r9, r0, asr #24
    cmp r1, r0, asr #24
    bgt L_02200fd4
    b L_02201330
L_02201118:
    bl native_fn_02062aa0
    mov r4, r0, lsl #24
    bl native_fn_02062ad0
    add r0, r0, r4, asr #24
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    str r0, [sp, #0x1c]
    mov r0, r0, lsl #1
    rsb r2, r0, #23
    ldr r0, [pc, #0x260]
    mov r1, #0
    strb r1, [r0, #0x5eb]
    mov r0, #28
    and r9, r2, #255
    bl native_fn_02049ad0
    ldr r0, [r0]
    ldr r0, [r0, #0x4]
    bl native_fn_02049ffc
    ldr r0, [sp, #0x1c]
    mov r7, #0
    cmp r0, #0
    ble L_02201280
    mov r11, r7
L_02201174:
    cmp r7, r4, asr #24
    bge L_02201188
    mov r0, r7
    bl native_fn_02062a50
    b L_02201190
L_02201188:
    sub r0, r7, r4, asr #24
    bl native_fn_02062a88
L_02201190:
    mov r10, r0
    ldrsh r8, [r10, #36]
    and r0, r7, #255
    bl native_fn_02215d94
    mov r1, r0
    mov r0, r10
    bl native_fn_02210f74
    str r0, [sp, #0x14]
    cmp r8, r0
    bge L_022011c4
    ldrb r0, [r10, #0x33]
    cmp r0, #0
    beq L_022011d4
L_022011c4:
    mov r6, #3
    mov r0, r6
    str r0, [sp, #0x18]
    b L_02201200
L_022011d4:
    ldr r0, [pc, #0x1c8]
    mov r1, #1
    strb r1, [r0, #0x5eb]
    mov r0, r1
    str r0, [sp, #0x18]
    mov r6, r1
    ldr r0, [sp, #0x14]
    add r1, r8, r8, lsl #2
    cmp r1, r0
    movle r0, #7
    strle r0, [sp, #0x18]
L_02201200:
    mov r0, #24
    strh r0, [sp, #56]
    strh r11, [sp, #58]
    str r6, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    mov r1, r10
    mov r0, #27
    mov r2, #0
    add r3, sp, #56
    bl native_fn_0204a4ac
    mov r0, #0
    strh r0, [sp, #56]
    ldr r0, [sp, #0x14]
    str r8, [sp]
    str r0, [sp, #0x4]
    mov r0, #4
    str r0, [sp, #0x8]
    mov r0, #0
    str r0, [sp, #0xc]
    ldr r2, [sp, #0x18]
    mov r3, r6
    mov r0, #28
    add r1, sp, #56
    bl native_fn_0204a288
    add r0, r7, #1
    mov r1, r0, lsl #24
    ldr r0, [sp, #0x1c]
    add r11, r11, #16
    cmp r0, r1, asr #24
    mov r7, r1, asr #24
    bgt L_02201174
L_02201280:
    ldr r0, [sp, #0x1c]
    mov r10, #0
    cmp r0, #0
    ble L_022012e4
    mov r7, #8
    mov r8, #7
    mov r6, #4
L_0220129c:
    cmp r10, r4, asr #24
    bge L_022012b0
    mov r0, r8
    bl native_fn_0221742c
    b L_022012b8
L_022012b0:
    mov r0, r7
    bl native_fn_0221742c
L_022012b8:
    mov r2, r9, lsl #24
    mov r1, r6
    mov r2, r2, asr #24
    bl native_fn_02065818
    add r0, r10, #1
    mov r1, r0, lsl #24
    ldr r0, [sp, #0x1c]
    add r9, r9, #2
    cmp r0, r1, asr #24
    mov r10, r1, asr #24
    bgt L_0220129c
L_022012e4:
    ldr r0, [pc, #0xb8]
    mov r2, #16
    ldrb r0, [r0, #0x5eb]
    mov r1, #0
    mov r4, #1
    cmp r0, #0
    movne r3, #1
    strh r1, [sp, #58]
    strh r2, [sp, #56]
    mov r1, #26
    mov r0, #5
    str r1, [sp]
    moveq r3, #3
    str r3, [sp, #0x4]
    add r1, sp, #56
    mov r2, r0
    mov r3, #2
    str r4, [sp, #0x8]
    bl native_fn_0204a574
L_02201330:
    bl native_fn_02217dbc
    ldr r0, [sp, #0x10]
    cmp r0, #1
    beq L_0220136c
    cmp r0, #7
    addne sp, sp, #188
    ldmneia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    ldr r0, [pc, #0x50]
    ldr r0, [r0, #0x4]
    cmp r0, #1
    addne sp, sp, #188
    ldmneia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r0, #28
    ldr r5, [pc, #0x34]
    str r0, [sp, #0x20]
L_0220136c:
    ldrh r0, [r5, #12]
    ldr r2, [pc, #0x2c]
    ldr r3, [sp, #0x20]
    sub r0, r0, #1
    mov r0, r0, lsl #24
    ldr r2, [r2, #0x5f4]
    mov r1, r5
    mov r0, r0, asr #24
    bl native_fn_02217f78
    ldr r1, [pc, #0xc]
    strb r0, [r1, #0x5ea]
    add sp, sp, #188
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    dcd 0x02237780
    dcd 0x02237778
    dcd 0x02237870
    dcd 0x02237a54
    dcd 0x02237960
}
