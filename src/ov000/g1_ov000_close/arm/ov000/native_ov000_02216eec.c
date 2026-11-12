/* ov000 row 0x02216eec: 216 bytes.
 *
 * What it does: 50 instructions and 5 call(s), then a 15-entry dispatch through an inline branch table at 0x02216f08 (dispatch word at 0x02216f00)
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

extern void native_fn_0221575c(void);
extern void native_fn_02215790(void);
extern void native_fn_021e7b9c(void);
extern void native_fn_0205f9e4(void);


asm u32 native_ov000_02216eec (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldr r0, [pc, #0xbc]
    mov r4, #0
    ldrsb r0, [r0, #16]
    cmp r0, #14
    addls pc, pc, r0, lsl #2
    b L_02216f50
    dcd 0xea00000d
    dcd 0xea00000c
    dcd 0xea00000b
    dcd 0xea00000a
    dcd 0xea000009
    dcd 0xea000008
    dcd 0xea000007
    dcd 0xea000009
    dcd 0xea000005
    dcd 0xea000004
    dcd 0xea000003
    dcd 0xea000005
    dcd 0xea000004
    dcd 0xea000003
    dcd 0xea000002
    mov r0, r4
    bl native_fn_0221575c
    mov r4, #1
L_02216f50:
    bl native_fn_02215790
    cmp r0, #0
    beq L_02216f80
    ldr r0, [pc, #0x54]
    ldr r0, [r0, #0x10]
    cmp r0, #0
    beq L_02216f78
    mov r0, #82
    bl native_fn_021e7b9c
    b L_02216f80
L_02216f78:
    mov r0, #83
    bl native_fn_021e7b9c
L_02216f80:
    ldr r0, [pc, #0x34]
    ldr r0, [r0, #0x2c]
    cmp r0, #0
    beq L_02216f98
    ldr r0, [pc, #0x28]
    bl native_fn_0205f9e4
L_02216f98:
    ldr r1, [pc, #0x18]
    ldr r0, [pc, #0x18]
    str r4, [r1, #0xc]
    mov r1, #10
    strb r1, [r0, #0x494]
    mov r0, #1
    ldmia sp!, {r4, pc}
    dcd 0x0224536c
    dcd 0x0224532c
    dcd 0x022459b4
    dcd 0x022459c4
}
