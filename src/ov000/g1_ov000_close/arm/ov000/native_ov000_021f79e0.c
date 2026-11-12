/* ov000 row 0x021f79e0: 1436 bytes.
 *
 * What it does: 354 instructions and 41 call(s), then a 13-entry dispatch through an inline branch table at 0x021f7a28 (dispatch word at 0x021f7a20)
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

extern void native_fn_02061dcc(void);
extern void native_fn_020633b0(void);
extern void native_fn_020633bc(void);
extern void native_fn_02049ffc(void);
extern void native_fn_02062a50(void);
extern void native_fn_0207b460(void);
extern void native_fn_02008be0(void);
extern void native_fn_02046af4(void);
extern void native_fn_02087a48(void);
extern void native_fn_020602ec(void);
extern void native_fn_020630b0(void);
extern void native_fn_02210f74(void);
extern void native_fn_0207c164(void);
extern void native_fn_021f7878(void);
extern void native_fn_02210f84(void);
extern void native_fn_02085284(void);
extern void native_fn_020877bc(void);
extern void native_fn_021f77b4(void);
extern void native_fn_02067dd4(void);
extern void native_fn_02067d54(void);
extern void native_fn_0204aaf0(void);
extern void native_fn_0205dc70(void);
extern u8 native_data_0222f350[];
extern u8 native_data_0222f354[];
extern u8 native_data_0222f358[];


asm u32 native_ov000_021f79e0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #148
    mov r7, r0
    bl native_fn_02061dcc
    ldr r8, [r0]
    ldr r4, [r8, #0x4]
    bl native_fn_020633b0
    mov r9, r0
    bl native_fn_020633bc
    mov r0, r4
    mov r5, #0
    bl native_fn_02049ffc
    mov r0, r5
    strh r0, [sp, #16]
    strh r0, [sp, #18]
    cmp r7, #12
    addls pc, pc, r7, lsl #2
    b L_021f7a98
    dcd 0xea00001a
    dcd 0xea00000a
    dcd 0xea000009
    dcd 0xea000008
    dcd 0xea00000b
    dcd 0xea00000a
    dcd 0xea000009
    dcd 0xea00000c
    dcd 0xea00000b
    dcd 0xea00000a
    dcd 0xea00000d
    dcd 0xea00000c
    dcd 0xea00000b
    sub r0, r7, #1
    bl native_fn_02062a50
    mov r5, r0
    b L_021f7a98
    sub r0, r7, #4
    bl native_fn_02062a50
    mov r5, r0
    b L_021f7a98
    sub r0, r7, #7
    bl native_fn_02062a50
    mov r5, r0
    b L_021f7a98
    sub r0, r7, #10
    bl native_fn_02062a50
    mov r5, r0
L_021f7a98:
    cmp r5, #0
    beq L_021f7ab8
    ldrsh r0, [r5, #24]
    ldrb r1, [r5, #0x1a]
    add r3, sp, #20
    add r2, r5, #122
    add r6, r5, #32
    bl native_fn_0207b460
L_021f7ab8:
    cmp r7, #14
    addls pc, pc, r7, lsl #2
    b L_021f7f60
    b L_021f7b00
    b L_021f7b60
    b L_021f7b60
    b L_021f7b60
    b L_021f7b88
    b L_021f7b88
    b L_021f7b88
    b L_021f7b88
    b L_021f7b88
    b L_021f7b88
    b L_021f7b88
    b L_021f7b88
    b L_021f7b88
    b L_021f7da0
    b L_021f7e88
L_021f7b00:
    add r1, sp, #84
    mov r0, #0
    mov r2, #64
    bl native_fn_02008be0
    add r2, sp, #84
    str r2, [sp]
    mov r5, #255
    ldr r0, [pc, #0x444]
    mov r1, r9
    mov r2, #64
    mov r3, #0
    str r5, [sp, #0x4]
    bl native_fn_02046af4
    mov r1, #0
    mov r0, #1
    str r0, [sp]
    add r5, sp, #84
    mov r0, r4
    mov r2, r1
    mov r3, r1
    str r5, [sp, #0x4]
    bl native_fn_02087a48
    add sp, sp, #148
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
L_021f7b60:
    mov r3, #0
    str r3, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    ldrsh r1, [r5, #24]
    mov r0, r8
    mov r2, r5
    bl native_fn_020602ec
    add sp, sp, #148
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
L_021f7b88:
    ldrb r1, [r4, #0x1c]
    ldrb r0, [r4, #0x1d]
    cmp r7, #6
    sub r2, r1, #1
    add r1, r0, #2
    mov r0, r2, lsl #24
    mov r1, r1, lsl #24
    mov r0, r0, asr #24
    str r0, [sp, #0xc]
    mov r11, r1, asr #24
    mov r9, #0
    mov r8, #1
    bgt L_021f7be8
    ldrb r6, [r6, #0x10]
    mov r10, r9
    mov r7, #2
    cmp r6, #100
    moveq r9, r8
    beq L_021f7c74
    ldrb r0, [r5, #0x1c]
    bl native_fn_020630b0
    cmp r0, r6
    moveq r8, #5
    b L_021f7c74
L_021f7be8:
    cmp r7, #9
    add r1, sp, #20
    mov r7, #4
    bgt L_021f7c48
    ldrsh r6, [r6, #4]
    mov r0, r5
    bl native_fn_02210f74
    mov r5, r0
    mov r0, r6, lsl #16
    mov r1, r5, lsl #16
    mov r0, r0, asr #16
    mov r1, r1, asr #16
    mov r10, r8
    bl native_fn_0207c164
    cmp r0, #0
    ldr r0, [sp, #0xc]
    mov r12, #9
    mov r1, r11
    mov r2, r6
    mov r3, r5
    movne r8, #7
    str r12, [sp]
    bl native_fn_021f7878
    b L_021f7c74
L_021f7c48:
    ldrsh r6, [r6, #6]
    mov r0, r5
    bl native_fn_02210f84
    mov r3, r0
    ldr r0, [sp, #0xc]
    mov r5, #12
    mov r1, r11
    mov r2, r6
    str r5, [sp]
    mov r10, #2
    bl native_fn_021f7878
L_021f7c74:
    add r0, r10, #1
    mov r1, r0, lsl #16
    mov r3, r1, lsr #16
    add r0, r4, #60
    mov r1, #5
    mov r2, #1
    bl native_fn_02085284
    add r1, sp, #84
    mov r0, #255
    str r1, [sp]
    str r0, [sp, #0x4]
    ldr r1, [r4, #0x68]
    ldr r0, [pc, #0x2bc]
    mov r2, #2
    mov r3, #0
    bl native_fn_02046af4
    mov r0, #1
    str r0, [sp]
    add r1, sp, #84
    str r1, [sp, #0x4]
    ldrsh r2, [sp, #16]
    ldrsh r3, [sp, #18]
    mov r0, r4
    mov r1, #0
    bl native_fn_02087a48
    ldrsh r2, [sp, #16]
    mov r1, #1
    ldr r0, [pc, #0x284]
    add r2, r2, #16
    strh r2, [sp, #16]
    str r1, [sp]
    str r0, [sp, #0x4]
    ldrsh r2, [sp, #16]
    ldrsh r3, [sp, #18]
    mov r0, r4
    mov r1, #0
    bl native_fn_02087a48
    ldrsh r2, [sp, #16]
    mov r0, #0
    add r1, sp, #84
    add r2, r2, #8
    strh r2, [sp, #16]
    mov r2, #64
    bl native_fn_02008be0
    cmp r9, #0
    bne L_021f7d68
    add r1, sp, #84
    mov r0, r6
    mov r3, r7
    mov r2, #64
    bl native_fn_020877bc
    add r0, sp, #84
    str r8, [sp]
    str r0, [sp, #0x4]
    ldrsh r2, [sp, #16]
    ldrsh r3, [sp, #18]
    mov r0, r4
    mov r1, #0
    bl native_fn_02087a48
    add sp, sp, #148
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
L_021f7d68:
    ldrb r3, [r4, #0x1c]
    ldrsh r0, [sp, #16]
    ldrb r2, [r4, #0x1d]
    ldrsh r1, [sp, #18]
    add r0, r3, r0, asr #3
    mov r0, r0, lsl #24
    add r1, r2, r1, asr #3
    mov r2, r1, lsl #24
    mov r1, r0, asr #24
    mov r2, r2, asr #24
    mov r0, #5
    bl native_fn_021f77b4
    add sp, sp, #148
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
L_021f7da0:
    add r1, sp, #84
    mov r0, #0
    mov r2, #64
    bl native_fn_02008be0
    ldr r0, [pc, #0x1b8]
    add r2, sp, #84
    ldrh r3, [r0, #66]
    mov r1, #255
    ldr r0, [pc, #0x1a0]
    strh r3, [sp, #84]
    str r2, [sp]
    str r1, [sp, #0x4]
    ldr r1, [r4, #0x68]
    mov r2, #8
    mov r3, #0
    bl native_fn_02046af4
    mov r0, #1
    mov r1, #0
    str r0, [sp]
    add r3, sp, #84
    str r3, [sp, #0x4]
    mov r0, r4
    mov r2, r1
    mov r3, r1
    bl native_fn_02087a48
    ldrsh r2, [sp, #16]
    mov r0, r0, lsl #16
    mov r1, #1
    add r0, r2, r0, asr #16
    strh r0, [sp, #16]
    str r1, [sp]
    ldr r1, [pc, #0x150]
    mov r0, r4
    str r1, [sp, #0x4]
    ldrsh r2, [sp, #16]
    ldrsh r3, [sp, #18]
    mov r1, #0
    bl native_fn_02087a48
    ldrsh r2, [sp, #16]
    mov r0, r0, lsl #16
    add r1, sp, #84
    add r0, r2, r0, asr #16
    strh r0, [sp, #16]
    ldr r0, [r9, #0x14]
    mov r2, #64
    mov r3, #6
    bl native_fn_020877bc
    mov r1, #1
    str r1, [sp]
    add r2, sp, #84
    str r2, [sp, #0x4]
    ldrsh r2, [sp, #16]
    ldrsh r3, [sp, #18]
    mov r0, r4
    mov r1, #0
    bl native_fn_02087a48
    add sp, sp, #148
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
L_021f7e88:
    bl native_fn_02067dd4
    bl native_fn_02067d54
    mov r1, #37
    mov r5, r0
    str r1, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    mov r2, #0
    str r2, [sp, #0x8]
    add r1, sp, #16
    mov r0, r7
    mov r2, #5
    mov r3, #2
    bl native_fn_0204aaf0
    ldrsh r3, [sp, #16]
    mov r2, #1
    ldr r1, [pc, #0xa8]
    add r0, r3, r0
    strh r0, [sp, #16]
    str r2, [sp]
    str r1, [sp, #0x4]
    ldrsh r2, [sp, #16]
    ldrsh r3, [sp, #18]
    mov r0, r4
    mov r1, #0
    bl native_fn_02087a48
    ldrsh r3, [sp, #16]
    add r1, sp, #84
    mov r2, #64
    add r0, r3, r0
    strh r0, [sp, #16]
    mov r0, #0
    bl native_fn_02008be0
    add r0, r5, #77
    mov r0, r0, lsl #16
    mov r2, r0, lsr #16
    mov r0, #5
    mov r1, #2
    bl native_fn_0205dc70
    mov r1, r0
    ldr r0, [pc, #0x38]
    add r2, sp, #84
    mov r3, #0
    stmia sp, {r2, r3}
    mov r2, #32
    bl native_fn_02046af4
    mov r1, #1
    str r1, [sp]
    str r0, [sp, #0x4]
    ldrsh r2, [sp, #16]
    ldrsh r3, [sp, #18]
    mov r0, r4
    mov r1, #0
    bl native_fn_02087a48
L_021f7f60:
    add sp, sp, #148
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    dcd 0x021c9698
    dcd native_data_0222f350
    dcd 0x020dbf18
    dcd native_data_0222f354
    dcd native_data_0222f358
}
