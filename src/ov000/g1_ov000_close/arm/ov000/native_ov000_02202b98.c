/* ov000 row 0x02202b98: 1732 bytes.
 *
 * What it does: 426 instructions and 53 call(s), then a 21-entry dispatch through an inline branch table at 0x02202c04 (dispatch word at 0x02202bfc)
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

extern void native_fn_02061944(void);
extern void native_fn_02061dcc(void);
extern void native_fn_02049ffc(void);
extern void native_fn_02008be0(void);
extern void native_fn_020633b0(void);
extern void native_fn_0204abd4(void);
extern void native_fn_0204aaf0(void);
extern void native_fn_0204a9a0(void);
extern void native_fn_02063cf4(void);
extern void native_fn_0204a9d4(void);
extern void native_fn_02063d30(void);
extern void native_fn_02063d6c(void);
extern void native_fn_020449d4(void);
extern void native_fn_02044d84(void);
extern void native_fn_02044fcc(void);
extern void native_fn_02063520(void);
extern void native_fn_020877bc(void);
extern void native_fn_02087a48(void);
extern void native_fn_02085284(void);
extern void native_fn_02046af4(void);
extern void native_fn_020470fc(void);
extern void native_fn_02087674(void);
extern void native_fn_0208791c(void);
extern void native_fn_02008e0c(void);
extern u8 native_data_0222f54c[];
extern u8 native_data_0222f550[];
extern u8 native_data_0222f554[];
extern u8 native_data_0222f558[];
extern u8 native_data_0222f55c[];


asm u32 native_ov000_02202b98 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, lr}
    sub sp, sp, #80
    mov r8, r0
    bl native_fn_02061944
    mov r5, r0
    mov r0, r8
    ldr r6, [pc, #0x688]
    bl native_fn_02061dcc
    add r1, sp, #12
    mov r4, #0
    strh r4, [r1]
    strh r4, [r1, #2]
    ldr r0, [r0]
    cmp r0, #0
    ldrne r7, [r0, #0x4]
    cmpne r7, #0
    addeq sp, sp, #80
    ldmeqia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
    mov r0, r7
    bl native_fn_02049ffc
    add r1, sp, #16
    mov r0, r4
    mov r2, #64
    bl native_fn_02008be0
    cmp r8, #20
    addls pc, pc, r8, lsl #2
    b L_02203238
    dcd 0xea00018b
    dcd 0xea00018a
    dcd 0xea000189
    dcd 0xea000188
    dcd 0xea000187
    dcd 0xea000186
    dcd 0xea00000d
    dcd 0xea000019
    dcd 0xea000038
    dcd 0xea000057
    dcd 0xea000076
    dcd 0xea000084
    dcd 0xea000083
    dcd 0xea000082
    dcd 0xea000081
    dcd 0xea000080
    dcd 0xea00007f
    dcd 0xea00007e
    dcd 0xea00007d
    dcd 0xea0000be
    dcd 0xea000107
    bl native_fn_020633b0
    str r0, [sp]
    mov r3, #1
    add r2, sp, #12
    mov r0, r8
    mov r1, r6
    str r3, [sp, #0x4]
    bl native_fn_0204abd4
    ldrsh r1, [sp, #12]
    add r0, r1, r0
    strh r0, [sp, #12]
    add sp, sp, #80
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
    strh r4, [sp, #12]
    mov r0, #17
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    add r1, sp, #12
    mov r0, r8
    mov r2, #9
    mov r3, #5
    str r4, [sp, #0x8]
    bl native_fn_0204aaf0
    mov r4, #64
    ldr r3, [pc, #0x580]
    add r1, sp, #12
    mov r0, r8
    mov r2, #1
    strh r4, [sp, #12]
    bl native_fn_0204a9a0
    mov r0, #72
    strh r0, [sp, #12]
    bl native_fn_02063cf4
    mov r1, #4
    str r1, [sp]
    mov r1, #0
    mov r3, r0
    str r1, [sp, #0x4]
    mov r0, r8
    add r1, sp, #12
    mov r2, #1
    bl native_fn_0204a9d4
    add sp, sp, #80
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
    strh r4, [sp, #12]
    mov r0, #18
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    add r1, sp, #12
    mov r0, r8
    mov r2, #9
    mov r3, #5
    str r4, [sp, #0x8]
    bl native_fn_0204aaf0
    mov r4, #64
    ldr r3, [pc, #0x504]
    add r1, sp, #12
    mov r0, r8
    mov r2, #1
    strh r4, [sp, #12]
    bl native_fn_0204a9a0
    mov r0, #72
    strh r0, [sp, #12]
    bl native_fn_02063d30
    mov r1, #4
    str r1, [sp]
    mov r1, #0
    mov r3, r0
    str r1, [sp, #0x4]
    mov r0, r8
    add r1, sp, #12
    mov r2, #1
    bl native_fn_0204a9d4
    add sp, sp, #80
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
    strh r4, [sp, #12]
    mov r0, #19
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    add r1, sp, #12
    mov r0, r8
    mov r2, #9
    mov r3, #5
    str r4, [sp, #0x8]
    bl native_fn_0204aaf0
    mov r4, #64
    ldr r3, [pc, #0x488]
    add r1, sp, #12
    mov r0, r8
    mov r2, #1
    strh r4, [sp, #12]
    bl native_fn_0204a9a0
    mov r0, #72
    strh r0, [sp, #12]
    bl native_fn_02063d6c
    mov r1, #4
    str r1, [sp]
    mov r1, #0
    mov r3, r0
    str r1, [sp, #0x4]
    mov r0, r8
    add r1, sp, #12
    mov r2, #1
    bl native_fn_0204a9d4
    add sp, sp, #80
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
    mov r0, #20
    str r0, [sp]
    mov r2, #1
    str r2, [sp, #0x4]
    str r2, [sp, #0x8]
    add r1, sp, #12
    mov r0, r8
    mov r2, #9
    mov r3, #5
    bl native_fn_0204aaf0
    ldrsh r1, [sp, #12]
    add r0, r1, r0
    strh r0, [sp, #12]
    add sp, sp, #80
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
    add r1, sp, #16
    mov r0, r4
    mov r2, #64
    bl native_fn_02008be0
    add r0, r8, #3
    mov r0, r0, lsl #16
    mov r0, r0, lsr #16
    add r0, r0, #123
    add r1, r0, #256
    ldr r0, [pc, #0x3dc]
    mov r1, r1, lsl #1
    ldrh r0, [r0, r1]
    sub r9, r8, #10
    mov r6, r4
    strh r0, [sp, #16]
    mov r5, r4
L_02202e88:
    mov r0, r6
    bl native_fn_020449d4
    ldrh r0, [r0, #4]
    mov r0, r0, lsl #24
    mov r0, r0, lsr #28
    and r0, r0, #255
    cmp r9, r0
    bne L_02202f04
    mov r0, r6
    mov r8, r5
    bl native_fn_02044d84
    rsbs r0, r0, #2
    bmi L_02202f04
L_02202ebc:
    mov r0, r6
    mov r1, r8
    bl native_fn_02044fcc
    cmp r0, #0
    bne L_02202eec
    mov r0, r6
    mov r1, r8
    bl native_fn_02063520
    cmp r0, #0
    addne r0, r4, #1
    movne r0, r0, lsl #16
    movne r4, r0, lsr #16
L_02202eec:
    mov r0, r6
    add r8, r8, #1
    bl native_fn_02044d84
    rsb r0, r0, #2
    cmp r8, r0
    ble L_02202ebc
L_02202f04:
    add r6, r6, #1
    cmp r6, #512
    blt L_02202e88
    add r1, sp, #18
    mov r0, r4
    mov r2, #62
    mov r3, #3
    bl native_fn_020877bc
    mov r1, #0
    mov r0, #1
    str r0, [sp]
    add r4, sp, #16
    mov r0, r7
    mov r2, r1
    mov r3, r1
    str r4, [sp, #0x4]
    bl native_fn_02087a48
    add sp, sp, #80
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
    add r0, r7, #60
    mov r1, #9
    mov r2, #5
    mov r3, #21
    bl native_fn_02085284
    add r1, sp, #16
    mov r0, #255
    str r1, [sp]
    str r0, [sp, #0x4]
    ldrb r2, [r7, #0x5e]
    ldr r1, [r7, #0x68]
    mov r0, r6
    mov r3, r4
    bl native_fn_02046af4
    add r0, sp, #16
    bl native_fn_020470fc
    mov r8, r0
    mov r10, r4
    mov r5, r4
L_02202f9c:
    mov r0, r10
    mov r9, r5
    bl native_fn_02044d84
    rsbs r0, r0, #2
    bmi L_02202ff8
L_02202fb0:
    mov r0, r10
    mov r1, r9
    bl native_fn_02044fcc
    cmp r0, #0
    bne L_02202fe0
    mov r0, r10
    mov r1, r9
    bl native_fn_02063520
    cmp r0, #0
    addne r0, r4, #1
    movne r0, r0, lsl #16
    movne r4, r0, lsr #16
L_02202fe0:
    mov r0, r10
    add r9, r9, #1
    bl native_fn_02044d84
    rsb r0, r0, #2
    cmp r9, r0
    ble L_02202fb0
L_02202ff8:
    add r10, r10, #1
    cmp r10, #512
    blt L_02202f9c
    add r1, sp, #16
    mov r2, r8, lsl #1
    mov r0, r4
    add r1, r1, r8, lsl #1
    rsb r2, r2, #64
    mov r3, #3
    bl native_fn_020877bc
    add r3, r8, #3
    add r2, sp, #16
    mov r0, r6
    add r1, r7, #60
    strh r3, [r7, #108]
    bl native_fn_02087674
    mov r3, #1
    mov r2, r0, lsl #16
    add r0, sp, #16
    str r3, [sp]
    str r0, [sp, #0x4]
    ldrb r4, [r7, #0x5e]
    mov r1, #0
    mov r0, r7
    mov r4, r4, lsl #3
    sub r2, r4, r2, asr #16
    mov r2, r2, lsl #16
    mov r3, r1
    mov r2, r2, asr #16
    bl native_fn_02087a48
    add sp, sp, #80
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
    add r0, r7, #60
    mov r1, #5
    mov r2, #2
    mov r3, #10
    bl native_fn_02085284
    add r1, sp, #16
    mov r0, #255
    str r1, [sp]
    str r0, [sp, #0x4]
    ldrb r2, [r7, #0x5e]
    ldr r1, [r7, #0x68]
    mov r0, r6
    mov r3, r4
    bl native_fn_02046af4
    mov r0, #1
    mov r1, r4
    str r0, [sp]
    add r3, sp, #16
    str r3, [sp, #0x4]
    mov r0, r7
    mov r2, r1
    mov r3, r1
    bl native_fn_02087a48
    mov r0, r0, lsl #16
    mov r0, r0, asr #16
    add r0, r0, #8
    mov r0, r0, lsl #16
    mov r4, r0, asr #16
    add r0, r5, #512
    ldrsh r0, [r0, #180]
    add r1, sp, #16
    mov r2, #64
    mov r3, #4
    bl native_fn_020877bc
    mov r0, #1
    str r0, [sp]
    add r1, sp, #16
    str r1, [sp, #0x4]
    mov r1, #0
    mov r0, r7
    mov r2, r4
    mov r3, r1
    bl native_fn_02087a48
    mov r0, r0, lsl #16
    add r0, r4, r0, asr #16
    mov r0, r0, lsl #16
    mov r4, r0, asr #16
    mov r0, #1
    str r0, [sp]
    ldr r1, [pc, #0x110]
    mov r0, r7
    str r1, [sp, #0x4]
    mov r1, #0
    mov r2, r4
    mov r3, r1
    bl native_fn_02087a48
    mov r0, r0, lsl #16
    add r0, r4, r0, asr #16
    mov r0, r0, lsl #16
    mov r4, r0, asr #16
    add r0, r5, #512
    ldrsh r0, [r0, #182]
    add r1, sp, #16
    mov r2, #64
    mov r3, #2
    bl native_fn_0208791c
    mov r0, #1
    str r0, [sp]
    add r1, sp, #16
    str r1, [sp, #0x4]
    mov r1, #0
    mov r0, r7
    mov r2, r4
    mov r3, r1
    bl native_fn_02087a48
    mov r0, r0, lsl #16
    add r0, r4, r0, asr #16
    mov r0, r0, lsl #16
    mov r4, r0, asr #16
    mov r0, #1
    mov r1, #0
    str r0, [sp]
    ldr r6, [pc, #0x90]
    mov r0, r7
    mov r2, r4
    mov r3, r1
    str r6, [sp, #0x4]
    bl native_fn_02087a48
    mov r0, r0, lsl #16
    add r0, r4, r0, asr #16
    mov r4, r0, lsl #16
    add r1, r5, #512
    ldrsh r0, [r1, #184]
    add r1, sp, #16
    mov r2, #64
    mov r3, #2
    mov r4, r4, asr #16
    bl native_fn_0208791c
    mov r1, #1
    str r1, [sp]
    add r3, sp, #16
    mov r1, #0
    str r3, [sp, #0x4]
    mov r0, r7
    mov r2, r4
    mov r3, r1
    bl native_fn_02087a48
    add r1, r5, #186
    add r0, r5, #692
    add r1, r1, #512
    mov r2, #6
    bl native_fn_02008e0c
L_02203238:
    add sp, sp, #80
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
    dcd 0x021c9698
    dcd native_data_0222f54c
    dcd native_data_0222f550
    dcd native_data_0222f554
    dcd 0x020dbc18
    dcd native_data_0222f558
    dcd native_data_0222f55c
}
