/* ov000 row 0x0220ea98: 192 bytes.
 *
 * What it does: 48 instructions and 11 call(s), then a 9-entry dispatch through an inline branch table at 0x0220eabc (dispatch word at 0x0220eab4)
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

extern void native_fn_020c56b4(void);
extern void native_fn_0220d7b8(void);
extern void native_fn_0220d8b8(void);
extern void native_fn_0220d8c4(void);
extern void native_fn_0220d9f4(void);
extern void native_fn_0220daf8(void);
extern void native_fn_0220e3d0(void);
extern void native_fn_0220e20c(void);
extern void native_fn_0220e4d8(void);
extern void native_fn_0220e8c0(void);


asm u32 native_ov000_0220ea98 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r4, r0
    add r0, r4, #512
    ldrsh r0, [r0, #118]
    bl native_fn_020c56b4
    ldrb r0, [r0, #0x8]
    cmp r0, #8
    addls pc, pc, r0, lsl #2
    b L_0220eb4c
    dcd 0xea000007
    dcd 0xea000009
    dcd 0xea00000b
    dcd 0xea00000d
    dcd 0xea00000f
    dcd 0xea000011
    dcd 0xea000013
    dcd 0xea000015
    dcd 0xea000017
    mov r0, r4
    bl native_fn_0220d7b8
    ldmia sp!, {r4, pc}
    mov r0, r4
    bl native_fn_0220d8b8
    ldmia sp!, {r4, pc}
    mov r0, r4
    bl native_fn_0220d8c4
    ldmia sp!, {r4, pc}
    mov r0, r4
    bl native_fn_0220d9f4
    ldmia sp!, {r4, pc}
    mov r0, r4
    bl native_fn_0220daf8
    ldmia sp!, {r4, pc}
    mov r0, r4
    bl native_fn_0220e3d0
    ldmia sp!, {r4, pc}
    mov r0, r4
    bl native_fn_0220e20c
    ldmia sp!, {r4, pc}
    mov r0, r4
    bl native_fn_0220e4d8
    ldmia sp!, {r4, pc}
    mov r0, r4
    bl native_fn_0220e8c0
    ldmia sp!, {r4, pc}
L_0220eb4c:
    mov r0, r4
    bl native_fn_0220d7b8
    ldmia sp!, {r4, pc}
}
