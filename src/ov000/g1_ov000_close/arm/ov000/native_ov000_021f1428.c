/* ov000 row 0x021f1428: 1064 bytes.
 *
 * What it does: 265 instructions and 48 call(s), then a 7-entry dispatch through an inline branch table at 0x021f1458 (dispatch word at 0x021f1450)
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
extern void native_fn_0205e7a8(void);
extern void native_fn_021f1be0(void);
extern void native_fn_02062b9c(void);
extern void native_fn_020635d4(void);
extern void native_fn_020c48bc(void);
extern void native_fn_020c48d0(void);
extern void native_fn_02060954(void);
extern void native_fn_02044ff4(void);
extern void native_fn_02048034(void);
extern void native_fn_02072f48(void);
extern void native_fn_02062bf0(void);
extern void native_fn_02062c44(void);
extern void native_fn_021f24d8(void);
extern void native_fn_021f262c(void);
extern void native_fn_021f2524(void);
extern void native_fn_02063aa4(void);
extern void native_fn_020c48f8(void);
extern void native_fn_020c48e8(void);
extern void native_fn_021f2a64(void);


asm u32 native_ov000_021f1428 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    sub sp, sp, #32
    ldr r0, [pc, #0x414]
    ldr r0, [r0, #0x8]
    ldrsb r4, [r0, #32]
    bl native_fn_0202a634
    ldr r1, [pc, #0x404]
    ldr r3, [r1, #0x8]
    ldrsb r0, [r3, #32]
    cmp r0, #6
    addls pc, pc, r0, lsl #2
    b L_021f1840
    dcd 0xea000005
    dcd 0xea000022
    dcd 0xea000035
    dcd 0xea0000ce
    dcd 0xea0000f4
    dcd 0xea0000e0
    dcd 0xea0000f2
    ldr r0, [r3, #0x10]
    cmp r0, #0
    beq L_021f1494
    cmp r0, #1
    beq L_021f14a8
    cmp r0, #2
    beq L_021f14bc
    b L_021f14cc
L_021f1494:
    mvn r0, #0
    mov r1, #82
    bl native_fn_0205e7a8
    mov r4, #1
    b L_021f14cc
L_021f14a8:
    mvn r0, #0
    mov r1, #82
    bl native_fn_0205e7a8
    mov r4, #3
    b L_021f14cc
L_021f14bc:
    mvn r0, #0
    mov r1, #82
    bl native_fn_0205e7a8
    mov r4, #5
L_021f14cc:
    ldr r0, [pc, #0x378]
    mov r1, #0
    ldr r3, [r0, #0x8]
    ldr r2, [r3, #0x10]
    str r2, [r3, #0x100]
    ldr r0, [r0, #0x8]
    str r1, [r0, #0x104]
    b L_021f1840
    ldr r2, [r3, #0x10]
    add r0, r3, #4096
    strb r2, [r0, #0x921]
    ldr r0, [r1, #0x8]
    add r1, r0, #4096
    ldrb r0, [r0, #0x20]
    ldrb r1, [r1, #0x921]
    bl native_fn_021f1be0
    ldr r2, [pc, #0x338]
    mov r3, #0
    ldr r5, [r2, #0x8]
    sub r0, r3, #1
    ldr r4, [r5, #0x10]
    mov r1, #82
    str r4, [r5, #0x104]
    ldr r2, [r2, #0x8]
    mov r4, #2
    str r3, [r2, #0x108]
    bl native_fn_0205e7a8
    b L_021f1840
    ldr r0, [r3, #0x10]
    mov r5, #0
    add r0, r3, r0, lsl #2
    ldr r1, [r0, #0x10c]
    mov r0, r1, lsl #16
    mov r1, r1, lsr #16
    mov r7, r0, asr #16
    and r6, r1, #255
    mov r0, r7
    mov r1, r6
    bl native_fn_02062b9c
    mov r9, r0
    mov r0, r7
    mov r1, r6
    bl native_fn_020635d4
    cmp r0, #0
    beq L_021f1840
    cmp r9, #0
    bne L_021f15cc
    bl native_fn_020c48bc
    mov r0, #9
    mov r1, #5
    mov r2, #30
    bl native_fn_020c48d0
    mov r0, r7
    mov r1, r5
    bl native_fn_02060954
    mov r8, r0
    mov r1, r7
    mov r2, r6
    add r0, sp, #0
    bl native_fn_02044ff4
    mov r1, r8
    add r0, sp, #0
    bl native_fn_02048034
    b L_021f1774
L_021f15cc:
    cmp r7, #0
    ble L_021f1628
    mov r0, r7
    bl native_fn_02072f48
    cmp r0, #0
    beq L_021f1628
    bl native_fn_020c48bc
    mov r0, #9
    mov r1, #5
    mov r2, #27
    bl native_fn_020c48d0
    mov r0, r7
    mov r1, r5
    bl native_fn_02060954
    mov r8, r0
    mov r1, r7
    mov r2, r6
    add r0, sp, #0
    bl native_fn_02044ff4
    mov r1, r8
    add r0, sp, #0
    bl native_fn_02048034
    b L_021f1774
L_021f1628:
    mov r0, r7
    mov r1, r6
    bl native_fn_02062bf0
    mov r8, r0
    mov r0, r7
    mov r1, r6
    bl native_fn_02062c44
    add r0, r8, r0
    cmp r9, r0
    bgt L_021f1668
    bl native_fn_020c48bc
    mov r0, #9
    mov r1, #5
    mov r2, #29
    bl native_fn_020c48d0
    b L_021f1774
L_021f1668:
    mov r0, r7
    mov r1, r6
    bl native_fn_021f24d8
    cmp r0, #0
    beq L_021f16e4
    bl native_fn_020c48bc
    mov r0, r7
    mov r1, r6
    bl native_fn_021f262c
    cmp r0, #0
    mov r0, #9
    mov r1, #5
    bne L_021f16a8
    mov r2, #35
    bl native_fn_020c48d0
    b L_021f16b0
L_021f16a8:
    mov r2, #36
    bl native_fn_020c48d0
L_021f16b0:
    mov r0, r7
    mov r1, #0
    bl native_fn_02060954
    mov r5, r0
    add r0, sp, #0
    mov r1, r7
    mov r2, r6
    bl native_fn_02044ff4
    add r0, sp, #0
    mov r1, r5
    bl native_fn_02048034
    mov r5, #1
    b L_021f1774
L_021f16e4:
    mov r0, r7
    mov r1, r6
    bl native_fn_021f2524
    bl native_fn_020c48bc
    bl native_fn_02063aa4
    mov r1, #0
    bl native_fn_02048034
    mov r1, #32
    mov r0, r7
    bl native_fn_02060954
    mov r5, r0
    add r0, sp, #0
    mov r1, r7
    mov r2, r6
    bl native_fn_02044ff4
    add r1, r5, #32
    add r0, sp, #0
    bl native_fn_02048034
    mov r0, #9
    mov r1, #5
    mov r2, #28
    bl native_fn_020c48d0
    mov r0, r7
    mov r1, r6
    bl native_fn_021f262c
    cmp r0, #0
    ldreq r0, [pc, #0xf8]
    moveq r1, #1
    ldrne r0, [pc, #0xf0]
    movne r1, #2
    ldr r0, [r0, #0x8]
    add r0, r0, #4096
    strb r1, [r0, #0x922]
    mov r0, #2
    bl native_fn_020c48f8
    mov r5, #1
L_021f1774:
    cmp r5, #0
    movne r0, #82
    moveq r0, #84
    bl native_fn_020c48e8
    mov r0, #0
    bl native_fn_021f2a64
    ldr r0, [pc, #0xb8]
    mov r1, #4
    ldr r0, [r0, #0x8]
    add r0, r0, #4096
    strb r1, [r0, #0x91d]
    b L_021f1840
    ldr r2, [r3, #0x10]
    add r0, r3, #4096
    strb r2, [r0, #0x921]
    ldr r0, [r1, #0x8]
    add r1, r0, #4096
    ldrb r0, [r0, #0x20]
    ldrb r1, [r1, #0x921]
    bl native_fn_021f1be0
    ldr r2, [pc, #0x80]
    mov r3, #0
    ldr r5, [r2, #0x8]
    sub r0, r3, #1
    ldr r4, [r5, #0x10]
    mov r1, #82
    str r4, [r5, #0x104]
    ldr r2, [r2, #0x8]
    mov r4, #4
    str r3, [r2, #0x108]
    bl native_fn_0205e7a8
    b L_021f1840
    ldr r2, [r3, #0x10]
    add r0, r3, #4096
    strb r2, [r0, #0x921]
    ldr r0, [r1, #0x8]
    add r1, r0, #4096
    ldrb r0, [r0, #0x20]
    ldrb r1, [r1, #0x921]
    bl native_fn_021f1be0
    ldr r2, [pc, #0x30]
    mov r3, #0
    ldr r5, [r2, #0x8]
    sub r0, r3, #1
    ldr r4, [r5, #0x10]
    mov r1, #82
    str r4, [r5, #0x104]
    ldr r2, [r2, #0x8]
    mov r4, #6
    str r3, [r2, #0x108]
    bl native_fn_0205e7a8
L_021f1840:
    mov r0, r4
    add sp, sp, #32
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
    dcd 0x02236d98
}
