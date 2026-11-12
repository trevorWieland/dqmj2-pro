/* ov000 row 0x021f6294: 740 bytes.
 *
 * What it does: 172 instructions and 37 call(s), then a 12-entry dispatch through an inline branch table at 0x021f62ac (dispatch word at 0x021f62a4)
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

extern void native_fn_01ffa8d8(void);
extern void native_fn_021f6248(void);
extern void native_fn_021f6618(void);
extern void native_fn_01ffa948(void);
extern void native_fn_021f662c(void);
extern u8 native_data_0222eef0[];
extern u8 native_data_0222eff4[];
extern u8 native_data_0222eef4[];
extern u8 native_data_0222efb4[];
extern u8 native_data_0222ef34[];
extern u8 native_data_0222ef74[];
extern u8 native_data_0222f04c[];
extern u8 native_data_0222f0a4[];
extern u8 native_data_0222f0fc[];
extern u8 native_data_0222f154[];
extern u8 native_data_0222f1ac[];
extern u8 native_data_0222f204[];
extern u8 native_data_0222f25c[];


asm u32 native_ov000_021f6294 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r0, [pc, #0x2a4]
    ldrb r0, [r0, #0x1]
    cmp r0, #11
    addls pc, pc, r0, lsl #2
    b L_021f653c
    dcd 0xea00000a
    dcd 0xea000027
    dcd 0xea00003c
    dcd 0xea000042
    dcd 0xea00004d
    dcd 0xea000058
    dcd 0xea000063
    dcd 0xea00006e
    dcd 0xea000079
    dcd 0xea000084
    dcd 0xea00008f
    dcd 0xea000095
    bl native_fn_01ffa8d8
    cmp r0, #8
    mov r0, #0
    bne L_021f630c
    ldr r1, [pc, #0x250]
    mov r2, #3
    strb r2, [r1, #0x1]
    bl native_fn_021f6248
    mov r1, r0
    ldr r0, [pc, #0x240]
    bl native_fn_021f6618
    b L_021f653c
L_021f630c:
    bl native_fn_01ffa948
    tst r0, #4
    beq L_021f6330
    mov r0, #0
    bl native_fn_021f6248
    mov r1, r0
    ldr r0, [pc, #0x220]
    bl native_fn_021f6618
    b L_021f6344
L_021f6330:
    mov r0, #1
    bl native_fn_021f6248
    mov r1, r0
    ldr r0, [pc, #0x20c]
    bl native_fn_021f6618
L_021f6344:
    ldr r0, [pc, #0x1f8]
    mov r1, #1
    strb r1, [r0, #0x1]
    b L_021f653c
    bl native_fn_021f662c
    cmp r0, #1
    bne L_021f653c
    mov r0, #2
    bl native_fn_01ffa948
    tst r0, #4
    beq L_021f6388
    mov r0, #2
    bl native_fn_021f6248
    mov r1, r0
    ldr r0, [pc, #0x1d0]
    bl native_fn_021f6618
    b L_021f639c
L_021f6388:
    mov r0, #3
    bl native_fn_021f6248
    mov r1, r0
    ldr r0, [pc, #0x1bc]
    bl native_fn_021f6618
L_021f639c:
    ldr r0, [pc, #0x1a0]
    mov r1, #2
    strb r1, [r0, #0x1]
    b L_021f653c
    bl native_fn_021f662c
    cmp r0, #1
    bne L_021f653c
    ldr r0, [pc, #0x184]
    mov r1, #11
    strb r1, [r0, #0x1]
    b L_021f653c
    bl native_fn_021f662c
    cmp r0, #1
    bne L_021f653c
    mov r0, #1
    bl native_fn_021f6248
    mov r1, r0
    ldr r0, [pc, #0x174]
    bl native_fn_021f6618
    ldr r0, [pc, #0x154]
    mov r1, #4
    strb r1, [r0, #0x1]
    b L_021f653c
    bl native_fn_021f662c
    cmp r0, #1
    bne L_021f653c
    mov r0, #2
    bl native_fn_021f6248
    mov r1, r0
    ldr r0, [pc, #0x148]
    bl native_fn_021f6618
    ldr r0, [pc, #0x124]
    mov r1, #5
    strb r1, [r0, #0x1]
    b L_021f653c
    bl native_fn_021f662c
    cmp r0, #1
    bne L_021f653c
    mov r0, #3
    bl native_fn_021f6248
    mov r1, r0
    ldr r0, [pc, #0x11c]
    bl native_fn_021f6618
    ldr r0, [pc, #0xf4]
    mov r1, #6
    strb r1, [r0, #0x1]
    b L_021f653c
    bl native_fn_021f662c
    cmp r0, #1
    bne L_021f653c
    mov r0, #4
    bl native_fn_021f6248
    mov r1, r0
    ldr r0, [pc, #0xf0]
    bl native_fn_021f6618
    ldr r0, [pc, #0xc4]
    mov r1, #7
    strb r1, [r0, #0x1]
    b L_021f653c
    bl native_fn_021f662c
    cmp r0, #1
    bne L_021f653c
    mov r0, #5
    bl native_fn_021f6248
    mov r1, r0
    ldr r0, [pc, #0xc4]
    bl native_fn_021f6618
    ldr r0, [pc, #0x94]
    mov r1, #8
    strb r1, [r0, #0x1]
    b L_021f653c
    bl native_fn_021f662c
    cmp r0, #1
    bne L_021f653c
    mov r0, #6
    bl native_fn_021f6248
    mov r1, r0
    ldr r0, [pc, #0x98]
    bl native_fn_021f6618
    ldr r0, [pc, #0x64]
    mov r1, #9
    strb r1, [r0, #0x1]
    b L_021f653c
    bl native_fn_021f662c
    cmp r0, #1
    bne L_021f653c
    mov r0, #7
    bl native_fn_021f6248
    mov r1, r0
    ldr r0, [pc, #0x6c]
    bl native_fn_021f6618
    ldr r0, [pc, #0x34]
    mov r1, #10
    strb r1, [r0, #0x1]
    b L_021f653c
    bl native_fn_021f662c
    cmp r0, #1
    bne L_021f653c
    ldr r0, [pc, #0x18]
    mov r1, #11
    strb r1, [r0, #0x1]
    b L_021f653c
    mov r0, #1
    ldmia sp!, {r3, pc}
L_021f653c:
    mov r0, #0
    ldmia sp!, {r3, pc}
    dcd native_data_0222eef0
    dcd native_data_0222eff4
    dcd native_data_0222eef4
    dcd native_data_0222efb4
    dcd native_data_0222ef34
    dcd native_data_0222ef74
    dcd native_data_0222f04c
    dcd native_data_0222f0a4
    dcd native_data_0222f0fc
    dcd native_data_0222f154
    dcd native_data_0222f1ac
    dcd native_data_0222f204
    dcd native_data_0222f25c
}
