/* ov000 row 0x0220b308: 1604 bytes.
 *
 * What it does: 399 instructions and 64 call(s), then a 7-entry dispatch through an inline branch table at 0x0220b32c (dispatch word at 0x0220b324)
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

extern void native_fn_021e5f48(void);
extern void native_fn_0220a2a4(void);
extern void native_fn_021e5ef4(void);
extern void native_fn_020420c4(void);
extern void native_fn_021e5f10(void);
extern void native_fn_02002618(void);
extern void native_fn_021e5ed8(void);
extern void native_fn_02025a28(void);
extern void native_fn_02025578(void);
extern void native_fn_02025ab8(void);
extern void native_fn_020280fc(void);
extern void native_fn_021e5f2c(void);
extern void native_fn_02042464(void);
extern void native_fn_02042bfc(void);
extern void native_fn_02042c2c(void);
extern void native_fn_021e5f88(void);
extern void native_fn_02028158(void);
extern void native_fn_021e5f6c(void);
extern void native_fn_02041f90(void);
extern void native_fn_021e07b8(void);
extern void native_fn_02041f74(void);
extern void native_fn_020028d8(void);
extern void native_fn_0200235c(void);
extern void native_fn_02042104(void);
extern void native_fn_021e5fa4(void);
extern void native_fn_0205cba4(void);


asm u32 native_ov000_0220b308 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    sub sp, sp, #24
    mov r5, r0
    ldrb r0, [r5, #0x2c0]
    ldr r4, [pc, #0x624]
    bl native_fn_021e5f48
    cmp r0, #6
    addls pc, pc, r0, lsl #2
    b L_0220b92c
    dcd 0xea000005
    dcd 0xea00006b
    dcd 0xea00008e
    dcd 0xea00017b
    dcd 0xea0000ad
    dcd 0xea00010f
    dcd 0xea00015a
    ldrb r0, [r5, #0x279]
    cmp r0, #0
    bne L_0220b394
    mov r0, r5
    mov r1, #1
    mov r2, #0
    bl native_fn_0220a2a4
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5ef4
    add r3, sp, #12
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    mov r0, r5
    mov r1, r3
    bl native_fn_020420c4
    mov r0, #1
    strb r0, [r5, #0x2c1]
    mov r0, #10
    strb r0, [r5, #0x279]
L_0220b394:
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5ef4
    add r3, sp, #12
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    add r0, r5, #512
    ldrsh r0, [r0, #122]
    tst r0, #3
    bne L_0220b424
    ldr r1, [r5, #0x74]
    ldr r0, [sp, #0x10]
    ldr r6, [r5, #0x70]
    sub r2, r1, r0
    smull r0, r1, r2, r2
    ldr r2, [sp, #0xc]
    ldr r3, [r5, #0x78]
    sub r6, r6, r2
    ldr r2, [sp, #0x14]
    smlal r0, r1, r6, r6
    sub r2, r3, r2
    smlal r0, r1, r2, r2
    mov r0, r0, lsr #12
    orr r0, r0, r1, lsl #20
    subs r0, r0, #4096
    mov r0, #0
    rscs r0, r0, r1, asr #12
    bge L_0220b424
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5f10
    cmp r0, #255
    beq L_0220b424
    mov r1, #0
    strb r1, [r5, #0x279]
    add sp, sp, #24
    strb r0, [r5, #0x2c0]
    ldmia sp!, {r4, r5, r6, pc}
L_0220b424:
    add r1, sp, #12
    mov r0, r5
    bl native_fn_020420c4
    ldr r2, [sp, #0xc]
    ldr r0, [r5, #0x70]
    ldr r1, [sp, #0x10]
    sub r0, r2, r0
    str r0, [sp, #0xc]
    ldr r0, [r5, #0x74]
    ldr r2, [sp, #0x14]
    sub r0, r1, r0
    str r0, [sp, #0x10]
    ldr r1, [r5, #0x78]
    add r0, sp, #12
    sub r2, r2, r1
    add r1, sp, #0
    str r2, [sp, #0x14]
    bl native_fn_02002618
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5ed8
    ldr r0, [r0]
    bl native_fn_02025a28
    ldr r1, [pc, #0x4c4]
    bl native_fn_02025578
    mov r1, r0
    mov r0, r4
    bl native_fn_02025ab8
    mov r2, r0
    add r0, sp, #0
    mov r1, r0
    bl native_fn_020280fc
    ldr r1, [r5, #0x70]
    ldr r0, [sp]
    add r2, r5, #112
    add r0, r1, r0
    str r0, [r5, #0x70]
    ldr r1, [r5, #0x74]
    ldr r0, [sp, #0x4]
    add r3, r5, #272
    add r0, r1, r0
    str r0, [r5, #0x74]
    ldr r1, [r5, #0x78]
    ldr r0, [sp, #0x8]
    add r0, r1, r0
    str r0, [r5, #0x78]
    ldmia r2, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    b L_0220b92c
    ldrb r0, [r5, #0x279]
    cmp r0, #0
    bne L_0220b524
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5f2c
    mov r1, r0
    mov r0, r5
    mov r2, #1
    bl native_fn_02042464
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5ed8
    ldr r1, [r0]
    mov r0, r5
    bl native_fn_02042bfc
    mov r0, #10
    strb r0, [r5, #0x279]
L_0220b524:
    ldrb r0, [r5, #0x279]
    cmp r0, #10
    bne L_0220b92c
    ldr r1, [r5, #0x60]
    ldr r0, [r1, #0x8]
    ldr r1, [r1]
    ldrh r0, [r0, #4]
    mov r0, r0, lsl #12
    sub r0, r0, #1
    cmp r1, r0
    blt L_0220b92c
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5f10
    cmp r0, #255
    beq L_0220b92c
    mov r1, #0
    strb r1, [r5, #0x279]
    add sp, sp, #24
    strb r0, [r5, #0x2c0]
    ldmia sp!, {r4, r5, r6, pc}
    ldrb r0, [r5, #0x279]
    cmp r0, #0
    bne L_0220b5b8
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5ed8
    ldr r1, [r0]
    mov r0, r5
    bl native_fn_02042bfc
    mov r1, #0
    mov r0, r5
    mov r2, r1
    bl native_fn_0220a2a4
    add r0, r5, #512
    mov r1, #0
    strh r1, [r0, #122]
    mov r0, #10
    strb r0, [r5, #0x279]
L_0220b5b8:
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5f2c
    add r1, r5, #512
    ldrsh r1, [r1, #122]
    mov r0, r0, lsl #16
    cmp r1, r0, asr #16
    ble L_0220b92c
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5f10
    cmp r0, #255
    beq L_0220b92c
    mov r1, #0
    strb r1, [r5, #0x279]
    add sp, sp, #24
    strb r0, [r5, #0x2c0]
    ldmia sp!, {r4, r5, r6, pc}
    ldrb r0, [r5, #0x279]
    cmp r0, #0
    bne L_0220b630
    mov r0, r5
    mov r1, #1
    mov r2, #0
    bl native_fn_0220a2a4
    mov r1, #1
    mov r0, r5
    strb r1, [r5, #0x2c1]
    mov r1, #10
    strb r1, [r5, #0x279]
    bl native_fn_02042c2c
    str r0, [r5, #0x27c]
L_0220b630:
    add r0, r5, #512
    ldrsh r0, [r0, #122]
    tst r0, #3
    bne L_0220b698
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5f88
    movs r6, r0
    mov r0, r5
    rsbmi r6, r6, #0
    bl native_fn_02042c2c
    ldr r1, [r5, #0x27c]
    sub r0, r0, r1
    bl native_fn_02028158
    cmp r0, #0
    rsblt r0, r0, #0
    cmp r0, r6
    blt L_0220b698
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5f10
    cmp r0, #255
    beq L_0220b698
    mov r1, #0
    strb r1, [r5, #0x279]
    add sp, sp, #24
    strb r0, [r5, #0x2c0]
    ldmia sp!, {r4, r5, r6, pc}
L_0220b698:
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5f6c
    mov r6, r0
    mov r0, r5
    bl native_fn_02042c2c
    add r0, r6, r0
    bl native_fn_02028158
    mov r1, r0
    mov r0, r5
    mov r2, #1
    bl native_fn_02041f90
    mov r0, r5
    add r1, sp, #12
    bl native_fn_020420c4
    ldr r2, [sp, #0xc]
    ldr r0, [r5, #0x70]
    ldr r1, [sp, #0x10]
    sub r0, r2, r0
    str r0, [sp, #0xc]
    ldr r0, [r5, #0x74]
    ldr r2, [sp, #0x14]
    sub r0, r1, r0
    str r0, [sp, #0x10]
    ldr r1, [r5, #0x78]
    add r0, sp, #12
    sub r1, r2, r1
    str r1, [sp, #0x14]
    add r1, sp, #0
    bl native_fn_02002618
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5ed8
    ldr r0, [r0]
    bl native_fn_02025a28
    ldr r1, [pc, #0x224]
    bl native_fn_02025578
    mov r1, r0
    mov r0, r4
    bl native_fn_02025ab8
    mov r2, r0
    add r0, sp, #0
    mov r1, r0
    bl native_fn_020280fc
    ldr r1, [r5, #0x70]
    ldr r0, [sp]
    add r2, r5, #112
    add r0, r1, r0
    str r0, [r5, #0x70]
    ldr r1, [r5, #0x74]
    ldr r0, [sp, #0x4]
    add r3, r5, #272
    add r0, r1, r0
    str r0, [r5, #0x74]
    ldr r1, [r5, #0x78]
    ldr r0, [sp, #0x8]
    add r0, r1, r0
    str r0, [r5, #0x78]
    ldmia r2, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    b L_0220b92c
    ldrb r0, [r5, #0x279]
    cmp r0, #0
    bne L_0220b82c
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5ed8
    ldr r1, [r0]
    mov r0, r5
    bl native_fn_02042bfc
    mov r0, #0
    bl native_fn_021e07b8
    mov r4, r0
    mov r0, r5
    mov r1, #0
    bl native_fn_02041f74
    ldr r2, [r0]
    ldr r3, [r4]
    mov r0, r5
    mov r1, #0
    sub r6, r3, r2
    bl native_fn_02041f74
    mov r0, #0
    bl native_fn_021e07b8
    mov r0, #0
    bl native_fn_021e07b8
    mov r4, r0
    mov r0, r5
    mov r1, #0
    bl native_fn_02041f74
    ldr r1, [r0, #0x8]
    ldr r2, [r4, #0x8]
    mov r0, r6
    sub r1, r2, r1
    bl native_fn_020028d8
    str r0, [r5, #0x27c]
    mov r1, #71
    bl native_fn_0200235c
    str r0, [r5, #0x27c]
    mov r1, #0
    add r0, r5, #512
    strh r1, [r0, #122]
    mov r0, #10
    strb r0, [r5, #0x279]
L_0220b82c:
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5f6c
    mov r4, r0
    mov r0, r5
    bl native_fn_02042c2c
    ldr r1, [r5, #0x27c]
    mov r6, r0
    subs r0, r6, r1
    rsbmi r0, r0, #0
    cmp r0, #40960
    bge L_0220b87c
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5f10
    cmp r0, #255
    beq L_0220b87c
    mov r1, #0
    strb r1, [r5, #0x279]
    add sp, sp, #24
    strb r0, [r5, #0x2c0]
    ldmia sp!, {r4, r5, r6, pc}
L_0220b87c:
    ldr r0, [r5, #0x27c]
    add r0, r0, #1474560
    sub r0, r0, r6
    bl native_fn_02028158
    cmp r0, #0
    mov r0, r5
    mov r2, #0
    ble L_0220b8a8
    mov r1, r4
    bl native_fn_02042104
    b L_0220b92c
L_0220b8a8:
    rsb r1, r4, #0
    bl native_fn_02042104
    b L_0220b92c
    ldrb r0, [r5, #0x279]
    cmp r0, #0
    bne L_0220b8fc
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5f2c
    mov r4, r0
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5fa4
    mov r2, r0, lsl #24
    mov r0, r4
    mov r1, r5
    mov r2, r2, asr #24
    bl native_fn_0205cba4
    add r0, r5, #512
    mov r1, #0
    strh r1, [r0, #122]
    mov r0, #10
    strb r0, [r5, #0x279]
L_0220b8fc:
    ldrb r0, [r5, #0x279]
    cmp r0, #10
    bne L_0220b92c
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5f10
    cmp r0, #255
    beq L_0220b92c
    mov r1, #0
    strb r1, [r5, #0x279]
    add sp, sp, #24
    strb r0, [r5, #0x2c0]
    ldmia sp!, {r4, r5, r6, pc}
L_0220b92c:
    add r0, r5, #512
    ldrsh r1, [r0, #122]
    add r1, r1, #1
    strh r1, [r0, #122]
    add sp, sp, #24
    ldmia sp!, {r4, r5, r6, pc}
    dcd 0x3dcccccd
    dcd 0x45800000
}
