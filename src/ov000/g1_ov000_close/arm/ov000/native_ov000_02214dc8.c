/* ov000 row 0x02214dc8: 316 bytes.
 *
 * What it does: 76 instructions and 9 call(s), then a 4-entry dispatch through an inline branch table at 0x02214dfc (dispatch word at 0x02214df4)
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

extern void native_fn_02214f98(void);
extern void native_fn_02041814(void);
extern void native_fn_020642dc(void);
extern void native_fn_020406a8(void);
extern void native_fn_02215000(void);
extern void native_fn_0204176c(void);
extern void native_fn_020273c8(void);
extern void native_fn_01ffa4b4(void);
extern u8 native_data_0222f8f4[];


asm u32 native_ov000_02214dc8 (register u32 a0)
{
L_02214dc8:
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    ldr r1, [pc, #0x124]
    ldr r2, [pc, #0x124]
    ldr r8, [r1, #0x8]
    mov r0, #12
    mla r0, r8, r0, r2
    ldr r7, [r1, #0xc]
    ldr r5, [pc, #0x114]
    mov r4, #1
    cmp r7, #3
    mov r6, #0
    addls pc, pc, r7, lsl #2
    b L_02214ec4
    dcd 0xea000002
    dcd 0xea000008
    dcd 0xea000012
    dcd 0xea00001a
    ldr r0, [r0]
    cmp r0, #0
    beq L_02214e1c
    blx r0
L_02214e1c:
    mov r0, #1
    str r0, [r5, #0x4]
    b L_02214ec4
    ldr r0, [r0, #0x4]
    blx r0
    cmp r0, r8
    beq L_02214ec4
    ldr r2, [r5]
    mov r1, #2
    str r2, [r5, #0xc]
    str r1, [r5, #0x4]
    str r0, [r5, #0x8]
    mov r6, r4
    b L_02214ec4
    ldr r0, [r0, #0x8]
    cmp r0, #0
    beq L_02214e68
    blx r0
    bl native_fn_02214f98
L_02214e68:
    mov r0, #3
    str r0, [r5, #0x4]
    mov r6, #1
    b L_02214ec4
    bl native_fn_02041814
    cmp r0, #1
    beq L_02214ec4
    bl native_fn_020642dc
    cmp r0, #30
    bne L_02214ea0
    mov r4, r6
    mov r0, r4
    bl native_fn_020406a8
    b L_02214ec4
L_02214ea0:
    bl native_fn_02215000
    cmp r0, #0
    ldr r1, [r5, #0x8]
    movne r4, #7
    mov r0, #0
    cmp r1, #2
    str r1, [r5]
    str r0, [r5, #0x4]
    moveq r4, r0
L_02214ec4:
    cmp r6, #0
    ldrne r0, [r5, #0x4]
    cmpne r7, r0
    beq L_02214edc
    bl L_02214dc8
    mov r4, r0
L_02214edc:
    bl native_fn_0204176c
    bl native_fn_020273c8
    cmp r0, #8
    bne L_02214ef0
    bl native_fn_01ffa4b4
L_02214ef0:
    mov r0, r4
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
    dcd 0x02245314
    dcd native_data_0222f8f4
    dcd 0x0224531c
}
