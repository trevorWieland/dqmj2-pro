/* ov000 row 0x02207668: 480 bytes.
 *
 * What it does: 119 instructions and 22 call(s), then a 6-entry dispatch through an inline branch table at 0x022076b8 (dispatch word at 0x022076b0)
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

extern void native_fn_02207610(void);
extern void native_fn_0205e7a8(void);
extern void native_fn_02206128(void);
extern void native_fn_02206d58(void);
extern void native_fn_02207b9c(void);
extern void native_fn_02205e80(void);
extern void native_fn_02205e70(void);
extern void native_fn_020c18b8(void);
extern void native_fn_02041538(void);


asm u32 native_ov000_02207668 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    sub sp, sp, #8
    ldr r0, [pc, #0x1cc]
    mov r4, #0
    ldr r0, [r0]
    mov r5, #1
    bl native_fn_02207610
    cmp r0, #0
    bne L_022076a4
    mvn r0, #0
    mov r1, #84
    bl native_fn_0205e7a8
    add sp, sp, #8
    mov r0, r4
    ldmia sp!, {r3, r4, r5, pc}
L_022076a4:
    ldr r2, [pc, #0x198]
    ldr r0, [r2]
    cmp r0, #5
    addls pc, pc, r0, lsl #2
    b L_022077f4
    dcd 0xea00001e
    dcd 0xea000003
    dcd 0xea000023
    dcd 0xea00002d
    dcd 0xea000035
    dcd 0xea00003d
    bl native_fn_02206128
    cmp r0, #0
    beq L_02207718
    mov r3, r5
    str r3, [sp]
    mov r4, #82
    mov r0, #5
    mov r1, #6
    mov r2, #33
    str r4, [sp, #0x4]
    bl native_fn_02206d58
    mov r0, #0
    bl native_fn_02207b9c
    ldr r0, [pc, #0x138]
    mov r1, #4
    strb r1, [r0, #0xf0]
    mov r5, #0
    b L_02207724
L_02207718:
    mvn r0, #0
    mov r1, #82
    bl native_fn_0205e7a8
L_02207724:
    ldr r0, [pc, #0x118]
    mov r1, #2
    strb r1, [r0, #0xf1]
    mov r4, #1
    b L_02207800
    mov r3, #3
    sub r0, r3, #4
    mov r1, #82
    strb r3, [r2, #0xf1]
    bl native_fn_0205e7a8
    mov r4, r5
    b L_02207800
    mov r1, #4
    mov r0, #8
    strb r1, [r2, #0xf1]
    bl native_fn_02205e80
    mov r0, r4
    bl native_fn_02205e70
    mvn r0, #0
    mov r1, #82
    bl native_fn_0205e7a8
    mov r4, r5
    b L_02207800
    mov r0, #3
    bl native_fn_02205e80
    mov r0, r4
    bl native_fn_02205e70
    mvn r0, #0
    mov r1, #82
    bl native_fn_0205e7a8
    mov r4, r5
    b L_02207800
    mov r0, #10
    bl native_fn_02205e80
    mov r0, r4
    bl native_fn_02205e70
    mvn r0, #0
    mov r1, #82
    bl native_fn_0205e7a8
    mov r4, r5
    b L_02207800
    mov r1, #4
    mov r0, #13
    strb r1, [r2, #0xf1]
    bl native_fn_02205e80
    mov r0, r4
    bl native_fn_02205e70
    mvn r0, #0
    mov r1, #82
    bl native_fn_0205e7a8
    mov r4, r5
    b L_02207800
L_022077f4:
    mvn r0, #0
    mov r1, #84
    bl native_fn_0205e7a8
L_02207800:
    cmp r4, #0
    beq L_02207838
    ldr r0, [pc, #0x34]
    ldr r0, [r0]
    bl native_fn_020c18b8
    cmp r5, #0
    beq L_02207838
    ldr r3, [pc, #0x20]
    mov r5, #5
    mov r0, #1
    mov r1, #2
    mov r2, #10
    strb r5, [r3, #0xf0]
    bl native_fn_02041538
L_02207838:
    mov r0, r4
    add sp, sp, #8
    ldmia sp!, {r3, r4, r5, pc}
    dcd 0x022382c8
}
