/* ov000 row 0x0221e480: 588 bytes.
 *
 * What it does: 144 instructions and 21 call(s), then a 11-entry dispatch through an inline branch table at 0x0221e4a4 (dispatch word at 0x0221e49c)
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

extern void native_fn_0204b61c(void);
extern void native_fn_02049130(void);
extern void native_fn_0205f9e4(void);
extern void native_fn_022213d8(void);
extern void native_fn_0204b5b0(void);
extern void native_fn_0204b53c(void);
extern u8 native_data_0222fb1c[];


asm u32 native_ov000_0221e480 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, lr}
    sub sp, sp, #4
    mov r5, r0
    ldrsb r2, [r5, #16]
    mov r1, #0
    mov r4, r1
    cmp r2, #10
    addls pc, pc, r2, lsl #2
    b L_0221e640
    dcd 0xea000065
    dcd 0xea000008
    dcd 0xea000018
    dcd 0xea000017
    dcd 0xea000061
    dcd 0xea000060
    dcd 0xea000057
    dcd 0xea000056
    dcd 0xea000040
    dcd 0xea00005c
    dcd 0xea000053
    ldr r2, [pc, #0x1e8]
    mov r4, #1
    ldrb r2, [r2, #0x1]
    cmp r2, #0
    bne L_0221e4f4
    ldr r0, [pc, #0x1d8]
    ldr r0, [r0, #0x14]
    bl native_fn_0204b61c
    b L_0221e688
L_0221e4f4:
    ldr r2, [pc, #0x1c8]
    mov r1, #10
    ldr r2, [r2, #0x14]
    bl native_fn_02049130
    ldr r0, [pc, #0x1b8]
    ldr r0, [r0, #0x14]
    bl native_fn_0205f9e4
    b L_0221e688
    ldr r0, [pc, #0x1a4]
    mov r4, #2
    ldrb r0, [r0]
    cmp r0, #0
    beq L_0221e578
    mov r0, #8
    strh r0, [sp]
    bl native_fn_022213d8
    mov r1, r0, lsl #1
    ldr r0, [pc, #0x184]
    add r1, r1, #6
    mov r2, r1, lsl #3
    ldr r0, [r0, #0x18]
    mov r1, #120
    strh r2, [sp, #2]
    bl native_fn_0204b5b0
    ldr r0, [pc, #0x168]
    add r1, sp, #0
    ldr r0, [r0, #0x18]
    bl native_fn_0204b53c
    ldr r0, [pc, #0x158]
    mov r1, #1
    ldr r0, [r0, #0x18]
    bl native_fn_0204b61c
    b L_0221e584
L_0221e578:
    ldr r0, [pc, #0x144]
    ldr r0, [r0, #0x18]
    bl native_fn_0204b61c
L_0221e584:
    ldr r0, [pc, #0x134]
    ldrb r0, [r0, #0x1]
    cmp r0, #0
    bne L_0221e5a8
    ldr r0, [pc, #0x128]
    mov r1, #0
    ldr r0, [r0, #0x14]
    bl native_fn_0204b61c
    b L_0221e688
L_0221e5a8:
    ldr r1, [pc, #0x114]
    mov r0, r5
    ldr r2, [r1, #0x14]
    mov r1, #20
    bl native_fn_02049130
    ldr r0, [pc, #0x100]
    ldr r0, [r0, #0x14]
    bl native_fn_0205f9e4
    b L_0221e688
    ldr r2, [pc, #0xec]
    mov r4, #1
    ldrb r2, [r2, #0x1]
    cmp r2, #0
    bne L_0221e5f0
    ldr r0, [pc, #0xdc]
    ldr r0, [r0, #0x14]
    bl native_fn_0204b61c
    b L_0221e688
L_0221e5f0:
    ldr r2, [pc, #0xcc]
    mov r1, #10
    ldr r2, [r2, #0x14]
    bl native_fn_02049130
    ldr r0, [pc, #0xbc]
    mov r1, #224
    ldr r0, [r0, #0x14]
    bl native_fn_0204b5b0
    ldr r0, [pc, #0xac]
    ldr r0, [r0, #0x14]
    bl native_fn_0205f9e4
    b L_0221e688
    ldr r0, [pc, #0x98]
    ldrb r0, [r0, #0x1]
    cmp r0, #0
    bne L_0221e688
    ldr r0, [pc, #0x8c]
    ldr r0, [r0, #0x14]
    bl native_fn_0204b61c
    b L_0221e688
L_0221e640:
    ldr r0, [pc, #0x78]
    mov r4, #1
    ldrb r0, [r0, #0x1]
    cmp r0, #0
    bne L_0221e668
    ldr r0, [pc, #0x68]
    mov r1, #0
    ldr r0, [r0, #0x14]
    bl native_fn_0204b61c
    b L_0221e688
L_0221e668:
    ldr r1, [pc, #0x54]
    mov r0, r5
    ldr r2, [r1, #0x14]
    mov r1, #26
    bl native_fn_02049130
    ldr r0, [pc, #0x40]
    ldr r0, [r0, #0x14]
    bl native_fn_0205f9e4
L_0221e688:
    cmp r4, #5
    addhs sp, sp, #4
    ldmhsia sp!, {r3, r4, r5, r6, pc}
    ldr r6, [pc, #0x2c]
    mov r5, #0
L_0221e69c:
    ldr r0, [r6, r4, lsl #2]
    mov r1, r5
    bl native_fn_0204b61c
    add r0, r4, #1
    and r4, r0, #255
    cmp r4, #5
    blo L_0221e69c
    add sp, sp, #4
    ldmia sp!, {r3, r4, r5, r6, pc}
    dcd native_data_0222fb1c
    dcd 0x02246318
    dcd 0x0224632c
}
