/* ov006 row 0x021dcd88: 612 bytes.
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

extern void native_fn_020642dc(void);
extern void native_fn_021dcd40(void);
extern void native_fn_021ded5c(void);
extern void native_fn_021dcd30(void);
extern void native_fn_020629e0(void);
extern void native_fn_021ded04(void);
extern void native_fn_021d77e8(void);
extern void native_fn_02067b64(void);
extern void native_fn_020642f8(void);
extern void native_fn_02064304(void);
extern void native_fn_0205dc70(void);
extern void native_fn_02048034(void);
extern void native_fn_02048094(void);
extern void native_fn_020630e4(void);
extern void native_fn_021def28(void);
extern void native_fn_020642cc(void);
extern u8 native_data_02207930[];
extern u8 native_data_0220cfe9[];
extern u8 native_data_0220cfe8[];


asm u32 native_ov006_021dcd88 (register u32 a0)
{
    stmdb sp!, {r3, r4, lr}
    sub sp, sp, #12
    ldr r0, [pc, #0x244]
    mov r1, #0
    str r1, [r0, #0x4]
    bl native_fn_020642dc
    cmp r0, #32
    bgt L_021dcdb0
    beq L_021dce04
    b L_021dce50
L_021dcdb0:
    sub r0, r0, #44
    cmp r0, #8
    addls pc, pc, r0, lsl #2
    b L_021dce50
    dcd 0xea000007
    dcd 0xea000021
    dcd 0xea000020
    dcd 0xea00001f
    dcd 0xea00001a
    dcd 0xea000019
    dcd 0xea000018
    dcd 0xea00001b
    dcd 0xea000016
    bl native_fn_021dcd40
    mov r0, #15
    mov r1, #4
    mov r2, #91
    bl native_fn_021ded5c
    mov r0, #8
    bl native_fn_021dcd30
    b L_021dcfcc
L_021dce04:
    bl native_fn_020629e0
    cmp r0, #100
    bne L_021dce34
    mov r0, #15
    mov r2, r0
    mov r1, #4
    bl native_fn_021ded04
    mov r0, #9
    bl native_fn_021dcd30
    mov r0, #2
    bl native_fn_021d77e8
    b L_021dcfcc
L_021dce34:
    mov r0, #7
    bl native_fn_021dcd30
    b L_021dcfcc
    bl native_fn_02067b64
    mov r4, r0
    bl native_fn_020642dc
    str r0, [r4]
L_021dce50:
    bl native_fn_020642f8
    ldrh r0, [r0]
    cmp r0, #0
    bne L_021dceac
    bl native_fn_020642f8
    ldr r1, [pc, #0x174]
    ldrb r4, [r0, #0x4]
    ldrh r0, [r1, #6]
    ldrh r2, [r1, #4]
    ldrh r3, [r1, #8]
    strh r0, [sp, #2]
    strh r2, [sp]
    ldrh r2, [r1, #10]
    add r0, sp, #0
    strh r3, [sp, #4]
    strh r2, [sp, #6]
    ldrh r2, [r1, #12]
    ldrh r1, [r1, #14]
    strh r2, [sp, #8]
    strh r1, [sp, #10]
    bl native_fn_02064304
    bl native_fn_020642f8
    strb r4, [r0, #0x4]
L_021dceac:
    bl native_fn_020642f8
    ldrh r0, [r0]
    cmp r0, #1
    bne L_021dcf64
    bl native_fn_020642f8
    ldrh r2, [r0, #2]
    mov r0, #4
    mov r1, #0
    bl native_fn_0205dc70
    mov r1, #0
    bl native_fn_02048034
    bl native_fn_020642f8
    ldrb r0, [r0, #0x5]
    mov r1, #32
    bl native_fn_02048094
    bl native_fn_020642f8
    ldrb r0, [r0, #0x5]
    cmp r0, #1
    bls L_021dcf18
    bl native_fn_020642f8
    ldrb r2, [r0, #0x4]
    ldr r1, [pc, #0xdc]
    mov r0, #15
    ldrb r2, [r1, r2, lsl #1]
    mov r1, #4
    bl native_fn_021ded5c
    b L_021dcf34
L_021dcf18:
    bl native_fn_020642f8
    ldrb r2, [r0, #0x4]
    ldr r1, [pc, #0xc0]
    mov r0, #15
    ldrb r2, [r1, r2, lsl #1]
    mov r1, #4
    bl native_fn_021ded5c
L_021dcf34:
    bl native_fn_020642f8
    mov r4, r0
    bl native_fn_020642f8
    mov r1, r0
    ldrh r0, [r4, #2]
    ldrb r1, [r1, #0x5]
    bl native_fn_020630e4
    mov r0, #0
    bl native_fn_021dcd30
    mov r0, #1
    bl native_fn_021def28
    b L_021dcfcc
L_021dcf64:
    bl native_fn_021dcd40
    bl native_fn_020642f8
    ldrb r0, [r0, #0x4]
    cmp r0, #7
    bne L_021dcfa0
    bl native_fn_020642f8
    ldrb r2, [r0, #0x4]
    ldr r1, [pc, #0x60]
    mov r0, #15
    ldrb r2, [r1, r2, lsl #1]
    mov r1, #4
    bl native_fn_021ded04
    mov r0, #2
    bl native_fn_021dcd30
    b L_021dcfcc
L_021dcfa0:
    bl native_fn_020642f8
    ldrb r2, [r0, #0x4]
    ldr r1, [pc, #0x38]
    mov r0, #15
    ldrb r2, [r1, r2, lsl #1]
    mov r1, #4
    bl native_fn_021ded5c
    mov r0, #3
    bl native_fn_021dcd30
    mov r0, #1
    bl native_fn_021def28
L_021dcfcc:
    mov r0, #0
    bl native_fn_020642cc
    add sp, sp, #12
    ldmia sp!, {r3, r4, pc}
    dcd 0x0220f4e0
    dcd native_data_02207930
    dcd native_data_0220cfe9
    dcd native_data_0220cfe8
}
