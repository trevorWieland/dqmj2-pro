/* ov000 row 0x021eaaac: 732 bytes.
 *
 * What it does: 181 instructions and 32 call(s), then a 8-entry dispatch through an inline branch table at 0x021eaadc (dispatch word at 0x021eaad4)
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

extern void native_fn_021ea848(void);
extern void native_fn_021ea588(void);
extern void native_fn_02042c0c(void);
extern void native_fn_021ea8d4(void);
extern void native_fn_020282a8(void);
extern void native_fn_020283dc(void);
extern void native_fn_020283fc(void);
extern void native_fn_0205caf4(void);
extern void native_fn_0205f35c(void);
extern void native_fn_0206157c(void);
extern void native_fn_021ea960(void);
extern void native_fn_021ea9fc(void);
extern void native_fn_0205cf14(void);
extern void native_fn_0205cedc(void);
extern void native_fn_02041510(void);
extern void native_fn_02041800(void);
extern void native_fn_02044d14(void);
extern void native_fn_02044cdc(void);
extern void native_fn_021ea754(void);
extern void native_fn_021eae2c(void);
extern void native_fn_0205d718(void);


asm u32 native_ov000_021eaaac (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r0, [pc, #0x2c8]
    mov r4, #0
    ldrb r1, [r0, #0x6]
    cmp r1, #0
    movne r1, #7
    strneb r1, [r0, #0x4]
    ldr r0, [pc, #0x2b0]
    ldrsb r1, [r0, #4]
    cmp r1, #7
    addls pc, pc, r1, lsl #2
    b L_021ead78
    dcd 0xea000006
    dcd 0xea00002d
    dcd 0xea000034
    dcd 0xea000041
    dcd 0xea000056
    dcd 0xea00007f
    dcd 0xea000087
    dcd 0xea000097
    bl native_fn_021ea848
    ldr r1, [pc, #0x278]
    ldr r0, [r1, #0x18]
    add r0, r0, #256
    ldrsh r2, [r0, #242]
    strh r2, [r0, #240]
    ldr r1, [r1, #0x18]
    ldrb r0, [r1, #0x1f5]
    strb r0, [r1, #0x1f4]
    bl native_fn_021ea588
    ldr r0, [pc, #0x254]
    mov r1, #0
    ldr r0, [r0, #0x18]
    bl native_fn_02042c0c
    ldr r0, [pc, #0x244]
    mov r1, #1
    ldr r0, [r0, #0x20]
    bl native_fn_021ea8d4
    mov r0, #0
    mov r1, #40960
    bl native_fn_020282a8
    ldr r1, [pc, #0x228]
    mov r2, #43008
    str r0, [r1, #0x1c]
    mov r0, #0
    mov r1, r0
    mov r3, #204800
    bl native_fn_020283dc
    mov r0, #0
    mov r1, r0
    mov r2, #14336
    mov r3, r0
    bl native_fn_020283fc
    mov r2, #1
    ldr r0, [pc, #0x1f4]
    mov r1, #0
    strb r2, [r0, #0x7]
    strb r2, [r0, #0x4]
    strb r1, [r0, #0x3]
    b L_021ead78
    ldrb r1, [r0, #0x3]
    add r2, r1, #1
    and r1, r2, #255
    cmp r1, #10
    strb r2, [r0, #0x3]
    movhs r1, #2
    strhsb r1, [r0, #0x4]
    b L_021ead78
    mov r1, #0
    ldr r0, [pc, #0x1bc]
    mov r2, r1
    mov r3, r1
    bl native_fn_0205caf4
    ldr r2, [pc, #0x1a8]
    mov r1, #151
    str r0, [r2, #0x24]
    mvn r0, #0
    bl native_fn_0205f35c
    ldr r0, [pc, #0x194]
    mov r1, #3
    strb r1, [r0, #0x4]
    b L_021ead78
    bl native_fn_0206157c
    bl native_fn_021ea960
    bl native_fn_021ea9fc
    ldr r0, [pc, #0x178]
    ldr r0, [r0, #0x24]
    bl native_fn_0205cf14
    ldr r1, [pc, #0x16c]
    mov r5, r0
    ldr r0, [r1, #0x24]
    bl native_fn_0205cedc
    sub r0, r5, r0
    mov r0, r0, asr #12
    cmp r0, #30
    bge L_021ead78
    mov r0, #1
    mov r1, #3
    mov r2, #30
    bl native_fn_02041510
    ldr r0, [pc, #0x13c]
    mov r1, #4
    strb r1, [r0, #0x4]
    b L_021ead78
    bl native_fn_02041800
    cmp r0, #1
    beq L_021eace4
    ldr r0, [pc, #0x120]
    mov r1, #1
    ldr r0, [r0, #0x20]
    bl native_fn_021ea8d4
    ldr r1, [pc, #0x110]
    mov r0, #0
    ldr r1, [r1, #0x1c]
    bl native_fn_020282a8
    ldr r0, [pc, #0x100]
    mov r1, #31
    ldr r0, [r0, #0x18]
    bl native_fn_02042c0c
    ldr r0, [pc, #0xf0]
    ldr r0, [r0, #0x18]
    add r0, r0, #256
    ldrsh r0, [r0, #240]
    bl native_fn_02044d14
    mov r5, r0
    ldr r0, [pc, #0xd8]
    ldr r0, [r0, #0x18]
    add r0, r0, #256
    ldrsh r0, [r0, #240]
    bl native_fn_02044cdc
    str r5, [sp]
    mov r3, r0
    ldr r2, [pc, #0xbc]
    mov r1, #1
    ldr r0, [r2, #0x20]
    ldr r2, [r2, #0x18]
    add r2, r2, #480
    bl native_fn_021ea754
    mov r1, #5
    ldr r0, [pc, #0xa0]
    strb r1, [r0, #0x4]
    b L_021ead78
L_021eace4:
    bl native_fn_0206157c
    bl native_fn_021ea960
    bl native_fn_021ea9fc
    b L_021ead78
    mov r0, #0
    mov r1, #3
    mov r2, #30
    bl native_fn_02041510
    bl native_fn_021eae2c
    ldr r0, [pc, #0x70]
    mov r1, #6
    strb r1, [r0, #0x4]
    b L_021ead78
    bl native_fn_0206157c
    bl native_fn_021ea960
    bl native_fn_021ea9fc
    bl native_fn_02041800
    cmp r0, #1
    beq L_021ead78
    ldr r1, [pc, #0x48]
    mov r0, #1
    strb r0, [r1]
    ldr r0, [r1, #0x18]
    add r0, r0, #256
    ldrsh r2, [r0, #240]
    ldrsh r0, [r0, #242]
    cmp r2, r0
    movne r0, #7
    strneb r0, [r1, #0x4]
    b L_021ead78
    ldr r0, [r0, #0x24]
    bl native_fn_0205d718
    ldr r0, [pc, #0x14]
    mov r1, #0
    strb r1, [r0]
    strb r1, [r0, #0x4]
    mov r4, #1
L_021ead78:
    mov r0, r4
    ldmia sp!, {r3, r4, r5, pc}
    dcd 0x02236950
    dcd 0x000001b2
}
