/* ov000 row 0x0220734c: 708 bytes.
 *
 * What it does: 174 instructions and 31 call(s), then a 7-entry dispatch through an inline branch table at 0x0220736c (dispatch word at 0x02207364)
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

extern void native_fn_02206868(void);
extern void native_fn_022069d8(void);
extern void native_fn_02206ae8(void);
extern void native_fn_020c18c8(void);
extern void native_fn_02206128(void);
extern void native_fn_02207954(void);
extern void native_fn_02207b9c(void);
extern void native_fn_02206dd4(void);
extern void native_fn_02041538(void);
extern void native_fn_0220610c(void);
extern void native_fn_02041814(void);
extern void native_fn_02206140(void);
extern void native_fn_0202a634(void);
extern void native_fn_02206158(void);
extern void native_fn_020491f8(void);
extern void native_fn_0205e7a8(void);
extern void native_fn_02207668(void);
extern void native_fn_02206c1c(void);
extern void native_fn_02207a58(void);
extern void native_fn_02206c4c(void);
extern void native_fn_022078e0(void);
extern void native_fn_02207acc(void);
extern u8 native_data_0222ba8c[];


asm u32 native_ov000_0220734c (register u32 a0)
{
    stmdb sp!, {r3, r4, lr}
    sub sp, sp, #36
    ldr r0, [pc, #0x2a8]
    mov r4, #0
    ldrb r0, [r0, #0xf0]
    cmp r0, #6
    addls pc, pc, r0, lsl #2
    b L_022075d8
    dcd 0xea000005
    dcd 0xea000050
    dcd 0xea000097
    dcd 0xea000059
    dcd 0xea00007a
    dcd 0xea000086
    dcd 0xea00008c
    mov r1, #1
    str r1, [sp]
    mov r0, #30
    str r0, [sp, #0x4]
    mov r3, #2
    str r3, [sp, #0x8]
    str r4, [sp, #0xc]
    ldr r4, [pc, #0x25c]
    str r1, [sp, #0x10]
    mov r0, #7
    mov r2, #127
    str r4, [sp, #0x14]
    bl native_fn_02206868
    mov r4, #0
    mov r0, #7
    mov r1, #5
    mov r2, #2
    mov r3, #65
    str r4, [sp]
    bl native_fn_022069d8
    ldr r0, [pc, #0x22c]
    mov r3, #4
    ldrh r2, [r0]
    ldrh r1, [r0, #2]
    ldrh r12, [r0, #4]
    strh r2, [sp, #24]
    strh r1, [sp, #26]
    ldrh r4, [r0, #6]
    mov r1, #23
    add r2, sp, #24
    strh r4, [sp, #30]
    strh r12, [sp, #28]
    ldrh lr, [r0, #8]
    ldrh r12, [r0, #10]
    ldr r4, [pc, #0x1f0]
    ldr r0, [pc, #0x1e8]
    strh lr, [sp, #32]
    strh r12, [sp, #34]
    str r3, [sp]
    str r1, [sp, #0x4]
    mov r1, #6
    mov r3, #1
    str r4, [sp, #0x8]
    bl native_fn_02206ae8
    bl native_fn_020c18c8
    ldr r1, [pc, #0x1c0]
    str r0, [r1]
    bl native_fn_02206128
    cmp r0, #0
    ldreq r0, [pc, #0x1b0]
    moveq r1, #1
    streq r1, [r0]
    bl native_fn_02207954
    mov r0, #1
    bl native_fn_02207b9c
    bl native_fn_02206dd4
    ldr r0, [r0, #0xc]
    cmp r0, #2
    beq L_02207484
    bl native_fn_02206dd4
    ldr r0, [r0, #0xc]
    cmp r0, #3
    bne L_022074a4
L_02207484:
    mov r0, #0
    mov r1, #2
    mov r2, #10
    bl native_fn_02041538
    ldr r0, [pc, #0x168]
    mov r1, #3
    strb r1, [r0, #0xf0]
    b L_022074b0
L_022074a4:
    ldr r0, [pc, #0x158]
    mov r1, #1
    strb r1, [r0, #0xf0]
L_022074b0:
    mov r4, #1
    b L_022075d8
    bl native_fn_0220610c
    cmp r0, #0
    beq L_022075d8
    mov r0, r4
    mov r1, #2
    mov r2, #60
    bl native_fn_02041538
    ldr r0, [pc, #0x128]
    mov r1, #3
    strb r1, [r0, #0xf0]
    b L_022075d8
    bl native_fn_02041814
    cmp r0, #1
    beq L_022075d8
    bl native_fn_02206140
    cmp r0, #0
    bne L_02207514
    bl native_fn_0202a634
    ldrh r0, [r0, #2]
    tst r0, #192
    beq L_02207514
    mov r0, #1
    bl native_fn_02206158
L_02207514:
    bl native_fn_02206140
    cmp r0, #0
    beq L_02207544
    ldr r0, [pc, #0xdc]
    bl native_fn_020491f8
    cmp r0, #0
    beq L_02207544
    mvn r0, #0
    mov r1, #85
    bl native_fn_0205e7a8
    mov r4, #1
    b L_022075d8
L_02207544:
    bl native_fn_0202a634
    ldrh r0, [r0, #2]
    tst r0, #1
    beq L_022075d8
    bl native_fn_02207668
    cmp r0, #0
    mov r0, #1
    movne r4, #1
    bl native_fn_02206158
    b L_022075d8
    bl native_fn_02041814
    cmp r0, #1
    beq L_022075d8
    mov r0, #1
    bl native_fn_02207b9c
    mov r0, #1
    mov r1, #2
    mov r2, #10
    bl native_fn_02041538
    ldr r0, [pc, #0x6c]
    mov r1, #5
    strb r1, [r0, #0xf0]
    b L_022075d8
    bl native_fn_02041814
    cmp r0, #1
    beq L_022075d8
    ldr r0, [pc, #0x50]
    mov r1, #6
    strb r1, [r0, #0xf0]
    b L_022075d8
    ldr r0, [pc, #0x44]
    bl native_fn_02206c1c
    bl native_fn_02207a58
    ldr r0, [pc, #0x34]
    add sp, sp, #36
    ldrb r0, [r0, #0xf1]
    ldmia sp!, {r3, r4, pc}
L_022075d8:
    cmp r4, #0
    beq L_022075ec
    ldr r0, [pc, #0x1c]
    bl native_fn_02206c4c
    bl native_fn_022078e0
L_022075ec:
    ldr r0, [pc, #0x10]
    mov r1, #1
    bl native_fn_02207acc
    mov r0, #1
    add sp, sp, #36
    ldmia sp!, {r3, r4, pc}
    dcd 0x022382c8
    dcd 0x022383cc
    dcd native_data_0222ba8c
}
