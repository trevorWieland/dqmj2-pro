/* ov006 row 0x021e674c: 388 bytes.
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

extern void native_fn_020273f0(void);
extern void native_fn_021e9440(void);
extern void native_fn_02041764(void);
extern void native_fn_0204176c(void);
extern void native_fn_021eb8e4(void);
extern void native_fn_021e94e4(void);
extern void native_fn_0205eae4(void);
extern void native_fn_02041814(void);
extern void native_fn_020851a8(void);
extern void native_fn_020851d4(void);
extern void native_fn_02085200(void);
extern void native_fn_020ba574(void);
extern void native_fn_0204bb18(void);
extern void native_fn_021e9e04(void);
extern void native_fn_021e9e78(void);
extern void native_fn_0204bb28(void);
extern u8 native_data_02207eb8[];
extern u8 native_data_02207eb0[];
extern u8 native_data_02207eb4[];


asm u32 native_ov006_021e674c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    bl native_fn_020273f0
    mov r4, r0
    bl native_fn_021e9440
    bl native_fn_02041764
    bl native_fn_0204176c
    bl native_fn_021eb8e4
    cmp r0, #0
    beq L_021e678c
    bl native_fn_021e94e4
    cmp r0, #0
    beq L_021e678c
    bl native_fn_0205eae4
    cmp r0, #0
    movne r0, #1
    bne L_021e6790
L_021e678c:
    mov r0, #0
L_021e6790:
    ldr r1, [pc, #0x124]
    ldr r2, [r1, #0x40]
    cmp r2, #3
    addls pc, pc, r2, lsl #2
    b L_021e6864
    dcd 0xea000011
    dcd 0xea00001f
    dcd 0xea000000
    dcd 0xea000026
    ldr r1, [r1, #0xc]
    mov r0, #12
    mul r2, r1, r0
    ldr r0, [pc, #0xf8]
    ldr r0, [r0, r2]
    blx r0
    ldr r1, [pc, #0xe8]
    mov r2, #0
    str r2, [r1, #0x40]
    ldr r2, [r1, #0xc]
    mov r4, r0
    str r2, [r1, #0x8]
    ldr r0, [r1, #0x24]
    str r0, [r1, #0xc]
    b L_021e6864
    ldr r2, [r1, #0xc]
    mov r0, #12
    mul r3, r2, r0
    ldr r2, [pc, #0xc0]
    ldr r0, [r1, #0x8]
    ldr r1, [r2, r3]
    blx r1
    ldr r0, [pc, #0xa8]
    mov r1, #3
    str r1, [r0, #0x40]
    mov r1, #1
    str r1, [r0, #0x30]
    mov r1, #0
    str r1, [r0, #0x44]
    b L_021e6864
    ldr r2, [r1, #0xc]
    mov r1, #12
    mul r3, r2, r1
    ldr r1, [pc, #0x88]
    ldr r1, [r1, r3]
    blx r1
    ldr r1, [pc, #0x70]
    str r0, [r1, #0x44]
    b L_021e6864
    bl native_fn_02041814
    cmp r0, #1
    ldrne r0, [pc, #0x5c]
    ldrne r1, [r0, #0x30]
    strne r1, [r0, #0x40]
L_021e6864:
    bl native_fn_020851a8
    bl native_fn_020851d4
    bl native_fn_02085200
    cmp r4, #4
    bne L_021e68a8
    bl native_fn_020ba574
    mov r5, r0
    bl native_fn_0204bb18
    cmp r0, #0
    bne L_021e6894
    bl native_fn_021e9e04
    b L_021e6898
L_021e6894:
    bl native_fn_021e9e78
L_021e6898:
    cmp r5, #0
    movlt r5, #0
    mov r0, r5
    bl native_fn_0204bb28
L_021e68a8:
    ldr r1, [pc, #0x1c]
    mov r2, #1
    mov r0, r4
    str r2, [r1, #0xc84]
    ldmia sp!, {r3, r4, r5, pc}
    dcd 0x02218d90
    dcd native_data_02207eb8
    dcd native_data_02207eb0
    dcd native_data_02207eb4
    dcd 0x02101ae8
}
