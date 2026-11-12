/* ov000 row 0x0220cb08: 216 bytes.
 *
 * What it does: 54 instructions and 8 call(s), then a 11-entry dispatch through an inline branch table at 0x0220cb40 (dispatch word at 0x0220cb38)
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

extern void native_fn_02042bfc(void);
extern void native_fn_020c56b4(void);
extern void native_fn_0220c5cc(void);
extern void native_fn_0220c9d0(void);
extern void native_fn_0220cad8(void);
extern void native_fn_02209c68(void);


asm u32 native_ov000_0220cb08 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    ldrb r1, [r5, #0x279]
    cmp r1, #0
    bne L_0220cb24
    mov r1, #4096
    bl native_fn_02042bfc
L_0220cb24:
    add r0, r5, #512
    ldrsh r0, [r0, #118]
    bl native_fn_020c56b4
    ldrb r0, [r0, #0x7]
    cmp r0, #10
    addls pc, pc, r0, lsl #2
    b L_0220cb9c
    dcd 0xea000009
    dcd 0xea000008
    dcd 0xea000007
    dcd 0xea00000e
    dcd 0xea000011
    dcd 0xea000010
    dcd 0xea000007
    dcd 0xea00000e
    dcd 0xea00000d
    dcd 0xea00000c
    dcd 0xea00000b
    mov r0, r5
    bl native_fn_0220c5cc
    mov r4, r0
    b L_0220cba8
    mov r0, r5
    bl native_fn_0220c9d0
    mov r4, r0
    b L_0220cba8
    mov r0, r5
    bl native_fn_0220cad8
    mov r4, r0
    b L_0220cba8
L_0220cb9c:
    mov r0, r5
    bl native_fn_0220c5cc
    mov r4, r0
L_0220cba8:
    cmp r4, #1
    bne L_0220cbc0
    mov r0, r5
    mov r1, #5
    bl native_fn_02209c68
    b L_0220cbd8
L_0220cbc0:
    mvn r0, #0
    cmp r4, r0
    bne L_0220cbd8
    mov r0, r5
    mov r1, #3
    bl native_fn_02209c68
L_0220cbd8:
    mov r0, r4
    ldmia sp!, {r3, r4, r5, pc}
}
