/* ov000 row 0x021d72cc: 644 bytes.
 *
 * What it does: 156 instructions and 20 call(s), then a 7-entry dispatch through an inline branch table at 0x021d72e4 (dispatch word at 0x021d72dc)
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

extern void native_fn_02041510(void);
extern void native_fn_0205e7a8(void);
extern void native_fn_021d813c(void);
extern void native_fn_021d82e0(void);
extern void native_fn_020414b0(void);
extern void native_fn_02041800(void);
extern void native_fn_02048360(void);
extern void native_fn_02048308(void);
extern void native_fn_020273f0(void);
extern void native_fn_02041764(void);
extern void native_fn_02048a44(void);
extern void native_fn_021d7ef8(void);
extern u8 native_data_0222e120[];


asm u32 native_ov000_021d72cc (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r0, [pc, #0x264]
    ldr r0, [r0, #0x4]
    cmp r0, #6
    addls pc, pc, r0, lsl #2
    b L_021d7504
    dcd 0xea000005
    dcd 0xea000014
    dcd 0xea000047
    dcd 0xea000054
    dcd 0xea000060
    dcd 0xea00006f
    dcd 0xea00007b
    mov r0, #0
    mov r1, #2
    mov r2, #10
    bl native_fn_02041510
    mov r3, #3
    ldr r0, [pc, #0x220]
    mov r12, #1
    ldr r2, [pc, #0x21c]
    mov r1, #192
    str r12, [r0, #0x4]
    str r1, [r2, #0x24]
    sub r0, r3, #4
    mov r1, #532
    str r3, [r2, #0x4]
    bl native_fn_0205e7a8
    b L_021d7504
    ldr r2, [pc, #0x1f8]
    ldr r1, [r2, #0x4]
    ldr r3, [r2, #0x24]
    add r0, r1, #1
    subs r1, r3, r1, asr #1
    str r1, [r2, #0x24]
    str r0, [r2, #0x4]
    bpl L_021d73e4
    mov r0, #0
    str r0, [r2, #0x24]
    ldr r12, [r2, #0x14]
    sub r0, r0, #1
    ldr r3, [r12, #0x7c]
    mov r1, #147
    orr r3, r3, #2
    str r3, [r12, #0x7c]
    ldr r12, [r2, #0x10]
    ldr r3, [r12, #0x7c]
    orr r3, r3, #2
    str r3, [r12, #0x7c]
    ldr r12, [r2, #0x28]
    ldr r3, [r12, #0x7c]
    orr r3, r3, #2
    str r3, [r12, #0x7c]
    ldr r12, [r2, #0x2c]
    ldr r3, [r12, #0x7c]
    orr r3, r3, #2
    str r3, [r12, #0x7c]
    ldr r3, [r2, #0x8]
    ldr r2, [r3, #0x7c]
    orr r2, r2, #2
    str r2, [r3, #0x7c]
    bl native_fn_0205e7a8
    mov r2, #67108864
    ldr r1, [r2]
    ldr r0, [pc, #0x168]
    bic r1, r1, #7936
    orr r1, r1, #7936
    str r1, [r2]
    mov r1, #2
    str r1, [r0, #0x4]
L_021d73e4:
    ldr r1, [pc, #0x154]
    ldr r0, [pc, #0x154]
    ldr r3, [r1, #0x24]
    ldr r2, [pc, #0x150]
    and r3, r3, r0
    str r3, [r2]
    ldr r1, [r1, #0x24]
    rsb r1, r1, #0
    and r0, r1, r0
    str r0, [r2, #0x4]
    b L_021d7504
    bl native_fn_021d813c
    cmp r0, #1
    bne L_021d7504
    bl native_fn_021d82e0
    ldr r1, [pc, #0x114]
    mov r2, #3
    mov r0, #33
    str r2, [r1, #0x4]
    bl native_fn_020414b0
    mov r0, #1
    mov r1, #2
    mov r2, #30
    bl native_fn_02041510
    b L_021d7504
    bl native_fn_02041800
    cmp r0, #1
    beq L_021d7504
    ldr r1, [pc, #0xe0]
    mov r2, #4
    mov r0, #63
    str r2, [r1, #0x4]
    bl native_fn_020414b0
    mov r0, #1
    mov r1, #3
    mov r2, #90
    bl native_fn_02041510
    b L_021d7504
    bl native_fn_02041800
    cmp r0, #1
    beq L_021d7504
    mov r1, #67108864
    ldr r0, [r1]
    ldr r3, [pc, #0xa4]
    bic r0, r0, #7936
    orr r0, r0, #256
    str r0, [r1]
    mov r12, #5
    mov r0, #0
    mov r1, #3
    mov r2, #45
    str r12, [r3, #0x4]
    bl native_fn_02041510
    b L_021d7504
    bl native_fn_02041800
    cmp r0, #1
    beq L_021d7504
    bl native_fn_02048360
    bl native_fn_02048308
    ldr r3, [pc, #0x64]
    mov r12, #6
    mov r0, #1
    mov r1, #2
    mov r2, #45
    str r12, [r3, #0x4]
    bl native_fn_02041510
    b L_021d7504
    bl native_fn_020273f0
    cmp r0, #0
    moveq r0, #2
    movne r0, #14
    ldmia sp!, {r3, pc}
L_021d7504:
    bl native_fn_02041764
    ldr r0, [pc, #0x30]
    mov r1, #1
    ldr r0, [r0, #0x8]
    add r0, r0, #8
    bl native_fn_02048a44
    ldr r0, [pc, #0x1c]
    ldr r0, [r0, #0x24]
    bl native_fn_021d7ef8
    ldr r0, [pc, #0x1c]
    mov r1, #1
    str r1, [r0, #0x540]
    mov r0, #14
    ldmia sp!, {r3, pc}
    dcd native_data_0222e120
    dcd 0x022300c0
    dcd 0x000001ff
    dcd 0x04000014
    dcd 0x020feae8
}
