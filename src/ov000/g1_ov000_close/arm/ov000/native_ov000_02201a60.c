/* ov000 row 0x02201a60: 764 bytes.
 *
 * What it does: 185 instructions and 37 call(s), then a 6-entry dispatch through an inline branch table at 0x02201aac (dispatch word at 0x02201aa4)
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

extern void native_fn_02215698(void);
extern void native_fn_0202a634(void);
extern void native_fn_022156c4(void);
extern void native_fn_02062aa0(void);
extern void native_fn_02062ad0(void);
extern void native_fn_02049f24(void);
extern void native_fn_02202070(void);
extern void native_fn_0204b61c(void);
extern void native_fn_0204b5d4(void);
extern void native_fn_0204b5b0(void);
extern void native_fn_02202708(void);
extern void native_fn_02217ac8(void);
extern void native_fn_021e7b9c(void);
extern void native_fn_02201818(void);
extern void native_fn_02201990(void);
extern void native_fn_0206332c(void);
extern void native_fn_0221794c(void);
extern void native_fn_02214008(void);
extern void native_fn_02048094(void);
extern void native_fn_02217bdc(void);
extern void native_fn_02217cf0(void);
extern void native_fn_020632f4(void);
extern void native_fn_022021b4(void);
extern void native_fn_02202674(void);


asm u32 native_ov000_02201a60 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    sub sp, sp, #8
    bl native_fn_02215698
    mov r6, #0
    mov r5, r0
    bl native_fn_0202a634
    mov r4, r0
    bl native_fn_022156c4
    mov r7, r0
    mov r8, r6
    bl native_fn_02062aa0
    bl native_fn_02062ad0
    bl native_fn_02049f24
    ldr r0, [pc, #0x2a8]
    mvn r9, #0
    ldr r0, [r0]
    cmp r0, #5
    addls pc, pc, r0, lsl #2
    b L_02201ccc
    dcd 0xea000004
    dcd 0xea000017
    dcd 0xea000034
    dcd 0xea000048
    dcd 0xea000061
    dcd 0xea00007b
    mov r0, #1
    ldr r6, [pc, #0x278]
    bl native_fn_02202070
    ldr r2, [pc, #0x26c]
    mov r1, #1
    add r0, r5, #16
    str r1, [r2]
    bl native_fn_0204b61c
    add r0, r5, #16
    mov r1, #36
    bl native_fn_0204b5d4
    add r0, r5, #16
    mov r1, #184
    bl native_fn_0204b5b0
    mov r0, #1
    bl native_fn_02202708
    mov r0, #1
    bl native_fn_02217ac8
    mov r8, #1
    b L_02201ccc
    ldrh r0, [r4, #2]
    ldr r6, [pc, #0x228]
    tst r0, #1
    ldr r9, [r6]
    beq L_02201b50
    ldr r0, [pc, #0x21c]
    ldrb r0, [r0, r9]
    cmp r0, #0
    beq L_02201b44
    mov r0, #84
    bl native_fn_021e7b9c
    b L_02201ccc
L_02201b44:
    mov r0, #1
    bl native_fn_02201818
    b L_02201ccc
L_02201b50:
    tst r0, #2
    beq L_02201b7c
    mov r0, #1
    bl native_fn_02201990
    ldr r1, [r6]
    ldr r0, [pc, #0x1e4]
    ldrb r0, [r0, r1]
    sub r0, r0, #12
    and r0, r0, #255
    bl native_fn_0206332c
    b L_02201ccc
L_02201b7c:
    mov r0, r6
    bl native_fn_0221794c
    mov r8, r0
    b L_02201ccc
    mov r0, #3
    ldr r6, [pc, #0x1bc]
    bl native_fn_02202070
    ldr r2, [pc, #0x1a4]
    mov r0, #3
    str r0, [r2]
    mov r3, r8
    add r0, r5, #16
    mov r1, #1
    str r3, [r2, #0x4]
    bl native_fn_0204b61c
    add r0, r5, #16
    mov r1, #36
    bl native_fn_0204b5d4
    add r0, r5, #16
    mov r1, #96
    bl native_fn_0204b5b0
    mov r0, r8
    bl native_fn_02217ac8
    mov r8, #1
    b L_02201ccc
    ldrh r0, [r4, #2]
    ldr r6, [pc, #0x168]
    tst r0, #1
    ldr r9, [r6]
    beq L_02201c24
    ldr r1, [r6, #0x4]
    ldr r0, [pc, #0x14c]
    sub r1, r9, r1
    ldrb r0, [r0, r1]
    cmp r0, #0
    beq L_02201c18
    mov r0, #84
    bl native_fn_021e7b9c
    b L_02201ccc
L_02201c18:
    mov r0, #3
    bl native_fn_02201818
    b L_02201ccc
L_02201c24:
    tst r0, #2
    beq L_02201c38
    mov r0, #3
    bl native_fn_02201990
    b L_02201ccc
L_02201c38:
    mov r0, r6
    bl native_fn_0221794c
    mov r8, r0
    b L_02201ccc
    bl native_fn_02214008
    cmp r0, #0
    mov r4, #82
    ble L_02201c80
    mov r1, r6
    bl native_fn_02048094
    mov r3, #1
    str r3, [sp]
    mov r0, #5
    mov r1, #6
    mov r2, #34
    str r4, [sp, #0x4]
    bl native_fn_02217bdc
    b L_02201c9c
L_02201c80:
    mov r3, #1
    str r3, [sp]
    mov r0, #5
    mov r1, #6
    mov r2, #36
    str r4, [sp, #0x4]
    bl native_fn_02217bdc
L_02201c9c:
    add r0, r5, #16
    bl native_fn_02217cf0
    ldr r0, [pc, #0x98]
    mov r1, #5
    str r1, [r0]
    b L_02201ccc
    ldrh r1, [r4, #2]
    ldr r0, [pc, #0x98]
    tst r1, r0
    beq L_02201ccc
    mov r0, #5
    bl native_fn_02201990
L_02201ccc:
    cmp r8, #0
    beq L_02201d28
    ldr r0, [pc, #0x68]
    ldr r0, [r0]
    cmp r0, #1
    bne L_02201d1c
    mvn r0, #0
    cmp r9, r0
    beq L_02201d1c
    ldr r0, [pc, #0x58]
    and r1, r9, #255
    ldrb r0, [r0, r1]
    sub r0, r0, #12
    and r4, r0, #255
    mov r0, r4
    bl native_fn_020632f4
    cmp r0, #0
    beq L_02201d1c
    mov r0, r4
    bl native_fn_0206332c
L_02201d1c:
    ldr r0, [pc, #0x20]
    ldr r0, [r0]
    bl native_fn_022021b4
L_02201d28:
    cmp r6, #0
    beq L_02201d38
    mov r0, r6
    bl native_fn_02202674
L_02201d38:
    mov r0, r7
    add sp, sp, #8
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
    dcd 0x02237d94
    dcd 0x02237d9c
    dcd 0x02238188
    dcd 0x02237f7c
    dcd 0x02237e8c
    dcd 0x00000ff7
}
