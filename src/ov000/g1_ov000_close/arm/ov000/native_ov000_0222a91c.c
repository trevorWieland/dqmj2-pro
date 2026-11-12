/* ov000 row 0x0222a91c: 580 bytes.
 *
 * What it does: 141 instructions and 21 call(s), then a 9-entry dispatch through an inline branch table at 0x0222a968 (dispatch word at 0x0222a960)
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
extern void native_fn_0222abf4(void);
extern void native_fn_02062520(void);
extern void native_fn_0222ab60(void);
extern void native_fn_02041538(void);
extern void native_fn_0222acc0(void);
extern void native_fn_0222ad00(void);
extern void native_fn_0222ac94(void);
extern void native_fn_0205e7a8(void);
extern void native_fn_0222ac5c(void);
extern void native_fn_020633b0(void);
extern void native_fn_0222b610(void);
extern void native_fn_0222ad94(void);
extern void native_fn_0222b044(void);
extern void native_fn_0222ac9c(void);
extern void native_fn_020c4318(void);
extern void native_fn_02062074(void);
extern void native_fn_02041814(void);


asm u32 native_ov000_0222a91c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #8
    mov r11, #6
    bl native_fn_0202a634
    ldr r6, [pc, #0x21c]
    mov r8, r0
    ldrsb r0, [r6, #32]
    ldr r7, [pc, #0x214]
    ldr r10, [pc, #0x214]
    str r0, [sp]
    mvn r0, #0
    ldr r5, [pc, #0x20c]
    add r4, r6, #256
    str r0, [sp, #0x4]
L_0222a954:
    ldrb r0, [r6, #0x100]
    mov r9, #0
    cmp r0, #8
    addls pc, pc, r0, lsl #2
    b L_0222ab30
    dcd 0xea000007
    dcd 0xea00000b
    dcd 0xea000020
    dcd 0xea000051
    dcd 0xea000053
    dcd 0xea000057
    dcd 0xea00005b
    dcd 0xea000064
    dcd 0xea000068
    bl native_fn_0222abf4
    mov r0, #1
    strb r0, [r6, #0x103]
    strb r0, [r6, #0x100]
    b L_0222ab30
    ldrsb r0, [r4, #3]
    cmp r0, #0
    beq L_0222a9b8
    bl native_fn_02062520
    cmp r0, #0
    beq L_0222ab30
L_0222a9b8:
    bl native_fn_0222ab60
    mov r0, #2
    strb r0, [r6, #0x100]
    ldrsb r0, [r4, #3]
    cmp r0, #0
    beq L_0222a9e8
    mov r0, #0
    mov r1, #2
    mov r2, #10
    bl native_fn_02041538
    mov r0, #0
    strb r0, [r6, #0x103]
L_0222a9e8:
    mov r0, #1
    str r0, [r5, #0x4]
    mov r9, r0
    b L_0222ab30
    ldrh r1, [r8, #2]
    tst r1, #2
    beq L_0222aa28
    mov r0, r7
    bl native_fn_0222acc0
    ldrsb r1, [r6, #32]
    cmp r0, r1
    beq L_0222aa8c
    strb r0, [r6, #0x101]
    mov r0, #3
    strb r0, [r6, #0x100]
    b L_0222aa8c
L_0222aa28:
    ldrh r0, [r8]
    tst r0, #1
    beq L_0222aa58
    mov r0, r7
    bl native_fn_0222ad00
    ldrsb r1, [r6, #32]
    cmp r0, r1
    beq L_0222aa8c
    strb r0, [r6, #0x101]
    mov r0, #3
    strb r0, [r6, #0x100]
    b L_0222aa8c
L_0222aa58:
    tst r1, #2048
    beq L_0222aa84
    bl native_fn_0222ac94
    cmp r0, #0
    beq L_0222aa8c
    ldr r0, [sp, #0x4]
    mov r1, #82
    bl native_fn_0205e7a8
    mov r0, #4
    strb r0, [r6, #0x100]
    b L_0222aa8c
L_0222aa84:
    mov r0, r7
    bl native_fn_0222ac5c
L_0222aa8c:
    ldr r0, [r5, #0x4]
    cmp r0, #1
    bne L_0222aab4
    bl native_fn_020633b0
    ldr r1, [r5, #0x4]
    mov r0, r10
    bl native_fn_0222b610
    bl native_fn_0222ad94
    mov r0, #0
    str r0, [r5, #0x4]
L_0222aab4:
    mov r0, r10
    bl native_fn_0222b044
    b L_0222ab30
    bl native_fn_0222ac9c
    mov r11, r0
    b L_0222ab30
    bl native_fn_020c4318
    cmp r0, #0
    movne r0, #2
    strneb r0, [r6, #0x100]
    b L_0222ab30
    bl native_fn_020c4318
    cmp r0, #0
    movne r0, #3
    strneb r0, [r6, #0x100]
    b L_0222ab30
    mov r0, r9
    bl native_fn_02062074
    mov r0, #1
    mov r1, #2
    mov r2, #10
    bl native_fn_02041538
    mov r0, #7
    strb r0, [r6, #0x100]
    mov r9, #1
    b L_0222ab30
    mov r0, r10
    bl native_fn_0222b044
    bl native_fn_02041814
    cmp r0, #1
    movne r11, #9
L_0222ab30:
    cmp r9, #0
    bne L_0222a954
    ldr r2, [pc, #0x10]
    ldr r1, [sp]
    mov r0, r11
    strb r1, [r2, #0x102]
    add sp, sp, #8
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    dcd 0x022475ec
    dcd 0x022475d8
    dcd 0x022475fc
    dcd 0x022475d4
}
