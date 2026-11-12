/* ov000 row 0x0220c3e8: 268 bytes.
 *
 * What it does: 67 instructions and 14 call(s), then a 12-entry dispatch through an inline branch table at 0x0220c430 (dispatch word at 0x0220c428)
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

extern void native_fn_0220aac4(void);
extern void native_fn_02209c68(void);
extern void native_fn_020c56b4(void);
extern void native_fn_0220ac48(void);
extern void native_fn_0220ad70(void);
extern void native_fn_0220adb4(void);
extern void native_fn_0220ae40(void);
extern void native_fn_0220b308(void);
extern void native_fn_0220ba28(void);
extern void native_fn_0220bc70(void);
extern void native_fn_0220bf50(void);
extern void native_fn_0220c33c(void);


asm u32 native_ov000_0220c3e8 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r1, #0
    mov r4, r0
    bl native_fn_0220aac4
    cmp r0, #0
    beq L_0220c414
    mov r0, r4
    mov r1, #4
    bl native_fn_02209c68
    mov r0, #1
    ldmia sp!, {r4, pc}
L_0220c414:
    add r0, r4, #512
    ldrsh r0, [r0, #118]
    bl native_fn_020c56b4
    ldrb r0, [r0, #0x7]
    cmp r0, #11
    addls pc, pc, r0, lsl #2
    b L_0220c4e0
    dcd 0xea00000a
    dcd 0xea00000d
    dcd 0xea000010
    dcd 0xea000012
    dcd 0xea000026
    dcd 0xea000019
    dcd 0xea00000f
    dcd 0xea000011
    dcd 0xea000019
    dcd 0xea000012
    dcd 0xea00001a
    dcd 0xea00001c
    mov r0, r4
    mov r1, #0
    bl native_fn_0220ac48
    b L_0220c4ec
    mov r0, r4
    mov r1, #1
    bl native_fn_0220ac48
    b L_0220c4ec
    mov r0, r4
    bl native_fn_0220ad70
    b L_0220c4ec
    mov r0, r4
    bl native_fn_0220adb4
    b L_0220c4ec
    mov r0, r4
    bl native_fn_0220ae40
    b L_0220c4ec
    mov r0, r4
    bl native_fn_0220b308
    b L_0220c4ec
    mov r0, r4
    bl native_fn_0220ba28
    b L_0220c4ec
    mov r0, r4
    bl native_fn_0220bc70
    b L_0220c4ec
    mov r0, r4
    bl native_fn_0220bf50
    b L_0220c4ec
    mov r0, r4
    bl native_fn_0220c33c
    b L_0220c4ec
L_0220c4e0:
    mov r0, r4
    mov r1, #0
    bl native_fn_0220ac48
L_0220c4ec:
    mov r0, #0
    ldmia sp!, {r4, pc}
}
