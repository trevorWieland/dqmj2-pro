/* ov006 row 0x021eb8e4: 192 bytes.
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

extern void native_fn_02041800(void);
extern u8 native_data_022087dc[];


asm u32 native_ov006_021eb8e4 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r1, [pc, #0xac]
    ldr r3, [pc, #0xac]
    ldr r2, [r1, #0x1c]
    mov r0, #12
    mla r3, r2, r0, r3
    ldr r0, [r1, #0x14]
    cmp r0, #3
    addls pc, pc, r0, lsl #2
    b L_021eb994
    dcd 0xea000002
    dcd 0xea00000b
    dcd 0xea00000d
    dcd 0xea000018
    ldr r0, [r3]
    blx r0
    cmp r0, #0
    beq L_021eb994
    ldr r0, [pc, #0x68]
    mov r1, #3
    str r1, [r0, #0x14]
    mov r1, #1
    str r1, [r0, #0x20]
    b L_021eb994
    ldr r0, [r3, #0x4]
    blx r0
    ldmia sp!, {r3, pc}
    ldr r0, [r3, #0x8]
    blx r0
    cmp r0, #0
    beq L_021eb994
    ldr r0, [pc, #0x34]
    mov r2, #0
    ldr r3, [r0, #0x10]
    mov r1, #3
    str r3, [r0, #0x1c]
    str r2, [r0, #0x14]
    str r1, [r0, #0x20]
    b L_021eb994
    bl native_fn_02041800
    cmp r0, #1
    ldrne r0, [pc, #0xc]
    ldrne r1, [r0, #0x20]
    strne r1, [r0, #0x14]
L_021eb994:
    mov r0, #0
    ldmia sp!, {r3, pc}
    dcd 0x02219290
    dcd native_data_022087dc
}
