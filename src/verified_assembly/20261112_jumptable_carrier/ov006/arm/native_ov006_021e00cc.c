/* ov006 row 0x021e00cc: 904 bytes.
 *
 * What it does: switch dispatch through an inline table
 *
 * Carrier: mwccarm asm with dcd data runs.
 * The measured extent is code plus data inside the function. The data
 * runs are emitted as data, not decoded as instructions; every
 * instruction, branch target, pool word and table entry is read from
 * the image.
 *
 * Unknowns: the field roles and the meaning of the table entries are not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02068510(void);
extern void native_fn_021dfe74(void);
extern void native_fn_020642dc(void);
extern void native_fn_021dea9c(void);
extern void native_fn_021e00bc(void);
extern void native_fn_021dfd70(void);
extern void native_fn_021d77e8(void);
extern void native_fn_01ff8580(void);
extern void native_fn_0206258c(void);
extern void native_fn_021dee68(void);
extern void native_fn_021ded5c(void);
extern void native_fn_0206442c(void);
extern void native_fn_021da9d0(void);
extern void native_fn_021df524(void);
extern void native_fn_021def28(void);
extern void native_fn_01ff8604(void);
extern void native_fn_02064488(void);
extern void native_fn_02068500(void);
extern void native_fn_02067748(void);
extern void native_fn_02008d78(void);
extern void native_fn_02067c08(void);
extern void native_fn_021da3b0(void);
extern void native_fn_021df974(void);
extern void native_fn_021d83c8(void);
extern void native_fn_0206344c(void);
extern void native_fn_021d83e4(void);
extern void native_fn_020678d4(void);
extern void native_fn_02067914(void);
extern void native_fn_02067978(void);
extern void native_fn_020679c0(void);
extern void native_fn_02067a00(void);
extern void native_fn_02067b70(void);
extern void native_fn_021e2f38(void);
extern void native_fn_02067a4c(void);
extern void native_fn_020679f0(void);
extern void native_fn_020642cc(void);


asm u32 native_ov006_021e00cc (register u32 a0)
{
    stmdb sp!, {r4, lr}
    sub sp, sp, #8
    bl native_fn_02068510
    cmp r0, #0
    bne L_021e00f0
    mov r0, #3
    mov r1, #2
    mov r2, #131
    bl native_fn_021dfe74
L_021e00f0:
    bl native_fn_020642dc
    cmp r0, #38
    bgt L_021e0134
    subs r1, r0, #28
    addpl pc, pc, r1, lsl #2
    b L_021e0380
    dcd 0xea00000c
    dcd 0xea00001e
    dcd 0xea000030
    dcd 0xea00005a
    dcd 0xea000098
    dcd 0xea00003e
    dcd 0xea000096
    dcd 0xea000095
    dcd 0xea000094
    dcd 0xea000093
    dcd 0xea000085
L_021e0134:
    cmp r0, #45
    beq L_021e0314
    b L_021e0380
    mov r0, #2
    mov r2, r0
    str r0, [sp]
    mov r4, #30
    mov r1, #0
    mov r3, #38
    str r4, [sp, #0x4]
    bl native_fn_021dea9c
    mov r0, #44
    bl native_fn_021e00bc
    mov r0, #6
    bl native_fn_021dfd70
    mov r0, #2
    bl native_fn_021d77e8
    mov r0, #1
    bl native_fn_01ff8580
    mov r0, #1
    bl native_fn_0206258c
    b L_021e0444
    mov r0, #2
    mov r2, r0
    str r0, [sp]
    mov r4, #30
    mov r1, #1
    mov r3, #38
    str r4, [sp, #0x4]
    bl native_fn_021dea9c
    mov r0, #44
    bl native_fn_021e00bc
    mov r0, #6
    bl native_fn_021dfd70
    mov r0, #2
    bl native_fn_021d77e8
    mov r0, #1
    bl native_fn_01ff8580
    mov r0, #1
    bl native_fn_0206258c
    b L_021e0444
    mov r2, #2
    str r2, [sp]
    mov r4, #28
    mov r0, #5
    mov r1, #1
    mov r3, #30
    str r4, [sp, #0x4]
    bl native_fn_021dea9c
    mov r0, #43
    bl native_fn_021e00bc
    mov r0, #2
    bl native_fn_021d77e8
    mov r0, #1
    bl native_fn_01ff8580
    mov r0, #1
    bl native_fn_0206258c
    b L_021e0444
    bl native_fn_02068510
    cmp r0, #1
    bne L_021e0250
    mov r0, #26
    bl native_fn_021e00bc
    bl native_fn_021dee68
    mov r0, #15
    mov r1, #4
    mov r2, #54
    bl native_fn_021ded5c
    mov r0, #2
    bl native_fn_021d77e8
    b L_021e0444
L_021e0250:
    mov r2, #2
    str r2, [sp]
    mov r4, #28
    mov r0, #5
    mov r1, #3
    mov r3, #30
    str r4, [sp, #0x4]
    bl native_fn_021dea9c
    mov r0, #43
    bl native_fn_021e00bc
    mov r0, #2
    bl native_fn_021d77e8
    b L_021e0444
    bl native_fn_02068510
    cmp r0, #1
    bne L_021e02e4
    bl native_fn_0206442c
    ldrh r0, [r0]
    cmp r0, #0
    bne L_021e02c0
    mov r0, #25
    bl native_fn_021e00bc
    bl native_fn_021dee68
    mov r0, #15
    mov r1, #4
    mov r2, #53
    bl native_fn_021ded5c
    b L_021e0444
L_021e02c0:
    bl native_fn_021da9d0
    mov r0, #26
    bl native_fn_021e00bc
    bl native_fn_021dee68
    mov r0, #15
    mov r1, #4
    mov r2, #54
    bl native_fn_021ded5c
    b L_021e0444
L_021e02e4:
    mov r1, #2
    mov r2, r1
    str r1, [sp]
    mov r4, #28
    mov r0, #5
    mov r3, #30
    str r4, [sp, #0x4]
    bl native_fn_021dea9c
    mov r0, #43
    bl native_fn_021e00bc
    bl native_fn_021da9d0
    b L_021e0444
L_021e0314:
    mov r0, #2
    bl native_fn_021d77e8
    mov r2, #2
    str r2, [sp]
    mov r3, #14
    mov r0, #5
    mov r1, #0
    str r3, [sp, #0x4]
    bl native_fn_021dea9c
    mov r0, #35
    bl native_fn_021e00bc
    mov r0, #33
    bl native_fn_021df524
    b L_021e0444
    mov r1, #3
    mov r2, r1
    mov r0, #15
    bl native_fn_021ded5c
    mov r0, #1
    bl native_fn_021def28
    mov r0, #0
    bl native_fn_01ff8604
    mov r0, #2
    bl native_fn_02064488
    mov r0, #30
    bl native_fn_021e00bc
    b L_021e0444
L_021e0380:
    mov r0, #0
    bl native_fn_02068500
    bl native_fn_02067748
    mov r1, #0
    mov r2, #56
    bl native_fn_02008d78
    mov r0, #15
    mov r1, #4
    mov r2, #38
    bl native_fn_021ded5c
    mov r0, #1
    bl native_fn_021def28
    mov r0, #0
    bl native_fn_021e00bc
    bl native_fn_02067c08
    mov r4, r0
    bl native_fn_021da3b0
    add r1, r4, #60
    mov r2, r0
    mov r0, #3
    mov r3, #98304
    bl native_fn_021df974
    mov r0, #0
    bl native_fn_01ff8580
    bl native_fn_021d83c8
    bl native_fn_0206344c
    bl native_fn_021d83e4
    mov r0, #1
    bl native_fn_01ff8580
    bl native_fn_020678d4
    bl native_fn_02067914
    bl native_fn_02067978
    bl native_fn_020679c0
    bl native_fn_02067a00
    bl native_fn_02067b70
    bl native_fn_021e2f38
    mov r1, #0
    mov r2, #24
    bl native_fn_02008d78
    bl native_fn_02067a4c
    bl native_fn_020679f0
    mov r1, #0
    str r1, [r0]
    bl native_fn_020679f0
    mov r1, #0
    str r1, [r0, #0x4]
    bl native_fn_020679f0
    mov r1, #0
    str r1, [r0, #0x38]
L_021e0444:
    mov r0, #0
    bl native_fn_020642cc
    add sp, sp, #8
    ldmia sp!, {r4, pc}
}
