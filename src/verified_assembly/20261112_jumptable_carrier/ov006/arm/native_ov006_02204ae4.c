/* ov006 row 0x02204ae4: 212 bytes.
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

extern void native_fn_021e8fc0(void);
extern void native_fn_021e8000(void);
extern void native_fn_021eac80(void);
extern void native_fn_021eb9a4(void);
extern u8 native_data_0220bb74[];


asm u32 native_ov006_02204ae4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    ldr r1, [pc, #0xbc]
    mov r2, r5
    mov r0, #7
    bl native_fn_021e8fc0
    movs r4, r0
    bne L_02204ba8
    cmp r5, #0
    beq L_02204ba8
    bl native_fn_021e8000
    mov r5, r0
    mvn r0, #0
    cmp r5, r0
    ldrne r0, [pc, #0x90]
    ldrne r0, [r0]
    cmpne r0, r5
    beq L_02204ba8
    cmp r5, #5
    addls pc, pc, r5, lsl #2
    b L_02204b8c
    dcd 0xea000013
    dcd 0xea000003
    dcd 0xea000002
    dcd 0xea000001
    dcd 0xea000000
    dcd 0xeaffffff
    sub r0, r5, #1
    bl native_fn_021eac80
    cmp r0, #0
    bne L_02204b80
    mov r1, #0
    mov r2, r1
    mov r0, #11
    bl native_fn_021eb9a4
    cmp r0, #0
    ldrne r0, [pc, #0x38]
    strne r5, [r0]
    b L_02204ba8
L_02204b80:
    ldr r0, [pc, #0x2c]
    str r5, [r0]
    b L_02204ba8
L_02204b8c:
    mov r1, #0
    mov r2, r1
    mov r0, #10
    bl native_fn_021eb9a4
    cmp r0, #0
    ldrne r0, [pc, #0xc]
    strne r5, [r0]
L_02204ba8:
    mov r0, r4
    ldmia sp!, {r3, r4, r5, pc}
    dcd native_data_0220bb74
    dcd 0x0221c1ec
}
