/* ov006 row 0x021ea3d4: 652 bytes.
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

extern void native_fn_021e75ec(void);
extern void native_fn_021e7b64(void);
extern void native_fn_0205dc88(void);
extern void native_fn_021e76f0(void);
extern void native_fn_021e767c(void);
extern void native_fn_021e796c(void);
extern void native_fn_0220769c(void);
extern void native_fn_021e791c(void);
extern void native_fn_021e92bc(void);
extern void native_fn_021ea314(void);
extern void native_fn_021ea35c(void);
extern u8 native_data_0220854c[];


asm u32 native_ov006_021ea3d4 (register u32 a0)
{
    stmdb sp!, {lr}
    sub sp, sp, #12
    ldr r0, [pc, #0x270]
    ldr r1, [r0]
    cmp r1, #13
    addls pc, pc, r1, lsl #2
    b L_021ea648
    dcd 0xea000094
    dcd 0xea000093
    dcd 0xea00000a
    dcd 0xea000013
    dcd 0xea000024
    dcd 0xea00002d
    dcd 0xea000047
    dcd 0xea000050
    dcd 0xea00005c
    dcd 0xea000063
    dcd 0xea00006a
    dcd 0xea000071
    dcd 0xea000078
    dcd 0xea00007f
    mov r0, #38
    bl native_fn_021e75ec
    mov r0, #38
    bl native_fn_021e7b64
    ldr r0, [pc, #0x214]
    mov r1, #3
    str r1, [r0]
    add sp, sp, #12
    mov r0, #0
    ldmia sp!, {pc}
    ldr r0, [pc, #0x200]
    bl native_fn_0205dc88
    cmp r0, #0
    mov r0, #38
    beq L_021ea470
    ldr r1, [pc, #0x1ec]
    bl native_fn_021e76f0
    b L_021ea478
L_021ea470:
    ldr r1, [pc, #0x1e4]
    bl native_fn_021e767c
L_021ea478:
    mov r0, #38
    bl native_fn_021e7b64
    ldr r0, [pc, #0x1cc]
    mov r1, #1
    str r1, [r0]
    add sp, sp, #12
    mov r0, #0
    ldmia sp!, {pc}
    mov r0, #40
    bl native_fn_021e75ec
    mov r0, #40
    bl native_fn_021e7b64
    ldr r0, [pc, #0x1a4]
    mov r1, #5
    str r1, [r0]
    add sp, sp, #12
    mov r0, #0
    ldmia sp!, {pc}
    mov r0, #40
    bl native_fn_021e7b64
    ldr r0, [pc, #0x184]
    mov r2, #0
    ldr r1, [r0, #0x4c]
    mov r3, r2
    mov r0, #40
    bl native_fn_021e796c
    ldr r0, [pc, #0x16c]
    ldr r0, [r0, #0x4c]
    bl native_fn_0220769c
    mov r2, #15
    mov r1, r0
    str r2, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    mov r3, #0
    mov r0, #40
    mov r2, #3
    str r3, [sp, #0x8]
    bl native_fn_021e791c
    ldr r0, [pc, #0x138]
    mov r1, #1
    str r1, [r0]
    add sp, sp, #12
    mov r0, #0
    ldmia sp!, {pc}
    mov r0, #39
    bl native_fn_021e75ec
    mov r0, #39
    bl native_fn_021e7b64
    ldr r0, [pc, #0x110]
    mov r1, #7
    str r1, [r0]
    add sp, sp, #12
    mov r0, #0
    ldmia sp!, {pc}
    ldr r0, [r0, #0x50]
    bl native_fn_021e92bc
    mov r1, r0
    mov r0, #39
    bl native_fn_021e767c
    mov r0, #39
    bl native_fn_021e7b64
    ldr r0, [pc, #0xdc]
    mov r1, #1
    str r1, [r0]
    add sp, sp, #12
    mov r0, #0
    ldmia sp!, {pc}
    mov r0, #0
    bl native_fn_021ea314
    ldr r0, [pc, #0xbc]
    mov r1, #9
    str r1, [r0]
    add sp, sp, #12
    mov r0, #0
    ldmia sp!, {pc}
    mov r0, #0
    bl native_fn_021ea35c
    ldr r0, [pc, #0x9c]
    mov r1, #1
    str r1, [r0]
    add sp, sp, #12
    mov r0, #0
    ldmia sp!, {pc}
    mov r0, #1
    bl native_fn_021ea314
    ldr r0, [pc, #0x7c]
    mov r1, #11
    str r1, [r0]
    add sp, sp, #12
    mov r0, #0
    ldmia sp!, {pc}
    mov r0, #1
    bl native_fn_021ea35c
    ldr r0, [pc, #0x5c]
    mov r1, #1
    str r1, [r0]
    add sp, sp, #12
    mov r0, #0
    ldmia sp!, {pc}
    mov r0, #2
    bl native_fn_021ea314
    ldr r0, [pc, #0x3c]
    mov r1, #13
    str r1, [r0]
    add sp, sp, #12
    mov r0, #0
    ldmia sp!, {pc}
    mov r0, #2
    bl native_fn_021ea35c
    ldr r0, [pc, #0x1c]
    mov r1, #1
    str r1, [r0]
    add sp, sp, #12
    mov r0, #0
    ldmia sp!, {pc}
L_021ea648:
    mov r0, #1
    add sp, sp, #12
    ldmia sp!, {pc}
    dcd 0x02219290
    dcd 0x022192f4
    dcd native_data_0220854c
}
