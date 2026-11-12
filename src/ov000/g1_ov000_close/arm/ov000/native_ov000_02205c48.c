/* ov000 row 0x02205c48: 540 bytes.
 *
 * What it does: 130 instructions and 10 call(s), then a 4-entry dispatch through an inline branch table at 0x02205c88 (dispatch word at 0x02205c80)
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

extern void native_fn_020044ac(void);
extern void native_fn_020045d8(void);
extern void native_fn_0207e4ac(void);
extern void native_fn_0207df2c(void);
extern void native_fn_0207e3f8(void);
extern void native_fn_0207e508(void);
extern void native_fn_020c225c(void);
extern void native_fn_020273d8(void);
extern void native_fn_02041764(void);
extern u8 native_data_0222f584[];
extern u8 native_data_0222f588[];


asm u32 native_ov000_02205c48 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r8, #7
    mov r9, #1
    bl native_fn_020044ac
    bl native_fn_020045d8
    mov r7, r8
    mov r10, #2
    mov r11, #0
    ldr r5, [pc, #0x1e0]
    ldr r4, [pc, #0x1e0]
    ldr r6, [pc, #0x1e0]
    b L_02205e3c
L_02205c78:
    ldrsb r0, [r6, #3]
    cmp r0, #3
    addls pc, pc, r0, lsl #2
    b L_02205e3c
    dcd 0xea000002
    dcd 0xea000005
    dcd 0xea00002c
    dcd 0xea000064
    mov r0, #1
    strb r0, [r6, #0x3]
    mov r9, r0
    b L_02205e3c
    ldrb r0, [r5]
    bic r0, r0, #1
    strb r0, [r5]
    bl native_fn_0207e4ac
    cmp r0, #0
    beq L_02205d38
    ldr r1, [pc, #0x194]
    mov r0, #0
    bl native_fn_0207df2c
    cmp r0, #0
    bne L_02205cf8
    bl native_fn_0207e3f8
    cmp r0, #3
    bne L_02205cec
    mov r0, #0
    bl native_fn_0207e508
    b L_02205d08
L_02205cec:
    mov r0, #1610612736
    bl native_fn_020c225c
    b L_02205d08
L_02205cf8:
    ldrb r0, [r5]
    bic r0, r0, #1
    orr r0, r0, #1
    strb r0, [r5]
L_02205d08:
    mov r0, #6
    bl native_fn_020273d8
    str r7, [r4]
    strb r10, [r6, #0x3]
    strb r11, [r6]
    strb r11, [r6, #0x1]
    ldrb r0, [r5]
    bic r0, r0, #4
    strb r0, [r5]
    mov r0, #1
    strb r0, [r6, #0x2]
    b L_02205d40
L_02205d38:
    mov r0, #1342177280
    bl native_fn_020c225c
L_02205d40:
    mov r9, #0
    b L_02205e3c
    ldrsb r3, [r6]
    ldr r0, [pc, #0x10c]
    mov r1, #12
    ldrsb r2, [r6, #2]
    mla r9, r3, r1, r0
    cmp r2, #0
    beq L_02205d7c
    ldr r0, [r9]
    cmp r0, #0
    beq L_02205d74
    blx r0
L_02205d74:
    mov r0, #0
    strb r0, [r6, #0x2]
L_02205d7c:
    ldr r0, [r9, #0x4]
    cmp r0, #0
    beq L_02205ddc
    blx r0
    cmp r0, #0
    beq L_02205e24
    ldr r0, [r9, #0x8]
    cmp r0, #0
    beq L_02205da4
    blx r0
L_02205da4:
    ldrsb r0, [r6, #1]
    strb r0, [r6]
    mov r0, #1
    strb r0, [r6, #0x2]
    ldrb r0, [r5]
    mov r1, r0, lsl #29
    movs r1, r1, lsr #31
    beq L_02205e24
    bic r0, r0, #4
    strb r0, [r5]
    mov r0, #3
    strb r0, [r6, #0x3]
    mov r9, #1
    b L_02205e3c
L_02205ddc:
    ldr r0, [r9, #0x8]
    cmp r0, #0
    beq L_02205dec
    blx r0
L_02205dec:
    ldrsb r0, [r6, #1]
    strb r0, [r6]
    mov r0, #1
    strb r0, [r6, #0x2]
    ldrb r0, [r5]
    mov r1, r0, lsl #29
    movs r1, r1, lsr #31
    beq L_02205e24
    bic r0, r0, #4
    strb r0, [r5]
    mov r0, #3
    strb r0, [r6, #0x3]
    mov r9, #1
    b L_02205e3c
L_02205e24:
    mov r9, #0
    b L_02205e3c
    mov r0, #0
    ldr r8, [r4]
    strb r0, [r6, #0x3]
    mov r9, r0
L_02205e3c:
    cmp r9, #0
    bne L_02205c78
    bl native_fn_02041764
    mov r0, r8
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    dcd 0x022381b4
    dcd native_data_0222f584
    dcd 0x022381a8
    dcd 0x022381b8
    dcd native_data_0222f588
}
