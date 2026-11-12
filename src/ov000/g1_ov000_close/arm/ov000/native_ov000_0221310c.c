/* ov000 row 0x0221310c: 1612 bytes.
 *
 * What it does: 402 instructions and 37 call(s), then a 18-entry dispatch through an inline branch table at 0x0221314c (dispatch word at 0x02213144)
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

extern void native_fn_02213e10(void);
extern void native_fn_02213e7c(void);
extern void native_fn_02212e1c(void);
extern void native_fn_02213ee4(void);
extern void native_fn_020413fc(void);
extern void native_fn_021dfbd4(void);
extern void native_fn_02029964(void);
extern void native_fn_021dfca4(void);
extern void native_fn_02029834(void);
extern void native_fn_021dfd48(void);


asm u32 native_ov000_0221310c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r8, #0
    mov r11, #2
    mov r10, #4
    ldr r9, [pc, #0x630]
    mov r4, r8
    mov r5, #6
    mov r6, r11
    mov r7, r10
L_02213130:
    ldrb r0, [r9, #0x105]
    cmp r0, #0
    beq L_02213740
    ldrb r0, [r9, #0x106]
    cmp r0, #17
    addls pc, pc, r0, lsl #2
    b L_0221365c
    dcd 0xea000010
    dcd 0xea000036
    dcd 0xea000056
    dcd 0xea00007e
    dcd 0xea0000a0
    dcd 0xea0000d1
    dcd 0xea0000d9
    dcd 0xea0000f3
    dcd 0xea000008
    dcd 0xea000007
    dcd 0xea000006
    dcd 0xea000005
    dcd 0xea000004
    dcd 0xea000003
    dcd 0xea000002
    dcd 0xea000001
    dcd 0xea000000
    dcd 0xea00012a
    ldrb r0, [r9, #0x107]
    cmp r0, #1
    bne L_022131b4
    mov r0, r8
    mov r1, #1
    bl native_fn_02213e10
    strb r7, [r9, #0x107]
    b L_0221365c
L_022131b4:
    cmp r0, #4
    bne L_022131e0
    ldr r1, [r9, #0x60]
    ldr r0, [r1]
    ldr r1, [r1, #0x8]
    ldrh r1, [r1, #4]
    mov r1, r1, lsl #12
    sub r1, r1, #1
    cmp r0, r1
    strgeb r6, [r9, #0x107]
    b L_0221365c
L_022131e0:
    cmp r0, #2
    bne L_02213218
    mov r0, r8
    mov r1, #1
    bl native_fn_02213e10
    cmp r0, #0
    beq L_0221365c
    ldr r0, [r9, #0x60]
    ldr r1, [r0, #0x8]
    ldrh r1, [r1, #4]
    mov r1, r1, lsl #12
    sub r1, r1, #1
    str r1, [r0]
    b L_0221365c
L_02213218:
    cmp r0, #5
    streqb r5, [r9, #0x107]
    beq L_0221365c
    cmp r0, #6
    streqb r4, [r9, #0x107]
    b L_0221365c
    ldrb r0, [r9, #0x107]
    cmp r0, #1
    bne L_0221325c
    mov r0, r8
    mov r1, #1
    bl native_fn_02213e10
    mov r0, r8
    mov r1, #1
    bl native_fn_02213e7c
    strb r10, [r9, #0x107]
    b L_0221365c
L_0221325c:
    cmp r0, #4
    bne L_02213294
    ldr r1, [r9, #0x60]
    ldr r0, [r1]
    ldr r1, [r1, #0x8]
    ldrh r1, [r1, #4]
    mov r1, r1, lsl #12
    sub r1, r1, #1
    cmp r0, r1
    blt L_0221365c
    mov r0, r8
    bl native_fn_02212e1c
    strb r11, [r9, #0x107]
    b L_0221365c
L_02213294:
    cmp r0, #5
    moveq r0, #6
    streqb r0, [r9, #0x107]
    beq L_0221365c
    cmp r0, #6
    moveq r0, #0
    streqb r0, [r9, #0x107]
    b L_0221365c
    ldrb r0, [r9, #0x107]
    cmp r0, #1
    bne L_022132d8
    mov r0, r8
    mov r1, #1
    bl native_fn_02213e10
    mov r0, #4
    strb r0, [r9, #0x107]
    b L_0221365c
L_022132d8:
    cmp r0, #4
    bne L_02213308
    ldr r1, [r9, #0x60]
    ldr r0, [r1]
    ldr r1, [r1, #0x8]
    ldrh r1, [r1, #4]
    mov r1, r1, lsl #12
    sub r1, r1, #1
    cmp r0, r1
    movge r0, #2
    strgeb r0, [r9, #0x107]
    b L_0221365c
L_02213308:
    cmp r0, #2
    bne L_02213338
    mov r0, r8
    mov r1, #1
    bl native_fn_02213e10
    ldr r0, [r9, #0x60]
    ldr r1, [r0, #0x8]
    ldrh r1, [r1, #4]
    mov r1, r1, lsl #12
    sub r1, r1, #1
    str r1, [r0]
    b L_0221365c
L_02213338:
    cmp r0, #5
    moveq r0, #6
    streqb r0, [r9, #0x107]
    beq L_0221365c
    cmp r0, #6
    moveq r0, #0
    streqb r0, [r9, #0x107]
    b L_0221365c
    ldrb r0, [r9, #0x107]
    cmp r0, #1
    bne L_02213388
    mov r0, r8
    mov r1, #1
    bl native_fn_02213e10
    mov r0, r8
    mov r1, #1
    bl native_fn_02213e7c
    mov r0, #4
    strb r0, [r9, #0x107]
    b L_0221365c
L_02213388:
    cmp r0, #4
    bne L_022133c4
    ldr r1, [r9, #0x60]
    ldr r0, [r1]
    ldr r1, [r1, #0x8]
    ldrh r1, [r1, #4]
    mov r1, r1, lsl #12
    sub r1, r1, #1
    cmp r0, r1
    blt L_0221365c
    mov r0, r8
    bl native_fn_02212e1c
    mov r0, #2
    strb r0, [r9, #0x107]
    b L_0221365c
L_022133c4:
    cmp r0, #5
    moveq r0, #6
    streqb r0, [r9, #0x107]
    beq L_0221365c
    cmp r0, #6
    moveq r0, #0
    streqb r0, [r9, #0x107]
    b L_0221365c
    ldrb r0, [r9, #0x107]
    cmp r0, #1
    bne L_02213414
    mov r0, r8
    mov r1, #1
    bl native_fn_02213e10
    mov r0, r8
    mov r1, #1
    bl native_fn_02213e7c
    mov r0, #4
    strb r0, [r9, #0x107]
    b L_0221365c
L_02213414:
    cmp r0, #4
    bne L_02213450
    ldr r1, [r9, #0x60]
    ldr r0, [r1]
    ldr r1, [r1, #0x8]
    ldrh r1, [r1, #4]
    mov r1, r1, lsl #12
    sub r1, r1, #1
    cmp r0, r1
    blt L_0221365c
    mov r0, r8
    bl native_fn_02212e1c
    mov r0, #2
    strb r0, [r9, #0x107]
    b L_0221365c
L_02213450:
    cmp r0, #5
    bne L_0221347c
    mov r0, r8
    mov r1, #2
    bl native_fn_02213e10
    mov r0, r8
    mov r1, #2
    bl native_fn_02213e7c
    mov r0, #6
    strb r0, [r9, #0x107]
    b L_0221365c
L_0221347c:
    cmp r0, #6
    bne L_0221365c
    ldr r1, [r9, #0x60]
    ldr r0, [r1]
    ldr r1, [r1, #0x8]
    ldrh r1, [r1, #4]
    mov r1, r1, lsl #12
    sub r1, r1, #1
    cmp r0, r1
    movge r0, #0
    strgeb r0, [r9, #0x107]
    b L_0221365c
    ldrb r0, [r9, #0x107]
    cmp r0, #5
    moveq r0, #6
    streqb r0, [r9, #0x107]
    beq L_0221365c
    cmp r0, #6
    moveq r0, #0
    streqb r0, [r9, #0x107]
    b L_0221365c
    ldrb r0, [r9, #0x107]
    cmp r0, #1
    bne L_022134f4
    mov r0, r8
    mov r1, #1
    bl native_fn_02213e7c
    mov r0, #4
    strb r0, [r9, #0x107]
    b L_0221365c
L_022134f4:
    cmp r0, #4
    beq L_0221365c
    cmp r0, #2
    bne L_0221365c
    mov r0, r8
    mov r1, #1
    bl native_fn_02213e7c
    cmp r0, #0
    beq L_0221365c
    ldr r0, [r9, #0x6c]
    ldr r1, [r0, #0x8]
    ldrh r1, [r1, #4]
    mov r1, r1, lsl #12
    sub r1, r1, #1
    str r1, [r0]
    mov r0, #4
    strb r0, [r9, #0x107]
    b L_0221365c
    ldrb r0, [r9, #0x107]
    cmp r0, #1
    bne L_02213578
    mov r0, r8
    mov r1, #1
    bl native_fn_02213e10
    mov r0, r8
    mov r1, #1
    bl native_fn_02213e7c
    mov r0, r8
    mov r1, #1
    bl native_fn_02213ee4
    mov r0, #4
    strb r0, [r9, #0x107]
    b L_0221365c
L_02213578:
    cmp r0, #4
    bne L_022135a8
    ldr r1, [r9, #0x60]
    ldr r0, [r1]
    ldr r1, [r1, #0x8]
    ldrh r1, [r1, #4]
    mov r1, r1, lsl #12
    sub r1, r1, #1
    cmp r0, r1
    movge r0, #2
    strgeb r0, [r9, #0x107]
    b L_0221365c
L_022135a8:
    cmp r0, #2
    bne L_02213620
    mov r0, r8
    mov r1, #1
    bl native_fn_02213e10
    mov r0, r8
    mov r1, #1
    bl native_fn_02213e7c
    mov r0, r8
    mov r1, #1
    bl native_fn_02213ee4
    ldr r0, [r9, #0x60]
    ldr r1, [r0, #0x8]
    ldrh r1, [r1, #4]
    mov r1, r1, lsl #12
    sub r1, r1, #1
    str r1, [r0]
    ldr r0, [r9, #0x6c]
    ldr r1, [r0, #0x8]
    ldrh r1, [r1, #4]
    mov r1, r1, lsl #12
    sub r1, r1, #1
    str r1, [r0]
    ldr r0, [r9, #0x68]
    ldr r1, [r0, #0x8]
    ldrh r1, [r1, #4]
    mov r1, r1, lsl #12
    sub r1, r1, #1
    str r1, [r0]
    b L_0221365c
L_02213620:
    cmp r0, #5
    moveq r0, #6
    streqb r0, [r9, #0x107]
    beq L_0221365c
    cmp r0, #6
    moveq r0, #0
    streqb r0, [r9, #0x107]
    b L_0221365c
    ldrb r0, [r9, #0x107]
    cmp r0, #1
    bne L_0221365c
    mov r0, r8
    bl native_fn_02212e1c
    mov r0, #2
    strb r0, [r9, #0x107]
L_0221365c:
    ldrb r0, [r9, #0x102]
    cmp r0, #0
    beq L_022136a8
    mov r0, r9
    mov r1, #4096
    mov r2, #0
    bl native_fn_020413fc
    ldrb r0, [r9, #0x102]
    bl native_fn_021dfbd4
    cmp r0, #0
    blt L_022136a8
    ldr r2, [r9, #0x60]
    ldr r3, [r2, #0x8]
    ldr r1, [r2]
    ldrh r3, [r3, #4]
    mov r3, r3, lsl #12
    sub r3, r3, #1
    cmp r1, r3
    strge r0, [r2]
L_022136a8:
    ldrb r0, [r9, #0x103]
    cmp r0, #0
    beq L_022136f4
    mov r0, r9
    mov r1, #4096
    mov r2, #0
    bl native_fn_02029964
    ldrb r0, [r9, #0x103]
    bl native_fn_021dfca4
    cmp r0, #0
    blt L_022136f4
    ldr r2, [r9, #0x6c]
    ldr r3, [r2, #0x8]
    ldr r1, [r2]
    ldrh r3, [r3, #4]
    mov r3, r3, lsl #12
    sub r3, r3, #1
    cmp r1, r3
    strge r0, [r2]
L_022136f4:
    ldrb r0, [r9, #0x104]
    cmp r0, #0
    beq L_02213740
    mov r0, r9
    mov r1, #4096
    mov r2, #0
    bl native_fn_02029834
    ldrb r0, [r9, #0x104]
    bl native_fn_021dfd48
    cmp r0, #0
    blt L_02213740
    ldr r2, [r9, #0x68]
    ldr r3, [r2, #0x8]
    ldr r1, [r2]
    ldrh r3, [r3, #4]
    mov r3, r3, lsl #12
    sub r3, r3, #1
    cmp r1, r3
    strge r0, [r2]
L_02213740:
    add r9, r9, #268
    add r8, r8, #1
    cmp r8, #16
    blt L_02213130
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    dcd 0x02243e3c
}
