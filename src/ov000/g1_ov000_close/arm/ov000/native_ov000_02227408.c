/* ov000 row 0x02227408: 576 bytes.
 *
 * What it does: 142 instructions and 20 call(s), then a 7-entry dispatch through an inline branch table at 0x02227434 (dispatch word at 0x0222742c)
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
extern void native_fn_020c5dc4(void);
extern void native_fn_0206bc80(void);
extern void native_fn_02223df0(void);
extern void native_fn_02223e70(void);
extern void native_fn_02223ce0(void);
extern void native_fn_02224e38(void);
extern void native_fn_020c9414(void);
extern void native_fn_020caf9c(void);
extern void native_fn_02227ccc(void);
extern void native_fn_0222534c(void);
extern void native_fn_022252ac(void);
extern void native_fn_01ffa824(void);
extern void native_fn_01ffa5fc(void);
extern void native_fn_02224b84(void);


asm u32 native_ov000_02227408 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    sub sp, sp, #16
    bl native_fn_0202a634
    ldr r1, [pc, #0x224]
    mov r4, #0
    ldr r0, [r1, #0xc]
    ldr r6, [pc, #0x21c]
    mov r5, r4
    cmp r0, #6
    addls pc, pc, r0, lsl #2
    b L_02227634
    dcd 0xea000005
    dcd 0xea000007
    dcd 0xea00003e
    dcd 0xea00003d
    dcd 0xea000047
    dcd 0xea000064
    dcd 0xea000072
    mov r0, #1
    str r0, [r1, #0xc]
    b L_02227634
    bl native_fn_020c5dc4
    cmp r0, #1
    beq L_0222747c
    ldr r0, [pc, #0x1d0]
    ldrsb r0, [r0]
    cmp r0, #0
    movne r4, #1
    moveq r5, #1
L_0222747c:
    cmp r4, #0
    beq L_02227510
    add r0, sp, #4
    add r1, sp, #0
    bl native_fn_0206bc80
    mov r0, #0
    mov r1, #3
    strb r1, [r6, #0x18d]
    strb r0, [r6, #0x190]
    strb r0, [r6, #0x18e]
    bl native_fn_02223df0
    bl native_fn_02223e70
    mov r7, #0
    mov r4, r7
    mov r5, r7
L_022274b8:
    ldrsh r0, [r6, #24]
    cmp r0, #0
    beq L_022274d8
    mov r0, r5
    mov r1, r7
    mov r2, r6
    bl native_fn_02223ce0
    b L_022274e8
L_022274d8:
    mov r0, r4
    mov r1, r7
    mov r2, r4
    bl native_fn_02223ce0
L_022274e8:
    add r0, r7, #1
    mov r0, r0, lsl #24
    mov r7, r0, asr #24
    cmp r7, #3
    add r6, r6, #132
    blt L_022274b8
    ldr r0, [pc, #0x138]
    mov r1, #6
    str r1, [r0, #0xc]
    b L_0222752c
L_02227510:
    cmp r5, #0
    beq L_0222752c
    bl native_fn_02224e38
    ldr r1, [pc, #0x11c]
    mov r2, #0
    str r0, [r1, #0x14]
    str r2, [r1, #0xc]
L_0222752c:
    mov r0, #10
    bl native_fn_020c9414
    bl native_fn_020caf9c
    b L_02227634
    strb r4, [r6, #0x18e]
    bl native_fn_02227ccc
    cmp r0, #0
    beq L_02227554
    bl native_fn_0222534c
    b L_02227558
L_02227554:
    bl native_fn_022252ac
L_02227558:
    ldr r0, [pc, #0xe0]
    mov r1, #4
    str r1, [r0, #0xc]
    b L_02227634
    bl native_fn_01ffa824
    ldrb r1, [r6, #0x18e]
    and r0, r0, #255
    add r1, r1, #48
    mov r1, r1, lsl #16
    mov r1, r1, lsr #16
    bl native_fn_01ffa5fc
    cmp r0, #0
    bne L_022275d0
    bl native_fn_02227ccc
    cmp r0, #0
    beq L_022275b4
    bl native_fn_0222534c
    cmp r0, #0
    bne L_02227634
    ldr r0, [pc, #0x94]
    mov r1, #5
    str r1, [r0, #0xc]
    b L_02227634
L_022275b4:
    bl native_fn_022252ac
    cmp r0, #0
    bne L_02227634
    ldr r0, [pc, #0x78]
    mov r1, #5
    str r1, [r0, #0xc]
    b L_02227634
L_022275d0:
    ldrb r0, [r6, #0x18e]
    add r0, r0, #1
    strb r0, [r6, #0x18e]
    b L_02227634
    ldrb r2, [r6, #0x190]
    ldrb r0, [r6, #0x18d]
    add r3, r2, #1
    and r2, r3, #255
    cmp r2, r0
    movhs r0, #6
    strb r3, [r6, #0x190]
    strhs r0, [r1, #0xc]
    bhs L_02227634
    mov r0, r2
    add r0, r0, #1
    mov r2, #3
    str r2, [r1, #0xc]
    strb r0, [r6, #0x190]
    b L_02227634
    mov r0, r4
    str r4, [r1, #0xc]
    bl native_fn_02224b84
    ldr r0, [pc, #0x10]
    mov r1, #6
    str r1, [r0, #0x14]
L_02227634:
    mov r0, #0
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
    dcd 0x022468b8
    dcd 0x02246c84
}
