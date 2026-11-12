/* ov000 row 0x0220629c: 348 bytes.
 *
 * What it does: 83 instructions and 7 call(s), then a 6-entry dispatch through an inline branch table at 0x022062d0 (dispatch word at 0x022062c8)
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

extern void native_fn_02041944(void);
extern void native_fn_02041538(void);
extern void native_fn_0202a634(void);
extern void native_fn_02206db8(void);
extern void native_fn_02041814(void);
extern void native_fn_0204176c(void);
extern u8 native_data_0222ba20[];


asm u32 native_ov000_0220629c (register u32 a0)
{
L_0220629c:
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    ldr r1, [pc, #0x140]
    ldr r2, [pc, #0x140]
    ldr r8, [r1, #0x18]
    mov r0, #12
    mla r0, r8, r0, r2
    ldr r7, [r1, #0x1c]
    ldr r5, [pc, #0x130]
    mov r4, #6
    cmp r7, #5
    mov r6, #0
    addls pc, pc, r7, lsl #2
    b L_022063c4
    dcd 0xea000004
    dcd 0xea00000a
    dcd 0xea000014
    dcd 0xea00002f
    dcd 0xea000037
    dcd 0xea000023
    ldr r0, [r0]
    cmp r0, #0
    beq L_022062f8
    blx r0
L_022062f8:
    mov r0, #1
    str r0, [r5, #0x4]
    b L_022063c4
    ldr r0, [r0, #0x4]
    blx r0
    cmp r0, r8
    beq L_022063c4
    ldr r2, [r5]
    mov r1, #2
    str r2, [r5, #0xc]
    str r1, [r5, #0x4]
    str r0, [r5, #0x8]
    mov r6, #1
    b L_022063c4
    ldr r0, [r0, #0x8]
    cmp r0, #0
    beq L_02206340
    blx r0
L_02206340:
    ldr r0, [r5, #0x8]
    mov r1, #3
    str r1, [r5, #0x4]
    cmp r0, #4
    mov r6, #1
    bne L_022063c4
    bl native_fn_02041944
    cmp r0, #0
    bne L_022063c4
    mov r0, r6
    mov r1, #2
    mov r2, #10
    bl native_fn_02041538
    b L_022063c4
    bl native_fn_0202a634
    ldrh r1, [r0, #2]
    ldr r0, [pc, #0x6c]
    tst r1, r0
    beq L_022063c4
    mov r0, #1
    bl native_fn_02206db8
    mov r0, #1
    str r0, [r5, #0x4]
    b L_022063c4
    bl native_fn_02041814
    cmp r0, #1
    beq L_022063c4
    ldr r1, [r5, #0x8]
    mov r0, r6
    cmp r1, #4
    str r1, [r5]
    str r0, [r5, #0x4]
    moveq r4, r0
L_022063c4:
    cmp r6, #0
    ldrne r0, [r5, #0x4]
    cmpne r7, r0
    beq L_022063dc
    bl L_0220629c
    mov r4, r0
L_022063dc:
    bl native_fn_0204176c
    mov r0, r4
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
    dcd 0x02238248
    dcd native_data_0222ba20
    dcd 0x02238260
    dcd 0x00000ff7
}
