/* ov000 row 0x021ecff0: 496 bytes.
 *
 * What it does: 123 instructions and 16 call(s), then a 5-entry dispatch through an inline branch table at 0x021ed014 (dispatch word at 0x021ed00c)
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

extern void native_fn_020494bc(void);
extern void native_fn_0202a634(void);
extern void native_fn_0205e7a8(void);
extern void native_fn_020491f8(void);
extern void native_fn_021ee300(void);
extern void native_fn_02062aa0(void);
extern void native_fn_02062a50(void);
extern void native_fn_02062a88(void);
extern void native_fn_0206dcd0(void);


asm u32 native_ov000_021ecff0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    sub sp, sp, #8
    ldr r1, [pc, #0x1dc]
    mov r4, r0
    ldr r1, [r1, #0x4]
    ldrsb r0, [r1, #32]
    cmp r0, #4
    addls pc, pc, r0, lsl #2
    b L_021ed1d4
    dcd 0xea000003
    dcd 0xea000002
    dcd 0xea000001
    dcd 0xea000043
    dcd 0xea00004f
    ldrb r0, [r1, #0x101]
    cmp r0, #0
    beq L_021ed0c8
    add r1, r1, #1280
    ldrsh r2, [r1, #6]
    mov r3, #0
    add r0, sp, #4
    str r2, [sp, #0x4]
    str r3, [sp]
    ldrsh r1, [r1, #8]
    mov r2, #1
    bl native_fn_020494bc
    bl native_fn_0202a634
    ldrh r0, [r0, #6]
    tst r0, #240
    beq L_021ed090
    ldr r0, [pc, #0x16c]
    ldr r1, [sp, #0x4]
    ldr r0, [r0, #0x4]
    add r0, r0, #1280
    ldrsh r0, [r0, #6]
    cmp r1, r0
    movne r1, #95
    moveq r1, #84
    mvn r0, #0
    bl native_fn_0205e7a8
L_021ed090:
    ldr r0, [pc, #0x144]
    ldr r2, [sp, #0x4]
    ldr r0, [r0, #0x4]
    add r0, r0, #1280
    ldrsh r1, [r0, #6]
    cmp r2, r1
    addeq sp, sp, #8
    ldmeqia sp!, {r3, r4, r5, pc}
    strh r2, [r0, #6]
    ldrb r0, [r4]
    add sp, sp, #8
    orr r0, r0, #4
    strb r0, [r4]
    ldmia sp!, {r3, r4, r5, pc}
L_021ed0c8:
    add r0, r1, #16
    ldr r5, [r1, #0x14]
    bl native_fn_020491f8
    cmp r0, #0
    addeq sp, sp, #8
    ldmeqia sp!, {r3, r4, r5, pc}
    ldrb r1, [r4]
    ldr r0, [pc, #0xf0]
    orr r1, r1, #1
    strb r1, [r4]
    ldr r0, [r0, #0x4]
    ldr r0, [r0, #0x14]
    cmp r5, r0
    beq L_021ed11c
    ldrb r2, [r4]
    mvn r0, #0
    mov r1, #86
    orr r2, r2, #2
    strb r2, [r4]
    bl native_fn_0205e7a8
    b L_021ed128
L_021ed11c:
    mvn r0, #0
    mov r1, #85
    bl native_fn_0205e7a8
L_021ed128:
    bl native_fn_021ee300
    add sp, sp, #8
    ldmia sp!, {r3, r4, r5, pc}
    add r0, r1, #16
    bl native_fn_020491f8
    cmp r0, #0
    addeq sp, sp, #8
    ldmeqia sp!, {r3, r4, r5, pc}
    mvn r0, #0
    mov r1, #85
    bl native_fn_0205e7a8
    ldrb r0, [r4]
    add sp, sp, #8
    orr r0, r0, #1
    strb r0, [r4]
    ldmia sp!, {r3, r4, r5, pc}
    add r0, r1, #16
    bl native_fn_020491f8
    cmp r0, #0
    addeq sp, sp, #8
    ldmeqia sp!, {r3, r4, r5, pc}
    ldr r0, [pc, #0x58]
    ldr r0, [r0, #0x4]
    ldr r5, [r0, #0x10]
    bl native_fn_02062aa0
    cmp r5, r0
    bge L_021ed1a0
    mov r0, r5
    bl native_fn_02062a50
    b L_021ed1b8
L_021ed1a0:
    bl native_fn_02062aa0
    ldr r1, [pc, #0x30]
    ldr r1, [r1, #0x4]
    ldr r1, [r1, #0x10]
    sub r0, r1, r0
    bl native_fn_02062a88
L_021ed1b8:
    bl native_fn_0206dcd0
    mvn r0, #0
    mov r1, #85
    bl native_fn_0205e7a8
    ldrb r0, [r4]
    orr r0, r0, #1
    strb r0, [r4]
L_021ed1d4:
    add sp, sp, #8
    ldmia sp!, {r3, r4, r5, pc}
    dcd 0x02236bc4
}
