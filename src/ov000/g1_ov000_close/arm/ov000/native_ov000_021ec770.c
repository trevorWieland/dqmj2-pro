/* ov000 row 0x021ec770: 820 bytes.
 *
 * What it does: 203 instructions and 26 call(s), then a 9-entry dispatch through an inline branch table at 0x021ec7a0 (dispatch word at 0x021ec798)
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

extern void native_fn_0202a634(void);
extern void native_fn_021ecf88(void);
extern void native_fn_02062520(void);
extern void native_fn_021ecaa4(void);
extern void native_fn_02041538(void);
extern void native_fn_021ed560(void);
extern void native_fn_021ed6bc(void);
extern void native_fn_021ed1e0(void);
extern void native_fn_021ed368(void);
extern void native_fn_021ee1b0(void);
extern void native_fn_021ef11c(void);
extern void native_fn_021ecff0(void);
extern void native_fn_021edd04(void);
extern void native_fn_021ee458(void);
extern void native_fn_021ef0b0(void);
extern void native_fn_021ed404(void);
extern void native_fn_020c4318(void);
extern void native_fn_021ec748(void);
extern void native_fn_021ec718(void);
extern void native_fn_02063b28(void);
extern void native_fn_02062074(void);
extern void native_fn_02041814(void);


asm u32 native_ov000_021ec770 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, lr}
    sub sp, sp, #4
    mov r4, #2
    bl native_fn_0202a634
    ldr r1, [pc, #0x314]
    mov r5, r0
    ldr r12, [r1, #0x4]
    ldrb r0, [r12, #0x100]
    ldrsb r6, [r12, #32]
    cmp r0, #8
    addls pc, pc, r0, lsl #2
    b L_021eca84
    dcd 0xea000007
    dcd 0xea00000d
    dcd 0xea000023
    dcd 0xea000082
    dcd 0xea000084
    dcd 0xea00008d
    dcd 0xea000094
    dcd 0xea0000a7
    dcd 0xea0000af
    bl native_fn_021ecf88
    ldr r0, [pc, #0x2cc]
    mov r1, #1
    str r1, [r0, #0x8]
    ldr r0, [r0, #0x4]
    strb r1, [r0, #0x100]
    b L_021eca84
    ldr r0, [r1, #0x8]
    cmp r0, #0
    beq L_021ec7f8
    bl native_fn_02062520
    cmp r0, #0
    beq L_021eca84
L_021ec7f8:
    bl native_fn_021ecaa4
    ldr r0, [pc, #0x298]
    mov r1, #2
    ldr r2, [r0, #0x4]
    strb r1, [r2, #0x100]
    ldr r0, [r0, #0x8]
    cmp r0, #0
    beq L_021ec830
    mov r0, #0
    mov r2, #10
    bl native_fn_02041538
    ldr r0, [pc, #0x270]
    mov r1, #0
    str r1, [r0, #0x8]
L_021ec830:
    ldr r0, [pc, #0x264]
    mov r1, #7
    strb r1, [r0, #0x1]
    ldr r0, [pc, #0x258]
    ldr r1, [r0, #0x4]
    ldrb r0, [r1, #0x518]
    cmp r0, #0
    bne L_021ec95c
    ldrh r0, [r5, #2]
    tst r0, #2
    beq L_021ec88c
    ldr r0, [pc, #0x23c]
    bl native_fn_021ed560
    ldr r1, [pc, #0x230]
    ldr r3, [r1, #0x4]
    ldrsb r2, [r3, #32]
    cmp r0, r2
    beq L_021ec95c
    strb r0, [r3, #0x102]
    ldr r0, [r1, #0x4]
    mov r1, #3
    strb r1, [r0, #0x100]
    b L_021ec95c
L_021ec88c:
    tst r0, #1
    beq L_021ec8c4
    ldr r0, [pc, #0x204]
    bl native_fn_021ed6bc
    ldr r1, [pc, #0x1f8]
    ldr r3, [r1, #0x4]
    ldrsb r2, [r3, #32]
    cmp r0, r2
    beq L_021ec95c
    strb r0, [r3, #0x102]
    ldr r0, [r1, #0x4]
    mov r1, #3
    strb r1, [r0, #0x100]
    b L_021ec95c
L_021ec8c4:
    tst r0, #2048
    beq L_021ec8ec
    bl native_fn_021ed1e0
    cmp r0, #0
    beq L_021ec95c
    ldr r0, [pc, #0x1bc]
    mov r1, #4
    ldr r0, [r0, #0x4]
    strb r1, [r0, #0x100]
    b L_021ec95c
L_021ec8ec:
    tst r0, #4
    beq L_021ec954
    ldrsb r0, [r1, #32]
    sub r0, r0, #1
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    and r0, r0, #255
    cmp r0, #1
    bhi L_021ec95c
    ldrb r0, [r1, #0x101]
    cmp r0, #0
    bne L_021ec95c
    bl native_fn_021ed368
    ldr r0, [pc, #0x174]
    ldr r0, [r0, #0x4]
    ldrb r0, [r0, #0x20]
    bl native_fn_021ee1b0
    mov r0, #0
    bl native_fn_021ef11c
    ldr r0, [pc, #0x15c]
    mov r3, #4
    ldr r2, [r0, #0x4]
    mov r1, #7
    strb r3, [r2, #0x100]
    strb r1, [r0, #0x1]
    b L_021ec95c
L_021ec954:
    ldr r0, [pc, #0x144]
    bl native_fn_021ecff0
L_021ec95c:
    ldr r0, [pc, #0x13c]
    bl native_fn_021edd04
    ldr r1, [pc, #0x130]
    ldr r3, [r1, #0x4]
    ldrsb r2, [r3, #32]
    cmp r0, r2
    beq L_021ec988
    strb r0, [r3, #0x102]
    ldr r0, [r1, #0x4]
    mov r1, #3
    strb r1, [r0, #0x100]
L_021ec988:
    ldr r0, [pc, #0x110]
    bl native_fn_021ee458
    ldr r0, [pc, #0x104]
    mov r1, #2
    ldr r0, [r0, #0x4]
    mov r2, #1
    add r3, r0, #1280
    ldrsh r5, [r3, #6]
    add r0, r0, #16
    str r5, [sp]
    ldrsh r3, [r3, #8]
    bl native_fn_021ef0b0
    b L_021eca84
    bl native_fn_021ed404
    mov r4, r0
    b L_021eca84
    bl native_fn_020c4318
    cmp r0, #0
    beq L_021eca84
    mov r0, #1
    bl native_fn_021ef11c
    ldr r0, [pc, #0xb8]
    mov r1, r4
    ldr r0, [r0, #0x4]
    strb r1, [r0, #0x100]
    b L_021eca84
    bl native_fn_020c4318
    cmp r0, #0
    beq L_021eca84
    ldr r0, [pc, #0x98]
    mov r1, #3
    ldr r0, [r0, #0x4]
    strb r1, [r0, #0x100]
    b L_021eca84
    ldrb r0, [r12, #0x519]
    cmp r0, #0
    beq L_021eca34
    bl native_fn_021ec748
    mov r5, r0
    bl native_fn_021ec718
    mov r1, r0
    mov r0, r5
    bl native_fn_02063b28
L_021eca34:
    mov r0, #0
    bl native_fn_02062074
    mov r0, #1
    mov r1, #2
    mov r2, #10
    bl native_fn_02041538
    ldr r0, [pc, #0x48]
    mov r1, #7
    ldr r0, [r0, #0x4]
    strb r1, [r0, #0x100]
    b L_021eca84
    mov r2, #0
    mov r3, r2
    add r0, r12, #16
    mov r1, r4
    str r2, [sp]
    bl native_fn_021ef0b0
    bl native_fn_02041814
    cmp r0, #1
    movne r4, #9
L_021eca84:
    ldr r1, [pc, #0x10]
    mov r0, r4
    ldr r1, [r1, #0x4]
    strb r6, [r1, #0x103]
    add sp, sp, #4
    ldmia sp!, {r3, r4, r5, r6, pc}
    dcd 0x02236bc4
    dcd 0x02236bc5
}
