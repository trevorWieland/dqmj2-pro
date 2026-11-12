/* ov000 row 0x02223580: 444 bytes.
 *
 * What it does: 109 instructions and 13 call(s), then a 4-entry dispatch through an inline branch table at 0x022235b0 (dispatch word at 0x022235a8)
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

extern void native_fn_02223c60(void);
extern void native_fn_02041814(void);
extern void native_fn_02045738(void);
extern void native_fn_0202a1e0(void);
extern void native_fn_0206258c(void);
extern void native_fn_020c40f4(void);
extern void native_fn_020851d4(void);
extern void native_fn_02085200(void);
extern void native_fn_0204176c(void);
extern u8 native_data_0222df40[];


asm u32 native_ov000_02223580 (register u32 a0)
{
L_02223580:
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    bl native_fn_02223c60
    mov r4, r0
    ldmia r4, {r7, r8}
    ldr r1, [pc, #0x19c]
    mov r0, #12
    mla r0, r7, r0, r1
    cmp r8, #3
    mov r5, #7
    mov r6, #0
    addls pc, pc, r8, lsl #2
    b L_022236cc
    dcd 0xea000002
    dcd 0xea000008
    dcd 0xea000012
    dcd 0xea000019
    ldr r0, [r0]
    cmp r0, #0
    beq L_022235d0
    blx r0
L_022235d0:
    mov r0, #1
    str r0, [r4, #0x4]
    b L_022236cc
    ldr r0, [r0, #0x4]
    blx r0
    cmp r0, r7
    beq L_022236cc
    ldr r2, [r4]
    mov r1, #2
    str r2, [r4, #0xc]
    str r1, [r4, #0x4]
    str r0, [r4, #0x8]
    mov r6, #1
    b L_022236cc
    ldr r0, [r0, #0x8]
    cmp r0, #0
    beq L_02223618
    blx r0
L_02223618:
    mov r0, #3
    str r0, [r4, #0x4]
    mov r6, #1
    b L_022236cc
    bl native_fn_02041814
    cmp r0, #1
    beq L_022236cc
    ldr r1, [r4, #0x8]
    mov r0, r6
    str r1, [r4]
    str r0, [r4, #0x4]
    ldr r1, [r4]
    cmp r1, #12
    addls pc, pc, r1, lsl #2
    b L_022236cc
    b L_022236cc
    b L_022236cc
    b L_022236cc
    b L_022236cc
    b L_02223688
    b L_022236cc
    b L_02223690
    b L_02223690
    b L_022236b8
    b L_022236b8
    b L_022236c4
    b L_022236c4
    b L_022236c4
L_02223688:
    mov r5, r0
    b L_022236cc
L_02223690:
    mov r0, #1
    bl native_fn_02045738
    mov r0, #2
    bl native_fn_0202a1e0
    mov r0, r6
    bl native_fn_0206258c
    mov r0, #1
    bl native_fn_020c40f4
    mov r5, #3
    b L_022236cc
L_022236b8:
    bl native_fn_0206258c
    mov r5, #1
    b L_022236cc
L_022236c4:
    bl native_fn_0206258c
    mov r5, r6
L_022236cc:
    cmp r6, #0
    ldrne r0, [r4, #0x4]
    cmpne r8, r0
    beq L_022236e4
    bl L_02223580
    mov r5, r0
L_022236e4:
    cmp r6, #2
    bne L_02223704
    ldr r0, [r4, #0x4]
    cmp r8, r0
    beq L_02223728
    bl L_02223580
    mov r5, r0
    b L_02223728
L_02223704:
    ldr r0, [r4]
    cmp r0, #4
    moveq r5, #0
    beq L_02223728
    bl native_fn_020851d4
    bl native_fn_02085200
    ldr r0, [pc, #0x14]
    mov r1, #1
    str r1, [r0, #0xc84]
L_02223728:
    bl native_fn_0204176c
    mov r0, r5
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
    dcd native_data_0222df40
    dcd 0x02101ae8
}
