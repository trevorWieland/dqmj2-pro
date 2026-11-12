/* ov000 row 0x02216ae8: 480 bytes.
 *
 * What it does: 115 instructions and 21 call(s), then a 15-entry dispatch through an inline branch table at 0x02216b7c (dispatch word at 0x02216b74)
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
extern void native_fn_0206c0b0(void);
extern void native_fn_02049ae4(void);
extern void native_fn_0221572c(void);
extern void native_fn_021f9c5c(void);
extern void native_fn_021ff6bc(void);
extern void native_fn_020735f8(void);
extern void native_fn_021fbf44(void);
extern void native_fn_02078a48(void);
extern void native_fn_022156d4(void);
extern void native_fn_021fea00(void);
extern void native_fn_02201a60(void);
extern void native_fn_0207726c(void);
extern void native_fn_021e7b9c(void);
extern void native_fn_02079170(void);
extern void native_fn_0222217c(void);
extern void native_fn_021fe1e8(void);
extern void native_fn_0205f9e4(void);


asm u32 native_ov000_02216ae8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    bl native_fn_0202a634
    mov r4, r0
    ldrh r1, [r4, #2]
    ldr r0, [pc, #0x1b4]
    mov r5, #0
    mov r7, r5
    tst r1, #3
    ldrsb r6, [r0, #1]
    bne L_02216b60
    bl native_fn_0206c0b0
    cmp r0, #0
    bne L_02216b60
    bl native_fn_0206c0b0
    cmp r0, #0
    bne L_02216b60
    ldrh r0, [r4, #2]
    tst r0, #2048
    beq L_02216b60
    bl native_fn_02049ae4
    ldr r0, [r0, #0x4]
    cmp r0, #0
    bne L_02216b60
    bl native_fn_0221572c
    cmp r0, #0
    beq L_02216b60
    ldr r0, [pc, #0x160]
    mov r1, #5
    strb r1, [r0, #0x494]
    mov r7, #1
L_02216b60:
    cmp r7, #0
    bne L_02216c5c
    ldr r0, [pc, #0x14c]
    ldrsb r0, [r0, #16]
    cmp r0, #14
    addls pc, pc, r0, lsl #2
    b L_02216c5c
    dcd 0xea00000d
    dcd 0xea00000f
    dcd 0xea000011
    dcd 0xea000013
    dcd 0xea000015
    dcd 0xea000019
    dcd 0xea00001e
    dcd 0xea000020
    dcd 0xea000026
    dcd 0xea000018
    dcd 0xea00002a
    dcd 0xea00002b
    dcd 0xea00002a
    dcd 0xea000029
    dcd 0xea000023
    bl native_fn_021f9c5c
    mov r6, r0
    b L_02216c5c
    bl native_fn_021ff6bc
    mov r6, r0
    b L_02216c5c
    bl native_fn_020735f8
    mov r6, r0
    b L_02216c5c
    bl native_fn_021fbf44
    mov r6, r0
    b L_02216c5c
    bl native_fn_02078a48
    cmp r0, #0
    beq L_02216c5c
    bl native_fn_022156d4
    b L_02216c5c
    bl native_fn_021fea00
    mov r6, r0
    b L_02216c5c
    bl native_fn_02201a60
    mov r6, r0
    b L_02216c5c
    bl native_fn_0207726c
    mov r6, r0
    b L_02216c5c
    ldrh r0, [r4, #2]
    tst r0, #2
    beq L_02216c5c
    bl native_fn_022156d4
    mov r0, #83
    bl native_fn_021e7b9c
    b L_02216c5c
    bl native_fn_02079170
    mov r6, r0
    b L_02216c5c
    bl native_fn_0222217c
    mov r6, r0
    b L_02216c5c
    bl native_fn_021fe1e8
    mov r6, r0
L_02216c5c:
    ldr r0, [pc, #0x50]
    ldrsb r0, [r0, #1]
    cmp r0, r6
    beq L_02216c7c
    ldr r0, [pc, #0x44]
    mov r1, #9
    strb r1, [r0, #0x494]
    mov r5, #2
L_02216c7c:
    ldr r0, [pc, #0x34]
    ldr r0, [r0, #0x2c]
    cmp r0, #0
    beq L_02216c94
    ldr r0, [pc, #0x2c]
    bl native_fn_0205f9e4
L_02216c94:
    ldr r0, [pc, #0x1c]
    ldr r0, [r0, #0x74]
    cmp r0, #0
    beq L_02216cac
    ldr r0, [pc, #0x18]
    bl native_fn_0205f9e4
L_02216cac:
    mov r0, r5
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
    dcd 0x0224532c
    dcd 0x022459b4
    dcd 0x0224536c
    dcd 0x022459c4
    dcd 0x02245a0c
}
