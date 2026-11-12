/* ov000 row 0x02216844: 388 bytes.
 *
 * What it does: 94 instructions and 22 call(s), then a 15-entry dispatch through an inline branch table at 0x02216870 (dispatch word at 0x02216868)
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

extern void native_fn_0221571c(void);
extern void native_fn_0221573c(void);
extern void native_fn_021f9b54(void);
extern void native_fn_022162e4(void);
extern void native_fn_020789dc(void);
extern void native_fn_02076700(void);
extern void native_fn_021ff4cc(void);
extern void native_fn_02072f70(void);
extern void native_fn_02079070(void);
extern void native_fn_0222216c(void);
extern void native_fn_021fbeb0(void);
extern void native_fn_021fe870(void);
extern void native_fn_02201608(void);
extern void native_fn_021fe048(void);
extern void native_fn_022179fc(void);
extern void native_fn_0206b324(void);
extern void native_fn_0221576c(void);
extern void native_fn_02215a8c(void);
extern void native_fn_02041538(void);
extern void native_fn_02062090(void);
extern void native_fn_02062074(void);


asm u32 native_ov000_02216844 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r0, #0
    mov r4, #1
    bl native_fn_0221571c
    mov r0, #127
    bl native_fn_0221573c
    ldr r0, [pc, #0x158]
    ldrsb r0, [r0, #16]
    cmp r0, #14
    addls pc, pc, r0, lsl #2
    b L_02216914
    dcd 0xea00000d
    dcd 0xea000015
    dcd 0xea000016
    dcd 0xea00001b
    dcd 0xea00000d
    dcd 0xea00001b
    dcd 0xea00000e
    dcd 0xea00001f
    dcd 0xea000012
    dcd 0xea000019
    dcd 0xea00001a
    dcd 0xea00001c
    dcd 0xea00001b
    dcd 0xea00001a
    dcd 0xea00000e
    bl native_fn_021f9b54
    cmp r0, #0
    moveq r4, #0
    b L_02216918
    bl native_fn_022162e4
    bl native_fn_020789dc
    b L_02216918
    bl native_fn_02076700
    b L_02216918
    bl native_fn_021ff4cc
    b L_02216918
    bl native_fn_02072f70
    b L_02216918
    bl native_fn_02079070
    b L_02216918
    bl native_fn_0222216c
    b L_02216918
    bl native_fn_021fbeb0
    b L_02216918
    bl native_fn_021fe870
    b L_02216918
    bl native_fn_02201608
    b L_02216918
    bl native_fn_021fe048
    b L_02216918
    bl native_fn_022162e4
L_02216914:
    bl native_fn_022179fc
L_02216918:
    cmp r4, #1
    bne L_0221699c
    ldr r0, [pc, #0x94]
    ldrsb r0, [r0, #16]
    cmp r0, #4
    bne L_02216938
    mov r0, #0
    bl native_fn_0206b324
L_02216938:
    bl native_fn_0221576c
    cmp r0, #0
    bne L_0221698c
    ldr r0, [pc, #0x70]
    ldrsb r0, [r0, #16]
    cmp r0, #0
    beq L_02216958
    bl native_fn_02215a8c
L_02216958:
    ldr r0, [pc, #0x5c]
    ldrsb r0, [r0, #16]
    cmp r0, #14
    beq L_02216978
    mov r0, #0
    mov r1, #2
    mov r2, #10
    bl native_fn_02041538
L_02216978:
    bl native_fn_02062090
    cmp r0, #0
    bne L_0221698c
    mov r0, #1
    bl native_fn_02062074
L_0221698c:
    ldr r0, [pc, #0x2c]
    mov r1, #3
    strb r1, [r0, #0x494]
    mov r4, #2
L_0221699c:
    ldr r0, [pc, #0x1c]
    mov r2, #1
    ldr r1, [pc, #0x18]
    strb r2, [r0, #0x49e]
    mov r2, #0
    mov r0, r4
    str r2, [r1, #0x10]
    ldmia sp!, {r4, pc}
    dcd 0x0224536c
    dcd 0x022459b4
    dcd 0x0224532c
}
