/* ov000 row 0x0220fde8: 316 bytes.
 *
 * What it does: 79 instructions and 16 call(s), then a 9-entry dispatch through an inline branch table at 0x0220fe2c (dispatch word at 0x0220fe24)
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

extern void native_fn_0204072c(void);
extern void native_fn_0220fcb8(void);
extern void native_fn_0220fd30(void);
extern void native_fn_0220a650(void);
extern void native_fn_0220a6e8(void);
extern void native_fn_0220a788(void);
extern void native_fn_0220c3e8(void);
extern void native_fn_0220cb08(void);
extern void native_fn_0220d72c(void);
extern void native_fn_0220ea98(void);
extern void native_fn_0220eb58(void);
extern void native_fn_0220ed9c(void);
extern void native_fn_0220fc60(void);
extern void native_fn_0220c4f4(void);
extern void native_fn_0220c560(void);
extern void native_fn_0220fbb4(void);


asm u32 native_ov000_0220fde8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    mov r4, #1
    bl native_fn_0204072c
    cmp r0, #0
    mov r0, r5
    beq L_0220fe0c
    bl native_fn_0220fcb8
    b L_0220fe10
L_0220fe0c:
    bl native_fn_0220fd30
L_0220fe10:
    ldrb r0, [r5, #0x1e2]
    cmp r0, #0
    ldrb r0, [r5, #0x278]
    beq L_0220fec4
    cmp r0, #8
    addls pc, pc, r0, lsl #2
    b L_0220febc
    dcd 0xea000007
    dcd 0xea000009
    dcd 0xea00000b
    dcd 0xea00000d
    dcd 0xea00000f
    dcd 0xea000011
    dcd 0xea000013
    dcd 0xea000015
    dcd 0xea000017
    mov r0, r5
    bl native_fn_0220a650
    b L_0220ff08
    mov r0, r5
    bl native_fn_0220a6e8
    b L_0220ff08
    mov r0, r5
    bl native_fn_0220a788
    b L_0220ff08
    mov r0, r5
    bl native_fn_0220c3e8
    b L_0220ff08
    mov r0, r5
    bl native_fn_0220cb08
    b L_0220ff08
    mov r0, r5
    bl native_fn_0220d72c
    b L_0220ff08
    mov r0, r5
    bl native_fn_0220ea98
    b L_0220ff08
    mov r0, r5
    bl native_fn_0220eb58
    b L_0220ff08
    mov r0, r5
    bl native_fn_0220ed9c
    b L_0220ff08
L_0220febc:
    mov r4, #0
    b L_0220ff08
L_0220fec4:
    cmp r0, #6
    beq L_0220fee0
    cmp r0, #10
    beq L_0220feec
    cmp r0, #11
    beq L_0220fef8
    b L_0220ff04
L_0220fee0:
    mov r0, r5
    bl native_fn_0220fc60
    b L_0220ff08
L_0220feec:
    mov r0, r5
    bl native_fn_0220c4f4
    b L_0220ff08
L_0220fef8:
    mov r0, r5
    bl native_fn_0220c560
    b L_0220ff08
L_0220ff04:
    mov r4, #0
L_0220ff08:
    ldrb r0, [r5, #0x278]
    cmp r0, #9
    bne L_0220ff1c
    mov r0, r5
    bl native_fn_0220fbb4
L_0220ff1c:
    mov r0, r4
    ldmia sp!, {r3, r4, r5, pc}
}
