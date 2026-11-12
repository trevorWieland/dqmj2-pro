/* ov006 row 0x021d7478: 696 bytes.
 *
 * What it does: switch dispatch through an inline table
 *
 * Carrier: mwccarm asm with dcd data runs.
 * The measured extent is code plus data inside the function. The data
 * runs are emitted as data, not decoded as instructions; every
 * instruction, branch target, pool word and table entry is read from
 * the image.
 *
 * Unknowns: the field roles and the meaning of the table entries are not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02041764(void);
extern void native_fn_021d822c(void);
extern void native_fn_02048a44(void);
extern void native_fn_02041510(void);
extern void native_fn_020414b0(void);
extern void native_fn_020406a8(void);
extern void native_fn_02041800(void);
extern void native_fn_0206157c(void);
extern void native_fn_02045738(void);
extern void native_fn_020273f0(void);
extern u8 native_data_0220ca30[];
extern u8 native_data_0220ca34[];
extern u8 native_data_0220ca38[];


asm u32 native_ov006_021d7478 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    bl native_fn_02041764
    ldr r0, [pc, #0x290]
    mov r1, #1
    str r1, [r0, #0x540]
    bl native_fn_021d822c
    ldr r6, [pc, #0x284]
    mov r5, #0
    mov r4, #1
L_021d749c:
    mov r1, r4
    add r0, r6, #8
    bl native_fn_02048a44
    add r5, r5, #1
    cmp r5, #10
    add r6, r6, #144
    blt L_021d749c
    ldr r0, [pc, #0x260]
    ldr r1, [r0, #0x4]
    cmp r1, #3
    addls pc, pc, r1, lsl #2
    b L_021d7710
    dcd 0xea000002
    dcd 0xea00001a
    dcd 0xea00005a
    dcd 0xea000076
    ldr r2, [r0, #0xc]
    cmp r2, #0
    beq L_021d74fc
    mov r0, #12
    mul r1, r2, r0
    ldr r0, [pc, #0x22c]
    ldr r0, [r0, r1]
    blx r0
L_021d74fc:
    ldr r0, [pc, #0x21c]
    mov r1, #1
    str r1, [r0, #0x4]
    ldr r0, [r0, #0x14]
    mov r1, #2
    cmp r0, #0
    mov r0, #0
    bne L_021d7528
    mov r2, r1
    bl native_fn_02041510
    b L_021d7530
L_021d7528:
    mov r2, #30
    bl native_fn_02041510
L_021d7530:
    ldr r0, [pc, #0x1e8]
    mov r1, #0
    str r1, [r0, #0x14]
    b L_021d7710
    ldr r2, [r0, #0xc]
    cmp r2, #0
    beq L_021d7560
    mov r0, #12
    mul r1, r2, r0
    ldr r0, [pc, #0x1cc]
    ldr r0, [r0, r1]
    blx r0
L_021d7560:
    ldr r1, [pc, #0x1b8]
    ldr r2, [r1, #0xc]
    ldr r0, [r1, #0x2c]
    cmp r0, r2
    beq L_021d75f4
    cmp r2, #0
    bne L_021d758c
    str r0, [r1, #0xc]
    mov r0, #0
    str r0, [r1, #0x4]
    b L_021d7710
L_021d758c:
    mov r2, #2
    mov r0, #47
    str r2, [r1, #0x4]
    bl native_fn_020414b0
    ldr r0, [pc, #0x17c]
    ldr r1, [r0, #0x14]
    cmp r1, #1
    beq L_021d7710
    ldr r0, [r0, #0xc]
    cmp r0, #3
    bne L_021d75c8
    mov r0, #0
    bl native_fn_020406a8
    mov r0, #63
    bl native_fn_020414b0
L_021d75c8:
    ldr r0, [pc, #0x150]
    ldr r0, [r0, #0x2c]
    cmp r0, #3
    bne L_021d75e0
    mov r0, #63
    bl native_fn_020414b0
L_021d75e0:
    mov r1, #2
    mov r2, r1
    mov r0, #1
    bl native_fn_02041510
    b L_021d7710
L_021d75f4:
    ldr r0, [r1, #0x8]
    cmp r0, #15
    beq L_021d7710
    mov r0, #63
    bl native_fn_020414b0
    ldr r0, [pc, #0x110]
    mov r2, #10
    ldr r0, [r0, #0x8]
    cmp r0, #7
    mov r0, #1
    bne L_021d762c
    mov r1, #3
    bl native_fn_02041510
    b L_021d7634
L_021d762c:
    mov r1, #2
    bl native_fn_02041510
L_021d7634:
    ldr r0, [pc, #0xe4]
    mov r1, #3
    str r1, [r0, #0x4]
    b L_021d7710
    bl native_fn_02041800
    cmp r0, #1
    beq L_021d7710
    ldr r0, [pc, #0xc8]
    ldr r0, [r0, #0xc]
    cmp r0, #3
    bne L_021d766c
    bl native_fn_0206157c
    cmp r0, #0
    beq L_021d7710
L_021d766c:
    ldr r0, [pc, #0xac]
    ldr r0, [r0, #0xc]
    cmp r0, #0
    beq L_021d76a0
    mov r0, #0
    bl native_fn_02045738
    ldr r1, [pc, #0x94]
    mov r0, #12
    ldr r2, [r1, #0xc]
    ldr r1, [pc, #0x94]
    mul r0, r2, r0
    ldr r0, [r1, r0]
    blx r0
L_021d76a0:
    ldr r0, [pc, #0x78]
    mov r1, #0
    ldr r2, [r0, #0x2c]
    str r2, [r0, #0xc]
    str r1, [r0, #0x4]
    b L_021d7710
    bl native_fn_02041800
    cmp r0, #1
    beq L_021d7710
    bl native_fn_020273f0
    cmp r0, #0
    bne L_021d7710
    ldr r0, [pc, #0x48]
    ldr r0, [r0, #0xc]
    cmp r0, #0
    beq L_021d7704
    mov r0, #0
    bl native_fn_02045738
    ldr r1, [pc, #0x30]
    mov r0, #12
    ldr r2, [r1, #0xc]
    ldr r1, [pc, #0x30]
    mul r0, r2, r0
    ldr r0, [r1, r0]
    blx r0
L_021d7704:
    ldr r0, [pc, #0x14]
    ldr r0, [r0, #0x8]
    ldmia sp!, {r4, r5, r6, pc}
L_021d7710:
    mov r0, #15
    ldmia sp!, {r4, r5, r6, pc}
    dcd 0x020feae8
    dcd 0x0220ed54
    dcd 0x0220e9a0
    dcd native_data_0220ca30
    dcd native_data_0220ca34
    dcd native_data_0220ca38
}
