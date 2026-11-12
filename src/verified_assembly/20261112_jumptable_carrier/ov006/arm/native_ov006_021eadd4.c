/* ov006 row 0x021eadd4: 500 bytes.
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

extern void native_fn_021e71b0(void);
extern void native_fn_0202a1e0(void);
extern void native_fn_02002c98(void);
extern void native_fn_02008c58(void);
extern void native_fn_020414b0(void);
extern void native_fn_02046150(void);
extern void native_fn_02061238(void);
extern void native_fn_021e9e8c(void);
extern void native_fn_0206dcd0(void);
extern void native_fn_02041510(void);
extern void native_fn_02041560(void);


asm u32 native_ov006_021eadd4 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldr r0, [pc, #0x1d8]
    ldr r1, [r0, #0x3c]
    cmp r1, #5
    addls pc, pc, r1, lsl #2
    b L_021eafb0
    dcd 0xea000004
    dcd 0xea000008
    dcd 0xea00004b
    dcd 0xea000050
    dcd 0xea00005b
    dcd 0xea000066
    bl native_fn_021e71b0
    ldr r0, [pc, #0x1a8]
    mov r1, #1
    str r1, [r0, #0x3c]
    b L_021eafb0
    mov r0, #2
    bl native_fn_0202a1e0
    mov r4, r0
    mov r0, #1
    mov r1, #3
    mov r2, #0
    bl native_fn_02002c98
    ldr r3, [pc, #0x180]
    mov r0, #0
    ldrh r12, [r3]
    mov r1, #100663296
    mov r2, #524288
    and r12, r12, #67
    orr r12, r12, #792
    strh r12, [r3]
    ldrh r12, [r3, #2]
    and r12, r12, #67
    orr r12, r12, #264
    strh r12, [r3, #2]
    ldrh r12, [r3, #4]
    and r12, r12, #67
    orr r12, r12, #528
    strh r12, [r3, #4]
    ldrh r12, [r3, #6]
    and r12, r12, #67
    orr r12, r12, #132
    orr r12, r12, #18432
    strh r12, [r3, #6]
    bl native_fn_02008c58
    mov r2, #67108864
    ldr r1, [r2]
    mov r0, #40
    bic r1, r1, #7936
    orr r1, r1, #7936
    str r1, [r2]
    bl native_fn_020414b0
    ldr r3, [pc, #0x110]
    mov r0, #0
    ldrh r2, [r3]
    sub lr, r3, #2
    mov r1, r0
    bic r2, r2, #3
    strh r2, [r3]
    ldrh r12, [r3, #4]
    mov r2, #2
    bic r12, r12, #3
    orr r12, r12, #3
    strh r12, [r3, #4]
    ldrh r12, [r3, #2]
    bic r12, r12, #3
    orr r12, r12, #2
    strh r12, [r3, #2]
    ldrh r12, [lr]
    bic r12, r12, #3
    orr r12, r12, #1
    strh r12, [lr]
    str r0, [r3, #0x12]
    bl native_fn_02046150
    mov r0, #1
    mov r1, #2
    mov r2, #0
    bl native_fn_02061238
    mov r0, r4
    bl native_fn_0202a1e0
    ldr r0, [pc, #0x98]
    mov r1, #2
    str r1, [r0, #0x3c]
    b L_021eafb0
    mov r0, #1
    bl native_fn_021e9e8c
    ldr r0, [pc, #0x80]
    mov r1, #3
    str r1, [r0, #0x3c]
    b L_021eafb0
    ldr r0, [r0, #0x24]
    ldr r1, [pc, #0x78]
    cmp r0, #0
    moveq r2, #1
    movne r2, #0
    mov r0, #132
    mla r0, r2, r0, r1
    bl native_fn_0206dcd0
    ldr r0, [pc, #0x50]
    mov r1, #4
    str r1, [r0, #0x3c]
    b L_021eafb0
    mov r0, #0
    mov r1, #2
    mov r2, #5
    bl native_fn_02041510
    mov r0, #10
    bl native_fn_02041560
    mov r0, #40
    bl native_fn_020414b0
    ldr r0, [pc, #0x20]
    mov r1, #5
    str r1, [r0, #0x3c]
    b L_021eafb0
    mov r1, #0
    str r1, [r0, #0x3c]
    mov r0, #1
    ldmia sp!, {r4, pc}
L_021eafb0:
    mov r0, #0
    ldmia sp!, {r4, pc}
    dcd 0x02219290
    dcd 0x04000008
    dcd 0x0400000a
    dcd 0x0221930c
}
