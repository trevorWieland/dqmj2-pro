/* ov000 row 0x021e729c: 244 bytes.
 *
 * What it does: 55 instructions and 12 call(s), then a 8-entry dispatch through an inline branch table at 0x021e72c8 (dispatch word at 0x021e72c0)
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
extern void native_fn_021e722c(void);


asm u32 native_ov000_021e729c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, #0
    bl native_fn_02040424
    bl native_fn_021df3bc
    mov r4, r0
    bl native_fn_0205bf9c
    add r0, r4, r0
    ldrsb r0, [r0, #12]
    cmp r0, #7
    addls pc, pc, r0, lsl #2
    b L_021e7370
    dcd 0xea000028
    dcd 0xea000005
    dcd 0xea00000f
    dcd 0xea000012
    dcd 0xea000015
    dcd 0xea000018
    dcd 0xea00001b
    dcd 0xea00001e
    bl native_fn_0205bfd4
    cmp r0, #0
    bne L_021e7304
    mov r0, #900
    bl native_fn_021e722c
    orr r5, r5, r0
    b L_021e7370
L_021e7304:
    ldr r0, [pc, #0x6c]
    bl native_fn_021e722c
    orr r5, r5, r0
    b L_021e7370
    ldr r0, [pc, #0x60]
    bl native_fn_021e722c
    orr r5, r5, r0
    b L_021e7370
    ldr r0, [pc, #0x54]
    bl native_fn_021e722c
    orr r5, r5, r0
    b L_021e7370
    mov r0, #904
    bl native_fn_021e722c
    orr r5, r5, r0
    b L_021e7370
    ldr r0, [pc, #0x38]
    bl native_fn_021e722c
    orr r5, r5, r0
    b L_021e7370
    ldr r0, [pc, #0x2c]
    bl native_fn_021e722c
    orr r5, r5, r0
    b L_021e7370
    ldr r0, [pc, #0x20]
    bl native_fn_021e722c
    orr r5, r5, r0
L_021e7370:
    mov r0, r5
    ldmia sp!, {r3, r4, r5, pc}
    dcd 0x00000387
    dcd 0x00000386
    dcd 0x00000385
    dcd 0x00000389
    dcd 0x0000038a
    dcd 0x0000038b
}
