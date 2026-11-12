/* ov000 row 0x021ecaa4: 1252 bytes.
 *
 * What it does: 310 instructions and 70 call(s), then a 5-entry dispatch through an inline branch table at 0x021ecaf0 (dispatch word at 0x021ecae8)
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

extern void native_fn_020c49e8(void);
extern void native_fn_021ee1b0(void);
extern void native_fn_021ef3a0(void);
extern void native_fn_021ef154(void);
extern void native_fn_021ef11c(void);
extern void native_fn_021ef808(void);
extern void native_fn_021efe60(void);
extern void native_fn_021ef97c(void);
extern void native_fn_02062b0c(void);
extern void native_fn_021efa14(void);
extern void native_fn_021ef17c(void);
extern void native_fn_021f0018(void);
extern void native_fn_021ef138(void);
extern void native_fn_020c4c58(void);
extern void native_fn_020c4c9c(void);
extern void native_fn_021edfdc(void);
extern void native_fn_021efbd0(void);
extern void native_fn_021ef8e0(void);
extern void native_fn_021f015c(void);
extern void native_fn_021ef1cc(void);
extern void native_fn_021ee300(void);
extern void native_fn_020620e8(void);
extern void native_fn_021ef878(void);
extern void native_fn_02062358(void);
extern void native_fn_02062aa0(void);
extern void native_fn_02062ad0(void);
extern void native_fn_02062a50(void);
extern void native_fn_0206dcd0(void);
extern u8 native_data_0222b8ca[];
extern u8 native_data_0222b8c4[];


asm u32 native_ov000_021ecaa4 (register u32 a0)
{
    stmdb sp!, {r3, r4, lr}
    sub sp, sp, #12
    bl native_fn_020c49e8
    ldr r0, [pc, #0x4c4]
    ldr r0, [r0, #0x4]
    ldrb r0, [r0, #0x20]
    bl native_fn_021ee1b0
    mov r0, #1
    bl native_fn_021ef3a0
    mov r0, #1
    bl native_fn_021ef154
    mov r0, #1
    bl native_fn_021ef11c
    ldr r0, [pc, #0x49c]
    ldr r1, [r0, #0x4]
    ldrsb r1, [r1, #32]
    cmp r1, #4
    addls pc, pc, r1, lsl #2
    b L_021ecf74
    dcd 0xea000003
    dcd 0xea000037
    dcd 0xea0000e2
    dcd 0xea00007e
    dcd 0xea0000ae
    ldrb r0, [r0]
    cmp r0, #0
    beq L_021ecb24
    cmp r0, #1
    beq L_021ecb30
    cmp r0, #2
    beq L_021ecb3c
    b L_021ecb44
L_021ecb24:
    mov r0, #17
    bl native_fn_021ef808
    b L_021ecb44
L_021ecb30:
    mov r0, #18
    bl native_fn_021ef808
    b L_021ecb44
L_021ecb3c:
    mov r0, #19
    bl native_fn_021ef808
L_021ecb44:
    mov r0, #0
    bl native_fn_021efe60
    mov r0, #0
    bl native_fn_021ef97c
    bl native_fn_02062b0c
    mov r1, #1
    bl native_fn_021efa14
    mov r0, #0
    bl native_fn_021ef17c
    mov r0, #4
    str r0, [sp]
    mov r0, #12
    str r0, [sp, #0x4]
    ldr r0, [pc, #0x3fc]
    ldr r2, [pc, #0x3fc]
    ldr r0, [r0, #0x4]
    mov r1, #3
    add r0, r0, #16
    mov r3, #1
    bl native_fn_021f0018
    mov r0, #96
    bl native_fn_021ef138
    mov r0, #0
    sub r1, r0, #1
    bl native_fn_020c4c58
    bl native_fn_020c4c9c
    ldr r0, [pc, #0x3c8]
    ldr r1, [r0, #0x4]
    add r0, r1, #16
    ldr r1, [r1, #0x510]
    bl native_fn_021edfdc
    ldr r0, [pc, #0x3b4]
    mov r1, #0
    ldr r0, [r0, #0x4]
    add sp, sp, #12
    str r1, [r0, #0x510]
    ldmia sp!, {r3, r4, pc}
    mov r0, #0
    bl native_fn_021ef808
    mov r0, #1
    bl native_fn_021ef97c
    bl native_fn_021efbd0
    mov r0, #1
    mov r1, #6
    mov r2, #28
    bl native_fn_021ef8e0
    ldr r0, [pc, #0x378]
    mov r4, #20
    ldr r2, [r0, #0x4]
    mov r3, #28
    ldrb r1, [r2, #0x504]
    cmp r1, #6
    movlo r0, r1
    movhs r0, #6
    and r0, r0, #255
    stmia sp, {r0, r1}
    add r0, r2, #16
    mov r1, #1
    mov r2, #7
    str r4, [sp, #0x8]
    bl native_fn_021f015c
    mov r0, #1
    bl native_fn_021efe60
    mov r0, #1
    bl native_fn_021ef17c
    mov r0, #0
    bl native_fn_021ef1cc
    mov r0, #224
    bl native_fn_021ef138
    bl native_fn_021ee300
    ldr r0, [pc, #0x318]
    ldr r0, [r0, #0x4]
    ldrb r0, [r0, #0x50b]
    cmp r0, #0
    bne L_021ecc8c
    mov r0, #9
    mov r1, #1
    bl native_fn_020620e8
    ldr r0, [pc, #0x2f8]
    mov r1, #1
    ldr r0, [r0, #0x4]
    strb r1, [r0, #0x50b]
L_021ecc8c:
    ldr r0, [pc, #0x2e8]
    ldr r0, [r0, #0x4]
    ldr r1, [r0, #0x514]
    add r0, r0, #16
    bl native_fn_021edfdc
    ldr r0, [pc, #0x2d4]
    mov r3, #0
    ldr r2, [r0, #0x4]
    sub r1, r3, #1
    str r3, [r2, #0x514]
    ldr r2, [r0, #0x4]
    ldr r0, [r2, #0x10]
    add r0, r2, r0, lsl #2
    ldr r0, [r0, #0x104]
    bl native_fn_020c4c58
    ldr r1, [pc, #0x2ac]
    mov r3, #0
    ldr r0, [r1, #0x4]
    mov r2, #1
    strb r3, [r0, #0x101]
    ldr r0, [r1, #0x4]
    add sp, sp, #12
    add r0, r0, #1280
    strh r2, [r0, #6]
    ldr r0, [r1, #0x4]
    add r0, r0, #1280
    strh r3, [r0, #8]
    ldmia sp!, {r3, r4, pc}
    mov r0, #0
    bl native_fn_021ef878
    mov r0, #1
    bl native_fn_021ef97c
    bl native_fn_021efbd0
    mov r0, #0
    bl native_fn_021efe60
    mov r0, #5
    str r0, [sp]
    mov r0, #28
    str r0, [sp, #0x4]
    ldr r0, [pc, #0x24c]
    mov r1, #3
    ldr r0, [r0, #0x4]
    ldr r2, [pc, #0x248]
    add r0, r0, #16
    mov r3, #1
    bl native_fn_021f0018
    mov r0, #0
    bl native_fn_021ef1cc
    mov r0, #0
    bl native_fn_021ef17c
    mov r0, #224
    bl native_fn_021ef138
    ldr r0, [pc, #0x218]
    ldr r0, [r0, #0x4]
    ldrb r0, [r0, #0x50b]
    cmp r0, #0
    bne L_021ecd94
    mov r0, #9
    mov r1, #1
    bl native_fn_020620e8
    mov r0, #1
    bl native_fn_02062358
    ldr r0, [pc, #0x1f0]
    mov r1, #1
    ldr r0, [r0, #0x4]
    strb r1, [r0, #0x50b]
L_021ecd94:
    ldr r0, [pc, #0x1e0]
    mvn r1, #0
    ldr r0, [r0, #0x4]
    ldr r0, [r0, #0x50c]
    bl native_fn_020c4c58
    ldr r0, [pc, #0x1cc]
    mov r1, #0
    ldr r0, [r0, #0x4]
    add sp, sp, #12
    strb r1, [r0, #0x101]
    ldmia sp!, {r3, r4, pc}
    mov r0, #0
    bl native_fn_021ef808
    mov r0, #0
    bl native_fn_021ef878
    mov r0, #1
    bl native_fn_021ef878
    mov r0, #1
    bl native_fn_021ef97c
    bl native_fn_021efbd0
    mov r0, #0
    bl native_fn_021efe60
    bl native_fn_02062aa0
    mov r4, r0
    bl native_fn_02062ad0
    add r0, r4, r0
    and r0, r0, #255
    cmp r0, #6
    movlo r1, r0
    movhs r1, #6
    str r0, [sp]
    and r0, r1, #255
    str r0, [sp, #0x4]
    mov r1, #16
    str r1, [sp, #0x8]
    ldr r0, [pc, #0x154]
    mov r1, #1
    ldr r0, [r0, #0x4]
    mov r2, #7
    add r0, r0, #16
    mov r3, #28
    bl native_fn_021f015c
    mov r0, #0
    bl native_fn_021ef1cc
    mov r0, #0
    bl native_fn_021ef17c
    mov r0, #224
    bl native_fn_021ef138
    mov r0, #1
    mov r1, r0
    bl native_fn_020620e8
    mov r0, #1
    bl native_fn_02062358
    ldr r1, [pc, #0x10c]
    mov r0, #0
    ldr r1, [r1, #0x4]
    strb r0, [r1, #0x50b]
    bl native_fn_02062a50
    bl native_fn_0206dcd0
    add sp, sp, #12
    ldmia sp!, {r3, r4, pc}
    mov r0, #1
    bl native_fn_021ef808
    mov r0, #1
    bl native_fn_021ef97c
    bl native_fn_021efbd0
    mov r0, #1
    mov r1, #6
    mov r2, #28
    bl native_fn_021ef8e0
    ldr r0, [pc, #0xc8]
    mov r12, #20
    ldr r2, [r0, #0x4]
    mov r3, #28
    ldrb r1, [r2, #0x504]
    cmp r1, #6
    movlo r0, r1
    movhs r0, #6
    and r0, r0, #255
    stmia sp, {r0, r1}
    add r0, r2, #16
    mov r1, #1
    mov r2, #7
    str r12, [sp, #0x8]
    bl native_fn_021f015c
    mov r0, #1
    bl native_fn_021efe60
    mov r0, #0
    bl native_fn_021ef1cc
    mov r0, #1
    bl native_fn_021ef17c
    mov r0, #224
    bl native_fn_021ef138
    bl native_fn_021ee300
    ldr r0, [pc, #0x68]
    mvn r1, #0
    ldr r2, [r0, #0x4]
    ldr r0, [r2, #0x10]
    add r0, r2, r0, lsl #2
    ldr r0, [r0, #0x104]
    bl native_fn_020c4c58
    ldr r1, [pc, #0x4c]
    mov r3, #0
    ldr r0, [r1, #0x4]
    mov r2, #1
    strb r3, [r0, #0x101]
    ldr r0, [r1, #0x4]
    add r0, r0, #1280
    strh r2, [r0, #6]
    ldr r0, [r1, #0x4]
    add r0, r0, #1280
    strh r3, [r0, #8]
    ldr r1, [r1, #0x4]
    add r0, r1, #16
    ldr r1, [r1, #0x514]
    bl native_fn_021edfdc
    ldr r0, [pc, #0x10]
    mov r1, #0
    ldr r0, [r0, #0x4]
    str r1, [r0, #0x514]
L_021ecf74:
    add sp, sp, #12
    ldmia sp!, {r3, r4, pc}
    dcd 0x02236bc4
    dcd native_data_0222b8ca
    dcd native_data_0222b8c4
}
