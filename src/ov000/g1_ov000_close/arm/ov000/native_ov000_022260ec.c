/* ov000 row 0x022260ec: 1320 bytes.
 *
 * What it does: 326 instructions and 36 call(s), then a 27-entry dispatch through an inline branch table at 0x02226130 (dispatch word at 0x02226128)
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
extern void native_fn_02224e38(void);
extern void native_fn_02225238(void);
extern void native_fn_02224b84(void);
extern void native_fn_02227a54(void);
extern void native_fn_02225eb8(void);
extern void native_fn_020644c0(void);
extern void native_fn_020624c0(void);
extern void native_fn_020624d0(void);
extern void native_fn_02225d74(void);
extern void native_fn_02225e4c(void);
extern void native_fn_0205e7a8(void);
extern u8 native_data_0222feb4[];


asm u32 native_ov000_022260ec (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r4, #0
    bl native_fn_0202a634
    ldr r2, [pc, #0x504]
    ldr r3, [pc, #0x504]
    ldrsb r1, [r2, #24]
    mov r5, r0
    ldr r6, [pc, #0x4fc]
    add r0, r1, r1, lsl #2
    add r0, r3, r0
    ldrb r0, [r0, #0x3]
    mov r0, r0, lsl #28
    movs r0, r0, lsr #28
    beq L_02226468
    cmp r1, #26
    addls pc, pc, r1, lsl #2
    b L_022265fc
    dcd 0xea000131
    dcd 0xea000130
    dcd 0xea00012f
    dcd 0xea00012e
    dcd 0xea00001c
    dcd 0xea0000b9
    dcd 0xea0000b8
    dcd 0xea000012
    dcd 0xea000038
    dcd 0xea000128
    dcd 0xea000127
    dcd 0xea000126
    dcd 0xea000052
    dcd 0xea00003e
    dcd 0xea00003d
    dcd 0xea000122
    dcd 0xea000121
    dcd 0xea000120
    dcd 0xea00011f
    dcd 0xea00011e
    dcd 0xea000064
    dcd 0xea00006b
    dcd 0xea00011b
    dcd 0xea00011a
    dcd 0xea000070
    dcd 0xea000086
    dcd 0xea000096
    ldrh r0, [r5, #2]
    tst r0, #2
    beq L_022261b8
    bl native_fn_02224e38
    ldr r1, [pc, #0x450]
    str r0, [r1, #0x14]
    b L_022265fc
L_022261b8:
    cmp r1, #4
    bne L_022261f0
    ldr r0, [pc, #0x43c]
    ldrsb r0, [r0, #27]
    cmp r0, #0
    beq L_022261f0
    bl native_fn_02225238
    cmp r0, #0
    beq L_022261f0
    ldr r0, [pc, #0x420]
    mov r1, #7
    strb r1, [r0, #0x1a]
    mov r1, #5
    str r1, [r0, #0x14]
L_022261f0:
    ldrb r0, [r6, #0x18c]
    cmp r0, #127
    beq L_022265fc
    cmp r0, #1
    bne L_02226218
    mov r0, #1
    bl native_fn_02224b84
    ldr r1, [pc, #0x3f0]
    str r0, [r1, #0x14]
    b L_022265fc
L_02226218:
    cmp r0, #2
    bne L_022265fc
    ldr r0, [pc, #0x3dc]
    mov r1, #6
    strb r1, [r0, #0x1a]
    mov r1, #5
    str r1, [r0, #0x14]
    b L_022265fc
    bl native_fn_02227a54
    cmp r0, #0
    bne L_022265fc
    ldr r0, [pc, #0x3b8]
    ldr r2, [r0, #0x10]
    sub r1, r2, #1
    str r1, [r0, #0x10]
    cmp r2, #0
    bge L_022265fc
    bl native_fn_02225eb8
    b L_022265fc
    ldrb r0, [r6, #0x18c]
    cmp r0, #127
    strneb r0, [r2, #0x21]
    ldr r0, [pc, #0x38c]
    ldrb r0, [r0, #0x21]
    cmp r0, #127
    beq L_022265fc
    bl native_fn_02225238
    cmp r0, #0
    beq L_022265fc
    ldr r0, [pc, #0x370]
    ldrb r0, [r0, #0x21]
    cmp r0, #2
    bne L_022265fc
    mov r0, #1
    bl native_fn_02224b84
    ldr r1, [pc, #0x358]
    str r0, [r1, #0x14]
    b L_022265fc
    ldrb r0, [r6, #0x18c]
    cmp r0, #127
    beq L_022265fc
    bl native_fn_02225238
    cmp r0, #0
    beq L_022265fc
    ldr r0, [pc, #0x334]
    ldrsb r0, [r0, #28]
    cmp r0, #0
    ldreqb r0, [r6, #0x18c]
    cmpeq r0, #0
    bne L_022262f4
    mov r0, #1
    bl native_fn_02224b84
    ldr r1, [pc, #0x314]
    str r0, [r1, #0x14]
    b L_022265fc
L_022262f4:
    ldrb r0, [r6, #0x18c]
    cmp r0, #2
    bne L_022265fc
    ldr r0, [pc, #0x2fc]
    mov r1, #14
    strb r1, [r0, #0x1a]
    mov r1, #5
    str r1, [r0, #0x14]
    b L_022265fc
    ldrb r0, [r6, #0x18f]
    cmp r0, #0
    beq L_022265fc
    mov r0, #1
    bl native_fn_02224b84
    ldr r1, [pc, #0x2d0]
    str r0, [r1, #0x14]
    b L_022265fc
    bl native_fn_020644c0
    cmp r0, #0
    beq L_022265fc
    mov r0, #1
    bl native_fn_02224b84
    ldr r1, [pc, #0x2b0]
    str r0, [r1, #0x14]
    b L_022265fc
    ldrb r0, [r6, #0x18c]
    cmp r0, #127
    beq L_022265fc
    bl native_fn_02225238
    cmp r0, #0
    beq L_022265fc
    ldr r0, [pc, #0x28c]
    ldrsb r0, [r0, #28]
    cmp r0, #0
    ldreqb r0, [r6, #0x18c]
    cmpeq r0, #0
    bne L_0222639c
    mov r0, #1
    bl native_fn_02224b84
    ldr r1, [pc, #0x26c]
    str r0, [r1, #0x14]
    b L_022265fc
L_0222639c:
    ldr r0, [pc, #0x260]
    mov r1, #26
    strb r1, [r0, #0x1a]
    mov r1, #5
    str r1, [r0, #0x14]
    b L_022265fc
    ldrb r0, [r6, #0x18c]
    cmp r0, #127
    beq L_022265fc
    bl native_fn_02225238
    cmp r0, #0
    beq L_022265fc
    ldrb r0, [r6, #0x18c]
    cmp r0, #1
    bne L_022265fc
    ldr r1, [pc, #0x224]
    mov r2, #60
    mov r0, #1
    str r2, [r1, #0x4]
    bl native_fn_02224b84
    ldr r1, [pc, #0x210]
    str r0, [r1, #0x14]
    b L_022265fc
    ldrb r0, [r6, #0x18c]
    cmp r0, #127
    beq L_022265fc
    bl native_fn_02225238
    cmp r0, #0
    beq L_022265fc
    ldrb r0, [r6, #0x18c]
    cmp r0, #1
    bne L_022265fc
    mov r0, #1
    bl native_fn_02224b84
    ldr r1, [pc, #0x1d8]
    str r0, [r1, #0x14]
    b L_022265fc
    ldrb r0, [r6, #0x18c]
    cmp r0, #127
    beq L_022265fc
    bl native_fn_02225238
    cmp r0, #0
    beq L_022265fc
    ldrb r0, [r6, #0x18c]
    cmp r0, #2
    bne L_022265fc
    mov r0, #1
    bl native_fn_02224b84
    ldr r1, [pc, #0x1a0]
    str r0, [r1, #0x14]
    b L_022265fc
L_02226468:
    cmp r1, #10
    beq L_0222650c
    cmp r1, #17
    beq L_02226484
    cmp r1, #18
    beq L_022264c8
    b L_022265a0
L_02226484:
    mov r0, #19
    bl native_fn_020624c0
    cmp r0, #0
    beq L_022264a8
    mov r1, r4
    mov r3, r1
    mov r0, #19
    mov r2, #1
    bl native_fn_020624d0
L_022264a8:
    bl native_fn_02225d74
    cmp r0, #0
    beq L_022265f8
    mov r0, #0
    bl native_fn_02224b84
    ldr r1, [pc, #0x140]
    str r0, [r1, #0x14]
    b L_022265f8
L_022264c8:
    mov r0, #19
    bl native_fn_020624c0
    cmp r0, #1
    beq L_022264ec
    mov r1, #1
    mov r2, r1
    mov r0, #19
    mov r3, r4
    bl native_fn_020624d0
L_022264ec:
    bl native_fn_02225e4c
    cmp r0, #0
    beq L_022265f8
    mov r0, #0
    bl native_fn_02224b84
    ldr r1, [pc, #0xfc]
    str r0, [r1, #0x14]
    b L_022265f8
L_0222650c:
    ldrb r0, [r6, #0x18c]
    cmp r0, #127
    strneb r0, [r2, #0x21]
    ldr r0, [pc, #0xe4]
    ldrb r0, [r0, #0x21]
    cmp r0, #127
    beq L_022265f8
    bl native_fn_02225238
    cmp r0, #0
    beq L_022265f8
    ldrh r1, [r5, #2]
    ldr r0, [pc, #0xd0]
    tst r1, r0
    ldreq r0, [pc, #0xbc]
    ldreqsb r0, [r0, #28]
    cmpeq r0, #0
    beq L_022265f8
    ldr r0, [pc, #0xac]
    ldrb r1, [r0, #0x21]
    cmp r1, #2
    bne L_022265f8
    ldrsb r0, [r0, #28]
    cmp r0, #0
    bne L_02226580
    mov r0, #1
    bl native_fn_02224b84
    ldr r1, [pc, #0x88]
    str r0, [r1, #0x14]
    b L_022265f8
L_02226580:
    mov r0, #0
    bl native_fn_02224b84
    ldr r2, [pc, #0x74]
    mov r1, #87
    str r0, [r2, #0x14]
    mvn r0, #0
    bl native_fn_0205e7a8
    b L_022265f8
L_022265a0:
    ldrh r1, [r5, #2]
    ldr r0, [pc, #0x64]
    tst r1, r0
    ldreqsb r0, [r2, #28]
    cmpeq r0, #0
    beq L_022265f8
    ldr r0, [pc, #0x44]
    ldrsb r0, [r0, #28]
    cmp r0, #0
    bne L_022265dc
    mov r0, #1
    bl native_fn_02224b84
    ldr r1, [pc, #0x2c]
    str r0, [r1, #0x14]
    b L_022265f8
L_022265dc:
    mov r0, #0
    bl native_fn_02224b84
    ldr r2, [pc, #0x18]
    mov r1, #87
    str r0, [r2, #0x14]
    mvn r0, #0
    bl native_fn_0205e7a8
L_022265f8:
    mov r4, #1
L_022265fc:
    mov r0, r4
    ldmia sp!, {r4, r5, r6, pc}
    dcd 0x022468b8
    dcd native_data_0222feb4
    dcd 0x02246aa8
    dcd 0x00000ff7
}
