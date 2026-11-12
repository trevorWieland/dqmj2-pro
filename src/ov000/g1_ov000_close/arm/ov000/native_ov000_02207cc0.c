/* ov000 row 0x02207cc0: 944 bytes.
 *
 * What it does: 231 instructions and 34 call(s), then a 13-entry dispatch through an inline branch table at 0x02207ce8 (dispatch word at 0x02207ce0)
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
extern void native_fn_022061a0(void);
extern void native_fn_02206ae8(void);
extern void native_fn_02206868(void);
extern void native_fn_022069d8(void);
extern void native_fn_02041538(void);
extern void native_fn_02208938(void);
extern void native_fn_02041814(void);
extern void native_fn_020491f8(void);
extern void native_fn_0205e7a8(void);
extern void native_fn_02208070(void);
extern void native_fn_02208154(void);
extern void native_fn_0207e340(void);
extern void native_fn_02206db8(void);
extern void native_fn_0220895c(void);
extern void native_fn_0207e3f8(void);
extern void native_fn_02206d58(void);
extern void native_fn_020c225c(void);
extern void native_fn_0205bf2c(void);
extern void native_fn_02205e80(void);
extern void native_fn_0203d138(void);
extern void native_fn_02205e70(void);
extern void native_fn_02206c1c(void);
extern void native_fn_02206c4c(void);
extern void native_fn_022082f4(void);
extern void native_fn_02208854(void);
extern u8 native_data_0222ba98[];


asm u32 native_ov000_02207cc0 (register u32 a0)
{
    stmdb sp!, {r4, r5, lr}
    sub sp, sp, #28
    bl native_fn_0202a634
    mov r5, r0
    ldr r0, [pc, #0x384]
    mov r4, #0
    ldrb r1, [r0, #0xf0]
    cmp r1, #12
    addls pc, pc, r1, lsl #2
    b L_02208030
    dcd 0xea00000b
    dcd 0xea000053
    dcd 0xea000059
    dcd 0xea00006d
    dcd 0xea00009a
    dcd 0xea0000cb
    dcd 0xea00009b
    dcd 0xea0000a6
    dcd 0xea0000c8
    dcd 0xea0000c7
    dcd 0xea0000a6
    dcd 0xea0000b8
    dcd 0xea0000be
    bl native_fn_022061a0
    ldr r1, [pc, #0x338]
    mov r4, r0
    ldrh r2, [r1, #2]
    ldrh r1, [r1]
    mov r0, #4
    strh r2, [sp, #26]
    strh r1, [sp, #24]
    str r0, [sp]
    mov r0, #12
    str r0, [sp, #0x4]
    ldr r12, [pc, #0x314]
    ldr r0, [pc, #0x308]
    add r2, sp, #24
    mov r1, #2
    mov r3, #1
    str r12, [sp, #0x8]
    bl native_fn_02206ae8
    mov r1, #1
    str r1, [sp]
    mov r0, #16
    str r0, [sp, #0x4]
    mov r3, #2
    str r3, [sp, #0x8]
    mov r0, #0
    str r0, [sp, #0xc]
    ldr r12, [pc, #0x2d8]
    str r1, [sp, #0x10]
    mov r0, #7
    mov r2, #127
    str r12, [sp, #0x14]
    bl native_fn_02206868
    mov r0, #0
    str r0, [sp]
    mov r0, #7
    mov r1, #5
    mov r2, #2
    mov r3, #52
    bl native_fn_022069d8
    mov r0, r4, lsl #1
    rsb r4, r0, #17
    add r0, r0, #6
    and r1, r0, #255
    ldr r3, [pc, #0x298]
    mov r2, #2
    strh r2, [r3, #26]
    strh r4, [r3, #28]
    ldrsh r12, [r3, #28]
    mov r4, #28
    mov r0, #0
    and r12, r12, #255
    str r12, [sp]
    str r4, [sp, #0x4]
    str r1, [sp, #0x8]
    str r0, [sp, #0xc]
    mov r1, #1
    ldr r4, [pc, #0x260]
    str r1, [sp, #0x10]
    str r4, [sp, #0x14]
    ldrsh r3, [r3, #26]
    mov r0, #8
    and r3, r3, #255
    bl native_fn_02206868
    mov r0, #0
    mov r1, #2
    mov r2, #10
    bl native_fn_02041538
    mov r0, #1
    bl native_fn_02208938
    ldr r0, [pc, #0x224]
    mov r4, #1
    strb r4, [r0, #0xf0]
    b L_02208030
    bl native_fn_02041814
    cmp r0, #1
    beq L_02208030
    ldr r0, [pc, #0x208]
    mov r1, #2
    strb r1, [r0, #0xf0]
    b L_02208030
    bl native_fn_020491f8
    cmp r0, #0
    beq L_02207e7c
    mvn r0, #0
    mov r1, #85
    bl native_fn_0205e7a8
    mov r4, #1
    b L_02208030
L_02207e7c:
    ldrh r0, [r5, #2]
    tst r0, #1
    beq L_02207e98
    bl native_fn_02208070
    cmp r0, #0
    movne r4, #1
    b L_02208030
L_02207e98:
    tst r0, #2
    beq L_02208030
    bl native_fn_02208154
    cmp r0, #0
    movne r4, #1
    b L_02208030
    ldrb r1, [r0, #0x118]
    add r2, r1, #1
    and r1, r2, #255
    strb r2, [r0, #0x118]
    cmp r1, #30
    blo L_02208030
    bl native_fn_0207e340
    cmp r0, #0
    beq L_02208030
    mov r0, r4
    bl native_fn_02206db8
    mov r0, r4
    bl native_fn_0220895c
    bl native_fn_0207e3f8
    cmp r0, #7
    addls pc, pc, r0, lsl #2
    b L_02207f54
    b L_02207f14
    b L_02207f54
    b L_02207f44
    b L_02207f54
    b L_02207f54
    b L_02207f54
    b L_02207f54
    b L_02207f54
L_02207f14:
    mov r3, r4
    str r3, [sp]
    mov r4, #87
    mov r0, #5
    mov r1, #6
    mov r2, #31
    str r4, [sp, #0x4]
    bl native_fn_02206d58
    ldr r0, [pc, #0x120]
    mov r1, #6
    strb r1, [r0, #0xf0]
    b L_02207f60
L_02207f44:
    ldr r0, [pc, #0x110]
    mov r1, #4
    strb r1, [r0, #0xf0]
    b L_02207f60
L_02207f54:
    ldr r0, [pc, #0x100]
    mov r1, #7
    strb r1, [r0, #0xf0]
L_02207f60:
    mov r4, #1
    b L_02208030
    mov r0, #1342177280
    bl native_fn_020c225c
    b L_02208030
    ldrh r2, [r5, #2]
    ldr r1, [pc, #0xec]
    tst r2, r1
    beq L_02208030
    mov r1, #10
    strb r1, [r0, #0xf0]
    mov r0, #1
    bl native_fn_02208938
    mov r0, #1
    bl native_fn_02206db8
    mov r4, #1
    b L_02208030
    mov r0, #1610612736
    bl native_fn_020c225c
    b L_02208030
    bl native_fn_02041814
    cmp r0, #1
    beq L_02208030
    mov r0, #1
    mov r1, #2
    mov r2, #10
    bl native_fn_02041538
    mov r0, #4
    bl native_fn_0205bf2c
    mov r0, #11
    bl native_fn_02205e80
    mov r0, #1
    bl native_fn_0203d138
    mov r0, r4
    bl native_fn_02205e70
    ldr r0, [pc, #0x68]
    mov r1, #11
    strb r1, [r0, #0xf0]
    b L_02208030
    bl native_fn_02041814
    cmp r0, #1
    beq L_02208030
    ldr r0, [pc, #0x4c]
    mov r1, #12
    strb r1, [r0, #0xf0]
    b L_02208030
    ldr r0, [pc, #0x44]
    bl native_fn_02206c1c
    ldr r0, [pc, #0x34]
    add sp, sp, #28
    ldrb r0, [r0, #0xf1]
    ldmia sp!, {r4, r5, pc}
L_02208030:
    cmp r4, #0
    beq L_02208044
    ldr r0, [pc, #0x1c]
    bl native_fn_02206c4c
    bl native_fn_022082f4
L_02208044:
    ldr r0, [pc, #0x10]
    mov r1, #1
    bl native_fn_02208854
    mov r0, #3
    add sp, sp, #28
    ldmia sp!, {r4, r5, pc}
    dcd 0x022383e8
    dcd native_data_0222ba98
    dcd 0x022384e4
    dcd 0x022384e8
    dcd 0x00000ff7
}
