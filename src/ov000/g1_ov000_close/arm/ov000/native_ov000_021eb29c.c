/* ov000 row 0x021eb29c: 656 bytes.
 *
 * What it does: 160 instructions and 26 call(s), then a 9-entry dispatch through an inline branch table at 0x021eb2ec (dispatch word at 0x021eb2e4)
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
extern void native_fn_021eb654(void);
extern void native_fn_021ebf9c(void);
extern void native_fn_021ebc34(void);
extern void native_fn_02062520(void);
extern void native_fn_021eb52c(void);
extern void native_fn_02041538(void);
extern void native_fn_021eb720(void);
extern void native_fn_021eb778(void);
extern void native_fn_021eb6f4(void);
extern void native_fn_0205e7a8(void);
extern void native_fn_021eb6bc(void);
extern void native_fn_020633b0(void);
extern void native_fn_021eb950(void);
extern void native_fn_021ec3f4(void);
extern void native_fn_021ec044(void);
extern void native_fn_021eb9e8(void);
extern void native_fn_021ebc80(void);
extern void native_fn_021ebd08(void);
extern void native_fn_021eb6fc(void);
extern void native_fn_020c4318(void);
extern void native_fn_02062074(void);
extern void native_fn_02041814(void);


asm u32 native_ov000_021eb29c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #16
    mov r0, #3
    str r0, [sp, #0x4]
    bl native_fn_0202a634
    ldr r6, [pc, #0x264]
    mov r8, r0
    ldrsb r0, [r6, #32]
    ldr r10, [pc, #0x25c]
    ldr r11, [pc, #0x25c]
    str r0, [sp]
    mvn r0, #0
    ldr r5, [pc, #0x254]
    add r4, r6, #256
    str r0, [sp, #0x8]
L_021eb2d8:
    ldrb r0, [r6, #0x100]
    mov r9, #0
    cmp r0, #8
    addls pc, pc, r0, lsl #2
    b L_021eb4fc
    dcd 0xea000007
    dcd 0xea000016
    dcd 0xea00002b
    dcd 0xea000062
    dcd 0xea000064
    dcd 0xea000068
    dcd 0xea00006c
    dcd 0xea000075
    dcd 0xea00007a
    bl native_fn_021eb654
    bl native_fn_021ebf9c
    mov r1, r9
    add r0, sp, #12
    strh r1, [r0]
    strh r1, [r0, #2]
    mov r0, #120
    strh r0, [sp, #12]
    mov r0, #152
    strh r0, [sp, #14]
    add r0, sp, #12
    bl native_fn_021ebc34
    mov r0, #1
    strb r0, [r6, #0x103]
    strb r0, [r6, #0x100]
    b L_021eb4fc
    ldrsb r0, [r4, #3]
    cmp r0, #0
    beq L_021eb368
    bl native_fn_02062520
    cmp r0, #0
    beq L_021eb4fc
L_021eb368:
    bl native_fn_021eb52c
    mov r0, #2
    strb r0, [r6, #0x100]
    ldrsb r0, [r4, #3]
    cmp r0, #0
    beq L_021eb398
    mov r0, #0
    mov r1, #2
    mov r2, #10
    bl native_fn_02041538
    mov r0, #0
    strb r0, [r6, #0x103]
L_021eb398:
    mov r0, #1
    str r0, [r5]
    mov r9, r0
    b L_021eb4fc
    ldrh r1, [r8, #2]
    tst r1, #2
    beq L_021eb3d8
    mov r0, r10
    bl native_fn_021eb720
    ldrsb r1, [r6, #32]
    cmp r0, r1
    beq L_021eb43c
    strb r0, [r6, #0x101]
    mov r0, #3
    strb r0, [r6, #0x100]
    b L_021eb43c
L_021eb3d8:
    ldrh r0, [r8]
    tst r0, #1
    beq L_021eb408
    mov r0, r10
    bl native_fn_021eb778
    ldrsb r1, [r6, #32]
    cmp r0, r1
    beq L_021eb43c
    strb r0, [r6, #0x101]
    mov r0, #3
    strb r0, [r6, #0x100]
    b L_021eb43c
L_021eb408:
    tst r1, #2048
    beq L_021eb434
    bl native_fn_021eb6f4
    cmp r0, #0
    beq L_021eb43c
    ldr r0, [sp, #0x8]
    mov r1, #82
    bl native_fn_0205e7a8
    mov r0, #4
    strb r0, [r6, #0x100]
    b L_021eb43c
L_021eb434:
    mov r0, r10
    bl native_fn_021eb6bc
L_021eb43c:
    ldr r0, [r5]
    cmp r0, #1
    bne L_021eb47c
    bl native_fn_020633b0
    mov r7, r0
    bl native_fn_021eb950
    ldr r1, [r5]
    mov r0, r11
    bl native_fn_021ec3f4
    ldr r0, [r7, #0x14]
    ldr r1, [r7, #0x18]
    bl native_fn_021ec044
    bl native_fn_021eb9e8
    bl native_fn_021ebc80
    mov r0, #0
    str r0, [r5]
L_021eb47c:
    mov r0, r11
    bl native_fn_021ebd08
    b L_021eb4fc
    bl native_fn_021eb6fc
    str r0, [sp, #0x4]
    b L_021eb4fc
    bl native_fn_020c4318
    cmp r0, #0
    movne r0, #2
    strneb r0, [r6, #0x100]
    b L_021eb4fc
    bl native_fn_020c4318
    cmp r0, #0
    movne r0, #3
    strneb r0, [r6, #0x100]
    b L_021eb4fc
    mov r0, r9
    bl native_fn_02062074
    mov r0, #1
    mov r1, #2
    mov r2, #10
    bl native_fn_02041538
    mov r0, #7
    strb r0, [r6, #0x100]
    mov r9, #1
    b L_021eb4fc
    mov r0, r11
    bl native_fn_021ebd08
    bl native_fn_02041814
    cmp r0, #1
    movne r0, #9
    strne r0, [sp, #0x4]
L_021eb4fc:
    cmp r9, #0
    bne L_021eb2d8
    ldr r2, [pc, #0x10]
    ldr r1, [sp]
    ldr r0, [sp, #0x4]
    strb r1, [r2, #0x102]
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    dcd 0x02236980
    dcd 0x0223697c
    dcd 0x02236990
    dcd 0x0223697c
}
