/* ov006 row 0x021d8414: 420 bytes.
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

extern void native_fn_02008be0(void);
extern void native_fn_020211c0(void);
extern u8 native_data_0220cb48[];
extern u8 native_data_0220cb50[];
extern u8 native_data_0220cb58[];
extern u8 native_data_0220cb60[];
extern u8 native_data_0220cb68[];
extern u8 native_data_0220cb70[];
extern u8 native_data_0220cb78[];
extern u8 native_data_0220cb80[];


asm u32 native_ov006_021d8414 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    movs r7, r0
    mov r4, r3
    mov r5, r2
    movmi r7, #0
    mov r6, r1
    mov r3, #1
    cmp r4, #0
    mov r2, #0
    ble L_021d845c
    mov r1, #10
L_021d8440:
    mul r0, r3, r1
    add r2, r2, #1
    mov r2, r2, lsl #24
    mov r3, r0
    cmp r4, r2, asr #24
    mov r2, r2, asr #24
    bgt L_021d8440
L_021d845c:
    mov r1, r6
    cmp r7, r3
    mov r2, r5
    mov r0, #0
    subge r7, r3, #1
    bl native_fn_02008be0
    cmp r4, #7
    addls pc, pc, r4, lsl #2
    b L_021d8548
    dcd 0xea000030
    dcd 0xea000005
    dcd 0xea00000a
    dcd 0xea00000f
    dcd 0xea000014
    dcd 0xea000019
    dcd 0xea00001e
    dcd 0xea000023
    ldr r2, [pc, #0xf0]
    mov r0, r6
    mov r1, r5
    mov r3, r7
    bl native_fn_020211c0
    b L_021d855c
    ldr r2, [pc, #0xdc]
    mov r0, r6
    mov r1, r5
    mov r3, r7
    bl native_fn_020211c0
    b L_021d855c
    ldr r2, [pc, #0xc8]
    mov r0, r6
    mov r1, r5
    mov r3, r7
    bl native_fn_020211c0
    b L_021d855c
    ldr r2, [pc, #0xb4]
    mov r0, r6
    mov r1, r5
    mov r3, r7
    bl native_fn_020211c0
    b L_021d855c
    ldr r2, [pc, #0xa0]
    mov r0, r6
    mov r1, r5
    mov r3, r7
    bl native_fn_020211c0
    b L_021d855c
    ldr r2, [pc, #0x8c]
    mov r0, r6
    mov r1, r5
    mov r3, r7
    bl native_fn_020211c0
    b L_021d855c
    ldr r2, [pc, #0x78]
    mov r0, r6
    mov r1, r5
    mov r3, r7
    bl native_fn_020211c0
    b L_021d855c
L_021d8548:
    ldr r2, [pc, #0x64]
    mov r0, r6
    mov r1, r5
    mov r3, r7
    bl native_fn_020211c0
L_021d855c:
    cmp r4, #0
    mov r3, #0
    ble L_021d8590
    mov r1, #12288
L_021d856c:
    mov r2, r3, lsl #1
    ldrh r0, [r6, r2]
    cmp r0, #32
    add r0, r3, #1
    mov r0, r0, lsl #24
    streqh r1, [r6, r2]
    cmp r4, r0, asr #24
    mov r3, r0, asr #24
    bgt L_021d856c
L_021d8590:
    mov r0, r6
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
    dcd native_data_0220cb48
    dcd native_data_0220cb50
    dcd native_data_0220cb58
    dcd native_data_0220cb60
    dcd native_data_0220cb68
    dcd native_data_0220cb70
    dcd native_data_0220cb78
    dcd native_data_0220cb80
}
