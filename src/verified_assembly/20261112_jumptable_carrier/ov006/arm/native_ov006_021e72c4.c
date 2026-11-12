/* ov006 row 0x021e72c4: 172 bytes.
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

extern void native_fn_020bb338(void);
extern void native_fn_0202a37c(void);
extern void native_fn_02008be0(void);
extern void native_fn_02007308(void);
extern u8 native_data_0220d138[];


asm u32 native_ov006_021e72c4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    cmp r5, #9
    addls pc, pc, r5, lsl #2
    b L_021e7318
    dcd 0xea000008
    dcd 0xea000007
    dcd 0xea000006
    dcd 0xea000005
    dcd 0xea000004
    dcd 0xea000003
    dcd 0xea000002
    dcd 0xea000001
    dcd 0xea000000
    dcd 0xea000005
    ldr r0, [pc, #0x5c]
    mov r1, #1
    ldr r0, [r0, r5, lsl #2]
    bl native_fn_020bb338
    mov r4, r0
    b L_021e735c
L_021e7318:
    ldr r1, [pc, #0x48]
    mov r0, #1
    mov r2, #4
    bl native_fn_0202a37c
    movs r4, r0
    beq L_021e735c
    cmp r5, #9
    ldreq r0, [pc, #0x30]
    add r1, r4, #8
    movne r0, #32768
    mov r0, r0, lsl #16
    mov r0, r0, lsr #16
    mov r2, #98304
    bl native_fn_02008be0
    mov r0, r4
    mov r1, #98304
    bl native_fn_02007308
L_021e735c:
    mov r0, r4
    ldmia sp!, {r3, r4, r5, pc}
    dcd native_data_0220d138
    dcd 0x00018008
    dcd 0x00007fff
}
