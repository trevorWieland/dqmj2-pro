/* ov000 row 0x0220d074: 1016 bytes.
 *
 * What it does: 254 instructions and 42 call(s), then a 7-entry dispatch through an inline branch table at 0x0220d090 (dispatch word at 0x0220d088)
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
extern void native_fn_0220cbe0(void);
extern void native_fn_02209c68(void);
extern void native_fn_021e5f10(void);
extern void native_fn_021e5f2c(void);
extern void native_fn_02042464(void);
extern void native_fn_021e07b8(void);
extern void native_fn_02041f74(void);
extern void native_fn_020028d8(void);
extern void native_fn_0200235c(void);
extern void native_fn_021e5f6c(void);
extern void native_fn_02042c2c(void);
extern void native_fn_02028158(void);
extern void native_fn_02042104(void);
extern void native_fn_021e5fa4(void);
extern void native_fn_0205cba4(void);


asm u32 native_ov000_0220d074 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r5, r0
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5f48
    cmp r0, #6
    addls pc, pc, r0, lsl #2
    b L_0220d458
    dcd 0xea000005
    dcd 0xea00003e
    dcd 0xea000062
    dcd 0xea0000ed
    dcd 0xea0000ec
    dcd 0xea000081
    dcd 0xea0000cd
    ldrb r0, [r5, #0x279]
    cmp r0, #0
    bne L_0220d100
    mov r0, r5
    mov r1, #1
    mov r2, #0
    bl native_fn_0220a2a4
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5ef4
    mov r1, r0
    mov r0, r5
    bl native_fn_020420c4
    mov r1, #10
    mov r0, r5
    strb r1, [r5, #0x279]
    bl native_fn_0220cbe0
    cmp r0, #0
    bne L_0220d100
    mov r0, r5
    mov r1, #6
    bl native_fn_02209c68
L_0220d100:
    add r0, r5, #512
    ldrsh r0, [r0, #122]
    tst r0, #3
    bne L_0220d458
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5ef4
    mov r4, r0
    ldr r1, [r5, #0x74]
    ldr r0, [r4, #0x4]
    ldr r3, [r5, #0x70]
    sub r12, r1, r0
    ldr r1, [r4]
    smull r0, r2, r12, r12
    sub r1, r3, r1
    smlal r0, r2, r1, r1
    ldr r12, [r5, #0x78]
    ldr r3, [r4, #0x8]
    mov r1, #0
    sub r3, r12, r3
    smlal r0, r2, r3, r3
    mov r0, r0, lsr #12
    orr r0, r0, r2, lsl #20
    subs r0, r0, #4096
    rscs r0, r1, r2, asr #12
    bge L_0220d184
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5f10
    cmp r0, #255
    beq L_0220d184
    mov r1, #0
    strb r1, [r5, #0x279]
    strb r0, [r5, #0x2c0]
    ldmia sp!, {r4, r5, r6, pc}
L_0220d184:
    mov r0, r5
    mov r1, r4
    bl native_fn_020420c4
    b L_0220d458
    ldrb r0, [r5, #0x279]
    cmp r0, #0
    bne L_0220d1dc
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5f2c
    mov r1, r0
    mov r0, r5
    mov r2, #1
    bl native_fn_02042464
    mov r1, #10
    mov r0, r5
    strb r1, [r5, #0x279]
    bl native_fn_0220cbe0
    cmp r0, #0
    bne L_0220d1dc
    mov r0, r5
    mov r1, #6
    bl native_fn_02209c68
L_0220d1dc:
    ldrb r0, [r5, #0x279]
    cmp r0, #10
    bne L_0220d458
    ldr r1, [r5, #0x60]
    ldr r0, [r1, #0x8]
    ldr r1, [r1]
    ldrh r0, [r0, #4]
    mov r0, r0, lsl #12
    sub r0, r0, #1
    cmp r1, r0
    blt L_0220d458
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5f10
    cmp r0, #255
    beq L_0220d458
    mov r1, #0
    strb r1, [r5, #0x279]
    strb r0, [r5, #0x2c0]
    ldmia sp!, {r4, r5, r6, pc}
    ldrb r0, [r5, #0x279]
    cmp r0, #0
    bne L_0220d274
    mov r1, #0
    mov r0, r5
    mov r2, r1
    bl native_fn_0220a2a4
    add r1, r5, #512
    mov r2, #0
    mov r0, r5
    strh r2, [r1, #122]
    mov r1, #10
    strb r1, [r5, #0x279]
    bl native_fn_0220cbe0
    cmp r0, #0
    bne L_0220d274
    mov r0, r5
    mov r1, #6
    bl native_fn_02209c68
L_0220d274:
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5f2c
    add r1, r5, #512
    ldrsh r1, [r1, #122]
    mov r0, r0, lsl #16
    cmp r1, r0, asr #16
    ble L_0220d458
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5f10
    cmp r0, #255
    beq L_0220d458
    mov r1, #0
    strb r1, [r5, #0x279]
    strb r0, [r5, #0x2c0]
    ldmia sp!, {r4, r5, r6, pc}
    ldrb r0, [r5, #0x279]
    cmp r0, #0
    bne L_0220d360
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
    mov r0, r5
    bl native_fn_0220cbe0
    cmp r0, #0
    bne L_0220d360
    mov r0, r5
    mov r1, #6
    bl native_fn_02209c68
L_0220d360:
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
    bge L_0220d3ac
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5f10
    cmp r0, #255
    beq L_0220d3ac
    mov r1, #0
    strb r1, [r5, #0x279]
    strb r0, [r5, #0x2c0]
    ldmia sp!, {r4, r5, r6, pc}
L_0220d3ac:
    ldr r0, [r5, #0x27c]
    add r0, r0, #1474560
    sub r0, r0, r6
    bl native_fn_02028158
    cmp r0, #0
    mov r0, r5
    mov r2, #0
    ble L_0220d3d8
    mov r1, r4
    bl native_fn_02042104
    b L_0220d458
L_0220d3d8:
    rsb r1, r4, #0
    bl native_fn_02042104
    b L_0220d458
    ldrb r0, [r5, #0x279]
    cmp r0, #0
    bne L_0220d42c
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
L_0220d42c:
    ldrb r0, [r5, #0x279]
    cmp r0, #10
    bne L_0220d458
    ldrb r0, [r5, #0x2c0]
    bl native_fn_021e5f10
    cmp r0, #255
    beq L_0220d458
    mov r1, #0
    strb r1, [r5, #0x279]
    strb r0, [r5, #0x2c0]
    ldmia sp!, {r4, r5, r6, pc}
L_0220d458:
    add r0, r5, #512
    ldrsh r1, [r0, #122]
    add r1, r1, #1
    strh r1, [r0, #122]
    ldmia sp!, {r4, r5, r6, pc}
}
