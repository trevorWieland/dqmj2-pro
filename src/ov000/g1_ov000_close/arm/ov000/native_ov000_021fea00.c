/* ov000 row 0x021fea00: 596 bytes.
 *
 * What it does: 145 instructions and 36 call(s), then a 4-entry dispatch through an inline branch table at 0x021fea44 (dispatch word at 0x021fea3c)
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
extern void native_fn_021fedf0(void);
extern void native_fn_0204b61c(void);
extern void native_fn_0206dcd0(void);
extern void native_fn_02217ac8(void);
extern void native_fn_02216664(void);
extern void native_fn_021e7b9c(void);
extern void native_fn_021fe964(void);
extern void native_fn_0221570c(void);
extern void native_fn_0221794c(void);
extern void native_fn_0204b5d4(void);
extern void native_fn_0204b5b0(void);
extern void native_fn_020630cc(void);
extern void native_fn_021fefdc(void);
extern void native_fn_021ff3e4(void);
extern void native_fn_020642dc(void);
extern void native_fn_01ffa4b4(void);


asm u32 native_ov000_021fea00 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
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
    ldr r2, [pc, #0x20c]
    ldr r0, [r2]
    cmp r0, #3
    addls pc, pc, r0, lsl #2
    b L_021febfc
    dcd 0xea000002
    dcd 0xea000012
    dcd 0xea00003a
    dcd 0xea00004c
    ldr r6, [pc, #0x1ec]
    mov r0, #1
    bl native_fn_021fedf0
    add r0, r5, #16
    mov r1, #1
    bl native_fn_0204b61c
    ldr r1, [r6]
    ldr r0, [pc, #0x1d4]
    ldr r0, [r0, r1, lsl #2]
    bl native_fn_0206dcd0
    ldr r1, [pc, #0x1c0]
    mov r2, #1
    mov r0, r8
    str r2, [r1]
    bl native_fn_02217ac8
    mov r8, #1
    b L_021febfc
    ldrh r0, [r4, #2]
    ldr r6, [pc, #0x1a4]
    tst r0, #1
    beq L_021feb04
    ldrh r0, [r6, #12]
    ldr r3, [r6]
    sub r0, r0, #1
    cmp r3, r0
    beq L_021feaf0
    mov r1, #2
    str r1, [r2]
    ldr r0, [pc, #0x180]
    mov r1, r8
    ldr r3, [r0, r3, lsl #2]
    add r0, r5, #16
    str r3, [r2, #0x1e8]
    bl native_fn_0204b61c
    mov r0, r6
    bl native_fn_02216664
    mov r0, #82
    bl native_fn_021e7b9c
    b L_021febfc
L_021feaf0:
    mov r0, #1
    bl native_fn_021fe964
    mov r0, #1
    bl native_fn_0221570c
    b L_021febfc
L_021feb04:
    tst r0, #2
    beq L_021feb18
    mov r0, #1
    bl native_fn_021fe964
    b L_021febfc
L_021feb18:
    mov r0, r6
    bl native_fn_0221794c
    movs r8, r0
    beq L_021febfc
    ldr r1, [r6]
    ldr r0, [pc, #0x118]
    ldr r0, [r0, r1, lsl #2]
    bl native_fn_0206dcd0
    b L_021febfc
    mov r0, #3
    ldr r6, [pc, #0x108]
    bl native_fn_021fedf0
    ldr r2, [pc, #0xf4]
    mov r3, #3
    add r0, r5, #16
    mov r1, #1
    str r3, [r2]
    bl native_fn_0204b61c
    add r0, r5, #16
    mov r1, #36
    bl native_fn_0204b5d4
    add r0, r5, #16
    mov r1, #224
    bl native_fn_0204b5b0
    mov r0, #1
    bl native_fn_02217ac8
    mov r8, #1
    b L_021febfc
    ldr r6, [pc, #0xc0]
    mov r0, r6
    bl native_fn_0221794c
    ldrh r1, [r4, #2]
    mov r8, r0
    tst r1, #1
    beq L_021febe4
    ldr r0, [pc, #0x98]
    ldr r2, [r0, #0x1e8]
    ldr r1, [r0, #0xf8]
    ldr r0, [r2, #0x14]
    and r1, r1, #255
    bl native_fn_020630cc
    ldr r2, [pc, #0x80]
    mov r1, #0
    add r0, r5, #16
    str r1, [r2]
    bl native_fn_0204b61c
    mov r0, #3
    bl native_fn_021fe964
    mov r0, #82
    bl native_fn_021e7b9c
    b L_021febfc
L_021febe4:
    tst r1, #2
    beq L_021febfc
    mov r0, #3
    bl native_fn_021fe964
    mov r0, #83
    bl native_fn_021e7b9c
L_021febfc:
    cmp r8, #0
    beq L_021fec10
    ldr r0, [pc, #0x38]
    ldr r0, [r0]
    bl native_fn_021fefdc
L_021fec10:
    cmp r6, #0
    beq L_021fec20
    mov r0, r6
    bl native_fn_021ff3e4
L_021fec20:
    bl native_fn_020642dc
    cmp r0, #16
    blt L_021fec3c
    bl native_fn_020642dc
    cmp r0, #18
    bgt L_021fec3c
    bl native_fn_01ffa4b4
L_021fec3c:
    mov r0, r7
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
    dcd 0x02237564
    dcd 0x0223756c
    dcd 0x02237754
    dcd 0x0223765c
}
