/* ov006 row 0x021ddfa8: 476 bytes.
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

extern void native_fn_02041814(void);
extern void native_fn_021ddc10(void);
extern void native_fn_0202a1e0(void);
extern void native_fn_0207e97c(void);
extern void native_fn_02008d78(void);
extern void native_fn_02067748(void);
extern void native_fn_02062a10(void);
extern void native_fn_0207e720(void);
extern void native_fn_02041538(void);
extern void native_fn_0207e874(void);
extern void native_fn_0207f390(void);
extern void native_fn_0207f3b0(void);
extern void native_fn_02008e0c(void);
extern void native_fn_0207e948(void);


asm u32 native_ov006_021ddfa8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    sub sp, sp, #16
    ldr r0, [pc, #0x1c8]
    mov r4, #1
    ldr r1, [r0, #0xc]
    cmp r1, #4
    addls pc, pc, r1, lsl #2
    b L_021de174
    dcd 0xea000003
    dcd 0xea000005
    dcd 0xea000033
    dcd 0xea000057
    dcd 0xea00005e
    bl native_fn_02041814
    cmp r0, #1
    beq L_021de174
    bl native_fn_021ddc10
    mov r0, #1
    bl native_fn_0202a1e0
    bl native_fn_0207e97c
    add r0, sp, #0
    mov r1, #0
    mov r2, #16
    bl native_fn_02008d78
    ldr r0, [pc, #0x170]
    ldr r1, [r0, #0x8]
    cmp r1, #0
    beq L_021de024
    cmp r1, #1
    beq L_021de04c
    b L_021de07c
L_021de024:
    bl native_fn_02067748
    add r3, r0, #16
    mov r2, #20
    mov r1, #2
    mov r0, #1
    str r3, [sp, #0x8]
    strb r2, [sp, #0xc]
    strb r1, [sp]
    strb r0, [sp, #0xd]
    b L_021de07c
L_021de04c:
    mov r1, #1
    strb r1, [sp]
    ldr r0, [r0, #0x10]
    bl native_fn_02062a10
    ldrsh r2, [r0, #24]
    mov r1, #16
    strh r2, [sp, #2]
    ldrb r2, [r0, #0x1a]
    strb r2, [sp, #0x4]
    ldrb r0, [r0, #0x1b]
    strb r0, [sp, #0x5]
    strb r1, [sp, #0xc]
L_021de07c:
    add r0, sp, #0
    bl native_fn_0207e720
    mov r0, #0
    mov r1, #2
    mov r2, #10
    bl native_fn_02041538
    ldr r0, [pc, #0xe4]
    mov r1, #2
    str r1, [r0, #0xc]
    b L_021de174
    bl native_fn_0207e874
    cmp r0, #0
    beq L_021de174
    bl native_fn_0207f390
    cmp r0, #0
    beq L_021de118
    ldr r0, [pc, #0xbc]
    ldr r1, [r0, #0x8]
    cmp r1, #0
    beq L_021de0d8
    cmp r1, #1
    beq L_021de0fc
    b L_021de118
L_021de0d8:
    bl native_fn_0207f3b0
    mov r5, r0
    bl native_fn_02067748
    mov r1, r0
    mov r0, r5
    add r1, r1, #16
    mov r2, #24
    bl native_fn_02008e0c
    b L_021de118
L_021de0fc:
    ldr r0, [r0, #0x10]
    bl native_fn_02062a10
    mov r5, r0
    bl native_fn_0207f3b0
    mov r1, r5
    mov r2, #20
    bl native_fn_02008e0c
L_021de118:
    mov r0, #1
    mov r1, #2
    mov r2, #10
    bl native_fn_02041538
    ldr r0, [pc, #0x50]
    mov r1, #3
    str r1, [r0, #0xc]
    b L_021de174
    bl native_fn_02041814
    cmp r0, #1
    beq L_021de174
    bl native_fn_0207e948
    ldr r0, [pc, #0x30]
    mov r1, #4
    str r1, [r0, #0xc]
    b L_021de174
    ldr r0, [r0, #0x8]
    cmp r0, #0
    beq L_021de170
    cmp r0, #1
    moveq r4, #4
    b L_021de174
L_021de170:
    mov r4, #0
L_021de174:
    mov r0, r4
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, pc}
    dcd 0x0220f4e8
}
