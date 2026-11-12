/* ov000 row 0x022043c4: 1620 bytes.
 *
 * What it does: 403 instructions and 40 call(s), then a 13-entry dispatch through an inline branch table at 0x022044ec (dispatch word at 0x022044e4)
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

extern void native_fn_02061944(void);
extern void native_fn_02061dcc(void);
extern void native_fn_02072f48(void);
extern void native_fn_02049ffc(void);
extern void native_fn_02008be0(void);
extern void native_fn_021f35f0(void);
extern void native_fn_021f3544(void);
extern void native_fn_02044fcc(void);
extern void native_fn_02063520(void);
extern void native_fn_0204aaf0(void);
extern void native_fn_021f3580(void);
extern void native_fn_020635d4(void);
extern void native_fn_022042a8(void);
extern void native_fn_0204ac20(void);
extern void native_fn_02044ff4(void);
extern void native_fn_020602ec(void);
extern void native_fn_021f3558(void);


asm u32 native_ov000_022043c4 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, lr}
    sub sp, sp, #164
    mov r7, r0
    bl native_fn_02061944
    mov r0, r7
    bl native_fn_02061dcc
    add r3, sp, #32
    mov r2, #0
    add r1, sp, #28
    strh r2, [r3]
    strh r2, [r3, #2]
    strh r2, [r1]
    strh r2, [r1, #2]
    ldr r4, [r0]
    mov r5, #1
    cmp r4, #0
    ldrne r6, [r4, #0x4]
    cmpne r6, #0
    addeq sp, sp, #164
    ldmeqia sp!, {r4, r5, r6, r7, pc}
    ldr r0, [pc, #0x5f4]
    ldrsh r0, [r0, #12]
    cmp r0, #0
    ble L_02204430
    bl native_fn_02072f48
    cmp r0, #0
    movne r5, #0
L_02204430:
    mov r0, r6
    bl native_fn_02049ffc
    add r1, sp, #100
    mov r0, #0
    mov r2, #64
    bl native_fn_02008be0
    bl native_fn_021f35f0
    cmp r0, #0
    addeq sp, sp, #164
    ldmeqia sp!, {r4, r5, r6, r7, pc}
    ldr r0, [pc, #0x5b0]
    ldrb r1, [r0, #0xe]
    cmp r1, #0
    ldrneh r6, [r0, #12]
    subne r0, r1, #1
    strneb r0, [sp, #0x1e]
    bne L_02204488
    ldrsh r0, [r0, #12]
    bl native_fn_021f3544
    ldrh r6, [r0]
    mov r0, #0
    strb r0, [sp, #0x1e]
L_02204488:
    cmp r7, #10
    cmpne r7, #11
    cmpne r7, #12
    bne L_022044e0
    ldr r1, [pc, #0x570]
    ldrsh r0, [r1, #12]
    ldrb r1, [r1, #0xe]
    bl native_fn_02044fcc
    cmp r0, #0
    addne sp, sp, #164
    ldmneia sp!, {r4, r5, r6, r7, pc}
    ldr r1, [pc, #0x554]
    ldrsh r0, [r1, #12]
    ldrb r1, [r1, #0xe]
    bl native_fn_02063520
    cmp r0, #0
    cmpne r6, #0
    ldrne r0, [pc, #0x540]
    cmpne r6, r0
    cmpne r5, #0
    addeq sp, sp, #164
    ldmeqia sp!, {r4, r5, r6, r7, pc}
L_022044e0:
    cmp r7, #12
    addls pc, pc, r7, lsl #2
    b L_02204a08
    dcd 0xea000145
    dcd 0xea000144
    dcd 0xea000143
    dcd 0xea000142
    dcd 0xea000141
    dcd 0xea000140
    dcd 0xea000005
    dcd 0xea000013
    dcd 0xea000069
    dcd 0xea000077
    dcd 0xea0000de
    dcd 0xea000117
    dcd 0xea000125
    mov r0, #23
    str r0, [sp]
    mov r2, #1
    str r2, [sp, #0x4]
    str r2, [sp, #0x8]
    add r1, sp, #32
    mov r0, r7
    mov r2, #9
    mov r3, #5
    bl native_fn_0204aaf0
    ldrsh r1, [sp, #32]
    add r0, r1, r0
    strh r0, [sp, #32]
    add sp, sp, #164
    ldmia sp!, {r4, r5, r6, r7, pc}
    ldr r1, [pc, #0x4ac]
    ldrsh r0, [r1, #12]
    ldrb r1, [r1, #0xe]
    bl native_fn_021f3580
    add r3, sp, #24
    mov r2, #0
    ldr r1, [pc, #0x494]
    mov r4, r0
    strh r2, [r3]
    strh r2, [r3, #2]
    ldrsh r0, [r1, #12]
    ldrb r1, [r1, #0xe]
    bl native_fn_020635d4
    cmp r0, #0
    beq L_0220467c
    and r0, r4, #255
    bl native_fn_022042a8
    cmp r0, #0
    cmpne r5, #0
    beq L_0220467c
    cmp r4, #13
    mov r2, #1
    add r1, sp, #24
    beq L_02204648
    mov r0, r4, lsl #16
    mov r0, r0, lsr #16
    str r0, [sp]
    str r2, [sp, #0x4]
    str r2, [sp, #0x8]
    mov r0, r7
    mov r2, #6
    mov r3, #0
    bl native_fn_0204aaf0
    ldrsh r2, [sp, #24]
    ldr r1, [pc, #0x424]
    add r2, r2, r0
    ldrsh r0, [r1, #12]
    strh r2, [sp, #24]
    bl native_fn_021f3544
    ldrb r0, [r0, #0x7]
    cmp r0, #1
    addls sp, sp, #164
    ldmlsia sp!, {r4, r5, r6, r7, pc}
    ldrsh r1, [sp, #24]
    mov r0, #68
    mov r2, #1
    add r1, r1, #8
    strh r1, [sp, #24]
    str r0, [sp]
    str r2, [sp, #0x4]
    mov r4, #0
    add r1, sp, #24
    mov r0, r7
    mov r2, #5
    mov r3, #2
    str r4, [sp, #0x8]
    bl native_fn_0204aaf0
    add sp, sp, #164
    ldmia sp!, {r4, r5, r6, r7, pc}
L_02204648:
    mov r0, #16
    str r0, [sp]
    str r2, [sp, #0x4]
    str r2, [sp, #0x8]
    mov r0, r7
    mov r2, #9
    mov r3, #5
    bl native_fn_0204aaf0
    ldrsh r1, [sp, #24]
    add r0, r1, r0
    strh r0, [sp, #24]
    add sp, sp, #164
    ldmia sp!, {r4, r5, r6, r7, pc}
L_0220467c:
    mov r0, #42
    str r0, [sp]
    mov r2, #1
    str r2, [sp, #0x4]
    str r2, [sp, #0x8]
    add r1, sp, #24
    mov r0, r7
    mov r2, #5
    mov r3, #7
    bl native_fn_0204aaf0
    ldrsh r1, [sp, #24]
    add r0, r1, r0
    strh r0, [sp, #24]
    add sp, sp, #164
    ldmia sp!, {r4, r5, r6, r7, pc}
    mov r0, #24
    str r0, [sp]
    mov r2, #1
    str r2, [sp, #0x4]
    str r2, [sp, #0x8]
    add r1, sp, #32
    mov r0, r7
    mov r2, #9
    mov r3, #5
    bl native_fn_0204aaf0
    ldrsh r1, [sp, #32]
    add r0, r1, r0
    strh r0, [sp, #32]
    add sp, sp, #164
    ldmia sp!, {r4, r5, r6, r7, pc}
    ldr r1, [pc, #0x314]
    ldrsh r0, [r1, #12]
    ldrb r1, [r1, #0xe]
    bl native_fn_02044fcc
    cmp r0, #0
    bne L_02204858
    ldr r1, [pc, #0x2fc]
    ldrsh r0, [r1, #12]
    ldrb r1, [r1, #0xe]
    bl native_fn_02063520
    cmp r0, #0
    cmpne r5, #0
    beq L_02204858
    ldr r0, [pc, #0x2e4]
    add r1, sp, #20
    mov r5, #0
    strh r5, [r1]
    strh r5, [r1, #2]
    cmp r6, r0
    beq L_02204750
    mov r0, r6
    bl native_fn_02072f48
    mov r5, r0
L_02204750:
    cmp r6, #0
    cmpeq r5, #0
    bne L_0220478c
    mov r0, #47
    str r0, [sp]
    mov r4, #1
    str r4, [sp, #0x4]
    add r1, sp, #20
    mov r0, r7
    mov r2, #5
    mov r3, #2
    str r4, [sp, #0x8]
    bl native_fn_0204aaf0
    add sp, sp, #164
    ldmia sp!, {r4, r5, r6, r7, pc}
L_0220478c:
    ldr r0, [pc, #0x280]
    cmp r6, r0
    beq L_022047ac
    ldrb r1, [sp, #0x1e]
    mov r0, r6
    bl native_fn_020635d4
    cmp r0, #0
    beq L_022047b4
L_022047ac:
    cmp r5, #0
    beq L_022047d4
L_022047b4:
    mov r2, #1
    add r1, sp, #20
    mov r0, r7
    mov r3, #8
    str r2, [sp]
    bl native_fn_0204ac20
    add sp, sp, #164
    ldmia sp!, {r4, r5, r6, r7, pc}
L_022047d4:
    ldr r0, [pc, #0x238]
    cmp r6, r0
    beq L_022047f0
    ldr r0, [pc, #0x228]
    ldrb r0, [r0, #0xe]
    cmp r0, #0
    beq L_02204820
L_022047f0:
    mov r0, #69
    str r0, [sp]
    mov r4, #1
    str r4, [sp, #0x4]
    add r1, sp, #20
    mov r0, r7
    mov r2, #5
    mov r3, #2
    str r4, [sp, #0x8]
    bl native_fn_0204aaf0
    add sp, sp, #164
    ldmia sp!, {r4, r5, r6, r7, pc}
L_02204820:
    ldrb r2, [sp, #0x1e]
    add r0, sp, #68
    mov r1, r6
    bl native_fn_02044ff4
    mov r3, #0
    mov r0, r4
    add r2, sp, #68
    mov r1, r6
    str r3, [sp]
    mov r4, #1
    str r4, [sp, #0x4]
    bl native_fn_020602ec
    add sp, sp, #164
    ldmia sp!, {r4, r5, r6, r7, pc}
L_02204858:
    mov r0, #42
    str r0, [sp]
    mov r2, #1
    str r2, [sp, #0x4]
    str r2, [sp, #0x8]
    add r1, sp, #32
    mov r0, r7
    mov r2, #5
    mov r3, #7
    bl native_fn_0204aaf0
    ldrsh r1, [sp, #32]
    add r0, r1, r0
    strh r0, [sp, #32]
    add sp, sp, #164
    ldmia sp!, {r4, r5, r6, r7, pc}
    ldr r0, [pc, #0x174]
    ldrb r1, [r0, #0xe]
    cmp r1, #0
    ldrneh r5, [r0, #12]
    subne r0, r1, #1
    andne r6, r0, #255
    bne L_022048c0
    ldrsh r0, [r0, #12]
    bl native_fn_021f3544
    ldrh r5, [r0, #2]
    mov r6, #0
L_022048c0:
    mov r0, r5
    mov r1, r6
    bl native_fn_020635d4
    cmp r0, #0
    beq L_022048e4
    mov r0, r5
    bl native_fn_02072f48
    cmp r0, #0
    beq L_02204904
L_022048e4:
    mov r2, #1
    add r1, sp, #32
    mov r0, r7
    mov r3, #8
    str r2, [sp]
    bl native_fn_0204ac20
    add sp, sp, #164
    ldmia sp!, {r4, r5, r6, r7, pc}
L_02204904:
    ldr r0, [pc, #0x104]
    ldrb r0, [r0, #0xe]
    cmp r0, #0
    beq L_02204944
    mov r0, #69
    str r0, [sp]
    mov r4, #1
    str r4, [sp, #0x4]
    add r1, sp, #32
    mov r0, r7
    mov r2, #5
    mov r3, #2
    str r4, [sp, #0x8]
    bl native_fn_0204aaf0
    add sp, sp, #164
    ldmia sp!, {r4, r5, r6, r7, pc}
L_02204944:
    add r0, sp, #36
    mov r1, r5
    mov r2, r6
    bl native_fn_02044ff4
    mov r3, #0
    mov r0, r4
    add r2, sp, #36
    mov r1, r5
    str r3, [sp]
    mov r4, #1
    str r4, [sp, #0x4]
    bl native_fn_020602ec
    add sp, sp, #164
    ldmia sp!, {r4, r5, r6, r7, pc}
    add r1, sp, #16
    mov r0, #0
    strh r0, [r1]
    strh r0, [r1, #2]
    mov r0, #8
    str r0, [sp]
    mov r4, #1
    str r4, [sp, #0x4]
    mov r0, r7
    mov r2, #9
    mov r3, #2
    str r4, [sp, #0x8]
    bl native_fn_0204aaf0
    add sp, sp, #164
    ldmia sp!, {r4, r5, r6, r7, pc}
    ldr r1, [pc, #0x50]
    ldrsh r0, [r1, #12]
    ldrb r1, [r1, #0xe]
    bl native_fn_021f3558
    cmp r0, #0
    addeq sp, sp, #164
    ldmeqia sp!, {r4, r5, r6, r7, pc}
    add r1, sp, #12
    mov r0, #0
    strh r0, [r1]
    strh r0, [r1, #2]
    mov r0, #68
    str r0, [sp]
    mov r4, #1
    str r4, [sp, #0x4]
    mov r0, r7
    mov r2, #5
    mov r3, #2
    str r4, [sp, #0x8]
    bl native_fn_0204aaf0
L_02204a08:
    add sp, sp, #164
    ldmia sp!, {r4, r5, r6, r7, pc}
    dcd 0x02238190
    dcd 0x0000ffff
}
