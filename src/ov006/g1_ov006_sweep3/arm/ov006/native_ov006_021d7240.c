/* ov006 row 0x021d7240: 568 bytes.
 *
 * What it does: first row of the overlay: 24 helper calls and display/engine control writes, then a seven-way dispatch on a value in 28..34 through an inline branch table at 0x021d7330
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

extern void native_fn_0203cb2c(void);
extern void native_fn_02002e5c(void);
extern void native_fn_020030ec(void);
extern void native_fn_0202a090(void);
extern void native_fn_0202a32c(void);
extern void native_fn_020848d0(void);
extern void native_fn_0205db90(void);
extern void native_fn_0205d9e8(void);
extern void native_fn_0205df8c(void);
extern void native_fn_02046150(void);
extern void native_fn_021d7f68(void);
extern void native_fn_020273d8(void);
extern void native_fn_020642dc(void);
extern void native_fn_020653d0(void);
extern void native_fn_021da3e8(void);
extern void native_fn_02067754(void);
extern void native_fn_02067828(void);
extern void native_fn_020ba564(void);
extern void native_fn_020414b0(void);
extern void native_fn_02041898(void);
extern u8 native_data_0220cae4[];
extern u8 native_data_0220caf0[];


asm u32 native_ov006_021d7240 (register u32 a0)
{
    stmdb sp!, {lr}
    sub sp, sp, #36
    bl native_fn_0203cb2c
    mov r0, #9
    bl native_fn_02002e5c
    mov r0, #2
    bl native_fn_020030ec
    mov r0, #2
    mov r1, #169984
    bl native_fn_0202a090
    mov r0, #1
    bl native_fn_0202a32c
    cmp r0, #0
    bne L_021d7284
    mov r0, #1
    mov r1, #716800
    bl native_fn_0202a090
L_021d7284:
    bl native_fn_020848d0
    ldr r1, [pc, #0x1d4]
    add r0, sp, #4
    mvn r2, #0
    bl native_fn_0205db90
    mov r12, #16
    ldr r2, [pc, #0x1c4]
    ldr r3, [pc, #0x1c4]
    add r1, sp, #4
    mov r0, #2
    str r12, [sp]
    bl native_fn_0205d9e8
    ldr r1, [pc, #0x1b4]
    str r0, [r1, #0x28]
    bl native_fn_0205df8c
    mov r0, #0
    mov r1, r0
    mov r2, #2
    bl native_fn_02046150
    ldr r0, [pc, #0x19c]
    mov r1, #4
    bl native_fn_021d7f68
    mov r0, #11
    bl native_fn_020273d8
    ldr r0, [pc, #0x184]
    mov r2, #15
    mov r1, #0
    str r2, [r0, #0x8]
    str r1, [r0, #0xc]
    mov r1, #67108864
    ldr r0, [r1]
    bic r0, r0, #7936
    orr r0, r0, #4096
    str r0, [r1]
    bl native_fn_020642dc
    cmp r0, #49
    bgt L_021d7358
    bge L_021d73b4
    cmp r0, #34
    bgt L_021d734c
    subs r1, r0, #28
    addpl pc, pc, r1, lsl #2
    b L_021d73e8
    dcd 0xea00000f
    dcd 0xea00000e
    dcd 0xea00000d
    dcd 0xea000029
    dcd 0xea000021
    dcd 0xea00000a
    dcd 0xea00000d
L_021d734c:
    cmp r0, #48
    beq L_021d73b4
    b L_021d73e8
L_021d7358:
    cmp r0, #50
    bgt L_021d7368
    beq L_021d73b4
    b L_021d73e8
L_021d7368:
    cmp r0, #52
    beq L_021d73b4
    b L_021d73e8
    ldr r0, [pc, #0xf4]
    mov r1, #2
    str r1, [r0, #0xc]
    b L_021d73fc
    bl native_fn_020653d0
    cmp r0, #0
    bne L_021d739c
    mov r0, #0
    bl native_fn_021da3e8
    b L_021d73a4
L_021d739c:
    mov r0, #1
    bl native_fn_021da3e8
L_021d73a4:
    ldr r0, [pc, #0xc4]
    mov r1, #1
    str r1, [r0, #0xc]
    b L_021d73fc
L_021d73b4:
    mov r0, #4
    bl native_fn_021da3e8
    ldr r0, [pc, #0xac]
    mov r1, #1
    str r1, [r0, #0xc]
    b L_021d73fc
    ldr r0, [pc, #0x9c]
    mov r1, #1
    str r1, [r0, #0x4]
    ldr r1, [r0, #0xc]
    add sp, sp, #36
    str r1, [r0, #0x2c]
    ldmia sp!, {pc}
L_021d73e8:
    bl native_fn_02067754
    bl native_fn_02067828
    ldr r0, [pc, #0x78]
    mov r1, #14
    str r1, [r0, #0xc]
L_021d73fc:
    ldr r0, [pc, #0x6c]
    ldr r2, [r0, #0xc]
    cmp r2, #0
    bne L_021d7420
    mov r1, #1
    str r1, [r0, #0x4]
    str r2, [r0, #0x2c]
    add sp, sp, #36
    ldmia sp!, {pc}
L_021d7420:
    bl native_fn_020ba564
    cmp r0, #0
    bne L_021d7438
    mov r0, #63
    bl native_fn_020414b0
    b L_021d7440
L_021d7438:
    mov r0, #47
    bl native_fn_020414b0
L_021d7440:
    mov r0, #2
    bl native_fn_02041898
    ldr r0, [pc, #0x20]
    mov r1, #0
    ldr r2, [r0, #0xc]
    str r2, [r0, #0x2c]
    str r1, [r0, #0x4]
    add sp, sp, #36
    ldmia sp!, {pc}
    dcd native_data_0220cae4
    dcd 0x020dc368
    dcd 0x020dc348
    dcd 0x0220e9a0
    dcd native_data_0220caf0
}
