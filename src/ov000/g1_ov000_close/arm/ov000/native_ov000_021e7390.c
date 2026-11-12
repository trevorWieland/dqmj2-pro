/* ov000 row 0x021e7390: 344 bytes.
 *
 * What it does: 79 instructions and 13 call(s), then a 8-entry dispatch through an inline branch table at 0x021e73dc (dispatch word at 0x021e73d4)
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

extern void native_fn_02040424(void);
extern void native_fn_021df3bc(void);
extern void native_fn_0205bf9c(void);
extern void native_fn_0205bfd4(void);
extern void native_fn_0205ccb8(void);


asm u32 native_ov000_021e7390 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    bl native_fn_02040424
    ldr r1, [pc, #0x12c]
    mvn r2, #0
    str r2, [r1, #0x4]
    mov r4, r0
    bl native_fn_021df3bc
    ldrb r0, [r0, #0xb]
    tst r0, #2
    beq L_021e74c0
    mov r0, r4
    bl native_fn_021df3bc
    mov r4, r0
    bl native_fn_0205bf9c
    add r0, r4, r0
    ldrsb r0, [r0, #12]
    cmp r0, #7
    addls pc, pc, r0, lsl #2
    b L_021e74c0
    dcd 0xea000037
    dcd 0xea000005
    dcd 0xea000012
    dcd 0xea000017
    dcd 0xea00001c
    dcd 0xea000021
    dcd 0xea000026
    dcd 0xea00002b
    bl native_fn_0205bfd4
    cmp r0, #0
    mov r1, #1024
    bne L_021e7420
    mov r0, #900
    bl native_fn_0205ccb8
    ldr r1, [pc, #0xb0]
    str r0, [r1, #0x4]
    b L_021e74c0
L_021e7420:
    ldr r0, [pc, #0xa8]
    bl native_fn_0205ccb8
    ldr r1, [pc, #0x9c]
    str r0, [r1, #0x4]
    b L_021e74c0
    ldr r0, [pc, #0x98]
    mov r1, #1024
    bl native_fn_0205ccb8
    ldr r1, [pc, #0x84]
    str r0, [r1, #0x4]
    b L_021e74c0
    ldr r0, [pc, #0x84]
    mov r1, #1024
    bl native_fn_0205ccb8
    ldr r1, [pc, #0x6c]
    str r0, [r1, #0x4]
    b L_021e74c0
    mov r0, #904
    mov r1, #1024
    bl native_fn_0205ccb8
    ldr r1, [pc, #0x54]
    str r0, [r1, #0x4]
    b L_021e74c0
    ldr r0, [pc, #0x58]
    mov r1, #1024
    bl native_fn_0205ccb8
    ldr r1, [pc, #0x3c]
    str r0, [r1, #0x4]
    b L_021e74c0
    ldr r0, [pc, #0x44]
    mov r1, #1024
    bl native_fn_0205ccb8
    ldr r1, [pc, #0x24]
    str r0, [r1, #0x4]
    b L_021e74c0
    ldr r0, [pc, #0x30]
    mov r1, #1024
    bl native_fn_0205ccb8
    ldr r1, [pc, #0xc]
    str r0, [r1, #0x4]
L_021e74c0:
    ldr r0, [pc, #0x4]
    ldr r0, [r0, #0x4]
    ldmia sp!, {r4, pc}
    dcd 0x022351d4
    dcd 0x00000387
    dcd 0x00000386
    dcd 0x00000385
    dcd 0x00000389
    dcd 0x0000038a
    dcd 0x0000038b
}
