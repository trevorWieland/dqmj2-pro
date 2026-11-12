/* ov000 row 0x0221a3a0: 1352 bytes.
 *
 * What it does: 336 instructions and 51 call(s), then a 11-entry dispatch through an inline branch table at 0x0221a3dc (dispatch word at 0x0221a3d4)
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
extern void native_fn_0221a8e8(void);
extern void native_fn_02062520(void);
extern void native_fn_0221aa6c(void);
extern void native_fn_0221d110(void);
extern void native_fn_020c48bc(void);
extern void native_fn_020c48d0(void);
extern void native_fn_020c48e8(void);
extern void native_fn_02048f7c(void);
extern void native_fn_020c484c(void);
extern void native_fn_0221f45c(void);
extern void native_fn_02048094(void);
extern void native_fn_0221e7e8(void);
extern void native_fn_0221e6cc(void);
extern void native_fn_0221c0c4(void);
extern void native_fn_02041538(void);
extern void native_fn_0207e874(void);
extern void native_fn_0207f3b0(void);
extern void native_fn_02062e18(void);
extern void native_fn_0206e1ac(void);
extern void native_fn_0221be98(void);
extern void native_fn_0221bd3c(void);
extern void native_fn_0206c0b0(void);
extern void native_fn_0221bb00(void);
extern void native_fn_0221b624(void);
extern void native_fn_0221c4b0(void);
extern void native_fn_0221c59c(void);
extern void native_fn_0221bcc4(void);
extern void native_fn_0221aea4(void);
extern void native_fn_0221af88(void);
extern void native_fn_0221b070(void);
extern void native_fn_021eade4(void);
extern void native_fn_020c4318(void);
extern void native_fn_02068f60(void);
extern void native_fn_02062074(void);
extern void native_fn_020d38f0(void);
extern void native_fn_020d37f0(void);
extern void native_fn_02041814(void);
extern void native_fn_0207ce20(void);


asm u32 native_ov000_0221a3a0 (register u32 a0)
{
L_0221a3a0:
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    sub sp, sp, #8
    mov r4, #0
    bl native_fn_0202a634
    mov r7, r4
    ldr r1, [pc, #0x524]
    mov r5, r0
    ldr r0, [pc, #0x520]
    ldrb r2, [r1, #0x7]
    ldrsb r6, [r0, #16]
    mov r8, r7
    str r7, [sp, #0x4]
    cmp r2, #10
    addls pc, pc, r2, lsl #2
    b L_0221a820
    dcd 0xea000009
    dcd 0xea00000e
    dcd 0xea000011
    dcd 0xea000050
    dcd 0xea0000d3
    dcd 0xea0000e4
    dcd 0xea0000ef
    dcd 0xea0000c8
    dcd 0xea0000f5
    dcd 0xea000101
    dcd 0xea000105
    bl native_fn_0221a8e8
    ldr r0, [pc, #0x4cc]
    mov r1, #1
    strb r1, [r0, #0x7]
    str r1, [r0, #0x14]
    b L_0221a820
    mov r0, #2
    strb r0, [r1, #0x7]
    mov r7, #1
    b L_0221a820
    ldr r0, [r1, #0x14]
    cmp r0, #0
    beq L_0221a448
    bl native_fn_02062520
    cmp r0, #0
    beq L_0221a820
L_0221a448:
    bl native_fn_0221aa6c
    ldr r0, [pc, #0x490]
    ldrsb r3, [r0, #16]
    cmp r3, #8
    beq L_0221a480
    ldr r2, [pc, #0x47c]
    mov r1, #3
    strb r1, [r2, #0x7]
    cmp r3, #2
    bne L_0221a4f0
    ldr r1, [sp, #0x4]
    ldr r2, [r2, #0x20]
    bl native_fn_0221d110
    b L_0221a4f0
L_0221a480:
    bl native_fn_020c48bc
    mov r0, #9
    mov r1, #0
    mov r2, #22
    bl native_fn_020c48d0
    mov r0, #87
    bl native_fn_020c48e8
    mov r0, #1
    bl native_fn_02048f7c
    bl native_fn_020c484c
    bl native_fn_0221f45c
    mov r1, #0
    bl native_fn_02048094
    mov r0, #0
    bl native_fn_0221e7e8
    ldr r0, [pc, #0x420]
    ldr r1, [sp, #0x4]
    ldr r2, [pc, #0x414]
    ldr r2, [r2, #0x20]
    bl native_fn_0221d110
    ldr r0, [pc, #0x40c]
    ldr r1, [pc, #0x404]
    ldr r1, [r1, #0x20]
    bl native_fn_0221e6cc
    bl native_fn_0221c0c4
    mov r1, #5
    ldr r0, [pc, #0x3f0]
    strb r1, [r0, #0x7]
L_0221a4f0:
    ldr r0, [pc, #0x3e8]
    ldr r0, [r0, #0x14]
    cmp r0, #0
    beq L_0221a51c
    mov r0, #0
    mov r1, #2
    mov r2, #10
    bl native_fn_02041538
    ldr r0, [pc, #0x3c8]
    mov r1, #0
    str r1, [r0, #0x14]
L_0221a51c:
    ldr r0, [pc, #0x3bc]
    mov r1, #0
    strb r1, [r0, #0x5]
    mov r7, #1
    b L_0221a820
    strb r7, [sp]
    bl native_fn_0221c0c4
    ldr r0, [pc, #0x3a0]
    ldrb r0, [r0, #0x5]
    cmp r0, #0
    bne L_0221a6ec
    ldr r0, [pc, #0x394]
    ldrsb r0, [r0, #16]
    cmp r0, #7
    bne L_0221a5ac
    bl native_fn_0207e874
    cmp r0, #1
    bne L_0221a6ec
    ldr r0, [pc, #0x374]
    mov r1, #1
    strb r1, [r0, #0x5]
    bl native_fn_0207f3b0
    ldr r2, [pc, #0x364]
    mov r1, r0
    ldr r0, [r2, #0xc]
    bl native_fn_02062e18
    bl native_fn_0206e1ac
    ldr r0, [pc, #0x350]
    mov r2, #10
    strb r2, [r0, #0x3]
    mov r0, #1
    mov r1, #2
    bl native_fn_02041538
    mov r0, #1
    str r0, [sp, #0x4]
    b L_0221a6ec
L_0221a5ac:
    add r0, sp, #4
    bl native_fn_0221be98
    ldr r1, [pc, #0x328]
    ldrsb r1, [r1, #16]
    cmp r0, r1
    beq L_0221a5d4
    ldr r1, [pc, #0x314]
    mov r2, #1
    strb r0, [r1, #0x3]
    strb r2, [r1, #0x5]
L_0221a5d4:
    add r0, sp, #0
    bl native_fn_0221bd3c
    ldrb r0, [sp]
    cmp r0, #0
    bne L_0221a6ac
    bl native_fn_0206c0b0
    cmp r0, #0
    bne L_0221a6ac
    ldrh r0, [r5, #2]
    tst r0, #2
    beq L_0221a630
    add r0, sp, #4
    bl native_fn_0221bb00
    ldr r1, [pc, #0x2d4]
    ldrsb r1, [r1, #16]
    cmp r0, r1
    beq L_0221a628
    ldr r1, [pc, #0x2c0]
    mov r2, #1
    strb r0, [r1, #0x3]
    strb r2, [r1, #0x5]
L_0221a628:
    mov r8, #1
    b L_0221a6ac
L_0221a630:
    tst r0, #1
    beq L_0221a668
    add r0, sp, #4
    bl native_fn_0221b624
    ldr r1, [pc, #0x29c]
    ldrsb r1, [r1, #16]
    cmp r0, r1
    beq L_0221a660
    ldr r1, [pc, #0x288]
    mov r2, #1
    strb r0, [r1, #0x3]
    strb r2, [r1, #0x5]
L_0221a660:
    mov r8, #1
    b L_0221a6ac
L_0221a668:
    tst r0, #2048
    beq L_0221a68c
    bl native_fn_0221c4b0
    cmp r0, #0
    ldrne r0, [pc, #0x260]
    movne r1, #5
    strneb r1, [r0, #0x7]
    mov r8, #1
    b L_0221a6ac
L_0221a68c:
    tst r0, #4
    beq L_0221a6ac
    bl native_fn_0221c59c
    cmp r0, #0
    ldrne r0, [pc, #0x23c]
    movne r1, #5
    strneb r1, [r0, #0x7]
    mov r8, #1
L_0221a6ac:
    ldrb r0, [sp]
    cmp r0, #0
    bne L_0221a6ec
    bl native_fn_0206c0b0
    cmp r0, #0
    bne L_0221a6ec
    ldr r0, [pc, #0x214]
    ldrb r1, [r0, #0x7]
    cmp r1, #7
    beq L_0221a6ec
    ldrb r0, [r0, #0x5]
    cmp r0, #0
    cmpeq r8, #0
    bne L_0221a6ec
    add r0, sp, #4
    bl native_fn_0221bcc4
L_0221a6ec:
    ldr r0, [pc, #0x1ec]
    ldrb r0, [r0, #0x5]
    cmp r0, #0
    beq L_0221a710
    bl native_fn_0221aea4
    cmp r0, #1
    ldreq r0, [pc, #0x1d4]
    moveq r1, #7
    streqb r1, [r0, #0x7]
L_0221a710:
    ldr r0, [pc, #0x1c8]
    mov r1, #1
    strb r1, [r0, #0x6]
    b L_0221a820
    bl native_fn_0221af88
    cmp r0, #0
    beq L_0221a820
    ldr r0, [pc, #0x1ac]
    mov r1, #4
    strb r1, [r0, #0x7]
    mov r7, #1
    b L_0221a820
    bl native_fn_0221b070
    cmp r0, #0
    beq L_0221a820
    ldr r1, [pc, #0x18c]
    ldr r0, [pc, #0x18c]
    ldrsb r1, [r1, #3]
    strb r1, [r0, #0x10]
    bl native_fn_021eade4
    cmp r0, #0
    bne L_0221a778
    ldr r0, [pc, #0x170]
    mov r1, #6
    strb r1, [r0, #0x7]
    b L_0221a820
L_0221a778:
    ldr r0, [pc, #0x160]
    mov r1, #2
    strb r1, [r0, #0x7]
    b L_0221a820
    bl native_fn_0221c0c4
    bl native_fn_020c4318
    cmp r0, #0
    beq L_0221a820
    mov r0, #1
    bl native_fn_0221e7e8
    mov r0, #1
    bl native_fn_02068f60
    ldr r0, [pc, #0x130]
    mov r1, #3
    strb r1, [r0, #0x7]
    b L_0221a820
    bl native_fn_021eade4
    cmp r0, #0
    ldrne r0, [pc, #0x118]
    movne r1, #2
    strneb r1, [r0, #0x7]
    ldr r0, [pc, #0x10c]
    ldrsb r6, [r0]
    b L_0221a820
    mov r0, r7
    bl native_fn_02062074
    mov r0, #1
    mov r1, #2
    mov r2, #10
    bl native_fn_02041538
    mov r0, r4
    bl native_fn_020d38f0
    bl native_fn_020d37f0
    ldr r0, [pc, #0xdc]
    mov r1, #9
    strb r1, [r0, #0x7]
    b L_0221a820
    ldr r1, [r1, #0x20]
    bl native_fn_0221e6cc
    bl native_fn_02041814
    cmp r0, #1
    movne r4, #9
L_0221a820:
    ldr r0, [pc, #0xb8]
    ldrb r0, [r0, #0x6]
    cmp r0, #0
    beq L_0221a8bc
    ldr r0, [pc, #0xac]
    ldrsb r1, [r0, #16]
    cmp r1, #7
    beq L_0221a8b0
    bl native_fn_0207ce20
    ldr r0, [pc, #0x94]
    ldrb r0, [r0, #0x5]
    cmp r0, #0
    beq L_0221a868
    ldr r0, [pc, #0x88]
    ldrsb r0, [r0, #16]
    cmp r0, #2
    cmpne r0, #3
    beq L_0221a87c
L_0221a868:
    ldr r0, [pc, #0x70]
    ldr r1, [sp, #0x4]
    ldr r2, [r0, #0x20]
    ldr r0, [pc, #0x68]
    bl native_fn_0221d110
L_0221a87c:
    ldr r0, [pc, #0x5c]
    ldrb r0, [r0, #0x5]
    cmp r0, #0
    beq L_0221a8a0
    ldr r0, [pc, #0x50]
    ldrsb r0, [r0, #16]
    cmp r0, #2
    cmpne r0, #3
    beq L_0221a8b0
L_0221a8a0:
    ldr r1, [pc, #0x38]
    ldr r0, [pc, #0x38]
    ldr r1, [r1, #0x20]
    bl native_fn_0221e6cc
L_0221a8b0:
    ldr r0, [pc, #0x28]
    mov r1, #0
    strb r1, [r0, #0x6]
L_0221a8bc:
    cmp r7, #0
    ldreq r1, [pc, #0x18]
    addeq sp, sp, #8
    moveq r0, r4
    streqb r6, [r1]
    ldmeqia sp!, {r4, r5, r6, r7, r8, pc}
    bl L_0221a3a0
    add sp, sp, #8
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
    dcd 0x02246090
    dcd 0x022460d4
}
