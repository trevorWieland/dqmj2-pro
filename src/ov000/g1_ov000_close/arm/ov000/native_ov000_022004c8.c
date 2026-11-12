/* ov000 row 0x022004c8: 780 bytes.
 *
 * What it does: 190 instructions and 19 call(s), then a 8-entry dispatch through an inline branch table at 0x022004f0 (dispatch word at 0x022004e8)
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

extern void ov000_display_context_02215698(void);
extern void native_fn_02217440(void);
extern void native_fn_022163fc(void);
extern void native_fn_02216440(void);
extern void native_fn_02216260(void);
extern void native_fn_0204b5b0(void);
extern void native_fn_02062aa0(void);
extern void native_fn_02062ad0(void);
extern void native_fn_02216350(void);
extern void native_fn_0204a644(void);
extern void native_fn_022166dc(void);
extern void native_fn_022008d8(void);


asm u32 native_ov000_022004c8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    sub sp, sp, #32
    mov r4, r0
    bl ov000_display_context_02215698
    mov r6, r0
    bl native_fn_02217440
    mov r5, r0
    cmp r4, #7
    addls pc, pc, r4, lsl #2
    b L_022007b0
    dcd 0xea0000ae
    dcd 0xea000005
    dcd 0xea0000ac
    dcd 0xea00001a
    dcd 0xea0000aa
    dcd 0xea000040
    dcd 0xea0000a8
    dcd 0xea0000a7
    ldr r0, [pc, #0x2a8]
    ldr r5, [pc, #0x2a8]
    ldrb r0, [r0, #0x5e6]
    ldmia r5, {r6, r7}
    add r0, r0, #1
    and r8, r0, #255
    mov r0, #5
    mov r1, #1
    mov r2, #3
    bl native_fn_022163fc
    str r8, [sp]
    str r8, [sp, #0x4]
    mov r1, #1
    str r1, [sp, #0x8]
    mov r0, #15
    str r0, [sp, #0xc]
    mov r0, r5
    str r1, [sp, #0x10]
    mov r2, #3
    mov r3, #28
    bl native_fn_02216440
    stmia r5, {r6, r7}
    b L_022007b0
    ldr r0, [pc, #0x24c]
    ldr r8, [pc, #0x250]
    ldr r1, [r0, #0x8]
    ldr r0, [pc, #0x24c]
    and r1, r1, #255
    ldrb r9, [r0, r1]
    ldmia r8, {r6, r7}
    mov r0, #3
    str r0, [sp]
    mov r1, #30
    str r1, [sp, #0x4]
    mov r2, #2
    mov r0, #1
    str r2, [sp, #0x8]
    mov r1, #0
    str r1, [sp, #0xc]
    str r0, [sp, #0x10]
    ldrsb r1, [r5, #16]
    mov r3, r0
    bl native_fn_02216260
    cmp r9, #6
    movhi r9, #6
    and r5, r9, #255
    mov r0, #5
    mov r1, #2
    mov r2, #22
    bl native_fn_022163fc
    str r5, [sp]
    str r5, [sp, #0x4]
    mov r1, #1
    str r1, [sp, #0x8]
    mov r0, #15
    str r0, [sp, #0xc]
    mov r0, r8
    str r1, [sp, #0x10]
    mov r2, #6
    mov r3, #28
    bl native_fn_02216440
    stmia r8, {r6, r7}
    b L_022007b0
    ldr r1, [pc, #0x1ac]
    mov r0, #2
    ldrb r7, [r1, #0x5e6]
    mov r2, #5
    mov r1, #29
    str r2, [sp]
    str r1, [sp, #0x4]
    str r0, [sp, #0x8]
    mov r1, #0
    str r1, [sp, #0xc]
    mov r1, #1
    str r1, [sp, #0x10]
    ldrsb r1, [r5, #16]
    mov r2, r0
    mov r3, r0
    ldr r9, [pc, #0x180]
    bl native_fn_02216260
    mov r0, #5
    mov r1, #1
    mov r2, #2
    bl native_fn_022163fc
    ldr r0, [pc, #0x158]
    ldrb r0, [r0, #0x5e8]
    cmp r0, #0
    bne L_022006ac
    str r7, [sp]
    str r7, [sp, #0x4]
    mov r1, #1
    str r1, [sp, #0x8]
    mov r0, #15
    str r0, [sp, #0xc]
    mov r0, r9
    mov r2, #8
    mov r3, #28
    str r1, [sp, #0x10]
    bl native_fn_02216440
    add r0, r6, #16
    mov r1, #224
    bl native_fn_0204b5b0
    b L_022007b0
L_022006ac:
    bl native_fn_02062aa0
    mov r7, r0
    bl native_fn_02062ad0
    add r0, r7, r0
    mov r0, r0, lsl #24
    mov r8, r0, asr #23
    rsb r0, r8, #21
    and r7, r0, #255
    add r1, sp, #28
    mov r2, #0
    strh r2, [r1]
    strh r2, [r1, #2]
    mov r1, #2
    str r1, [sp]
    mov r1, #1
    str r1, [sp, #0x4]
    str r1, [sp, #0x8]
    str r2, [sp, #0xc]
    mov r0, r9
    mov r2, #7
    mov r3, #12
    bl native_fn_02216350
    str r7, [sp]
    mov r0, #6
    str r0, [sp, #0x4]
    mov r2, #2
    str r2, [sp, #0x8]
    mov r0, #0
    str r0, [sp, #0xc]
    mov r0, #1
    str r0, [sp, #0x10]
    mov r0, #24
    ldrsb r1, [r5, #16]
    mov r3, r0
    bl native_fn_02216260
    mov r0, #2
    str r0, [sp]
    mov r3, #1
    str r3, [sp, #0x4]
    mov r0, #24
    add r1, sp, #28
    mov r2, #5
    str r3, [sp, #0x8]
    bl native_fn_0204a644
    add r0, r7, #2
    and r1, r0, #255
    mov r0, #17
    str r0, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    mov r0, #1
    str r0, [sp, #0x8]
    mov r0, #25
    str r0, [sp, #0xc]
    mov r0, #27
    str r0, [sp, #0x10]
    mov r2, #28
    and r3, r8, #255
    str r2, [sp, #0x14]
    mov r0, #2
    str r0, [sp, #0x18]
    bl native_fn_022166dc
    add r0, r6, #16
    mov r1, #96
    bl native_fn_0204b5b0
L_022007b0:
    mov r0, r4
    bl native_fn_022008d8
    add sp, sp, #32
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
    dcd 0x02237778
    dcd 0x02237780
    dcd 0x02237870
    dcd 0x02237d54
    dcd 0x02237960
}
