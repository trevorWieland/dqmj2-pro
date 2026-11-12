/* ov000 row 0x021f0c50: 852 bytes.
 *
 * What it does: 209 instructions and 41 call(s), then a 7-entry dispatch through an inline branch table at 0x021f0c74 (dispatch word at 0x021f0c6c)
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

extern void native_fn_020c49e8(void);
extern void native_fn_021f2e70(void);
extern void native_fn_021f2fcc(void);
extern void native_fn_021f2a48(void);
extern void native_fn_020675d8(void);
extern void native_fn_021f2644(void);
extern void native_fn_021f2edc(void);
extern void native_fn_021f2f4c(void);
extern void native_fn_021f2a7c(void);
extern void native_fn_020620e8(void);
extern void native_fn_021f26b4(void);
extern void native_fn_02205580(void);
extern void native_fn_020620b4(void);
extern void native_fn_021f2a64(void);
extern u8 native_data_0222b942[];
extern u8 native_data_0222b926[];
extern u8 native_data_0222b932[];


asm u32 native_ov000_021f0c50 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    sub sp, sp, #8
    bl native_fn_020c49e8
    ldr r0, [pc, #0x330]
    ldr r0, [r0, #0x8]
    ldrsb r0, [r0, #32]
    cmp r0, #6
    addls pc, pc, r0, lsl #2
    b L_021f0f84
    dcd 0xea000005
    dcd 0xea00001b
    dcd 0xea00002e
    dcd 0xea000051
    dcd 0xea000064
    dcd 0xea000088
    dcd 0xea00009a
    mov r0, #25
    bl native_fn_021f2e70
    mov r0, #4
    str r0, [sp]
    mov r1, #23
    ldr r0, [pc, #0x2e8]
    str r1, [sp, #0x4]
    ldr r0, [r0, #0x8]
    mov r1, #3
    add r0, r0, #16
    mov r2, #6
    mov r3, #1
    bl native_fn_021f2fcc
    mov r0, #184
    bl native_fn_021f2a48
    mov r0, #1
    bl native_fn_020675d8
    ldr r0, [pc, #0x2b8]
    ldr r1, [r0, #0x8]
    ldr r0, [r1, #0x100]
    str r0, [r1, #0x10]
    bl native_fn_021f2644
    b L_021f0f84
    mov r0, #22
    bl native_fn_021f2e70
    mov r0, #4
    mov r1, #9
    str r0, [sp]
    mov r2, #28
    ldr r0, [pc, #0x288]
    str r2, [sp, #0x4]
    ldr r0, [r0, #0x8]
    mov r2, r1
    add r0, r0, #16
    mov r3, #1
    bl native_fn_021f2fcc
    mov r0, #224
    bl native_fn_021f2a48
    ldr r0, [pc, #0x264]
    ldr r1, [r0, #0x8]
    ldr r0, [r1, #0x104]
    str r0, [r1, #0x10]
    b L_021f0f84
    mov r0, #22
    bl native_fn_021f2e70
    ldr r0, [pc, #0x248]
    ldr r1, [pc, #0x248]
    ldr r0, [r0, #0x8]
    add r0, r0, #4096
    ldrb r0, [r0, #0x921]
    mov r0, r0, lsl #2
    ldrh r0, [r1, r0]
    bl native_fn_021f2edc
    ldr r0, [pc, #0x228]
    mov r1, #7
    ldr r2, [r0, #0x8]
    mov r0, #28
    str r1, [sp]
    str r0, [sp, #0x4]
    add r0, r2, #6400
    ldrh r1, [r0, #24]
    add r0, r2, #16
    mov r2, #6
    mov r3, #1
    bl native_fn_021f2fcc
    bl native_fn_021f2f4c
    mov r0, #1
    bl native_fn_021f2a7c
    mov r0, #224
    bl native_fn_021f2a48
    ldr r1, [pc, #0x1e4]
    mov r0, #13
    ldr r3, [r1, #0x8]
    mov r1, #1
    ldr r2, [r3, #0x108]
    str r2, [r3, #0x10]
    bl native_fn_020620e8
    bl native_fn_021f26b4
    b L_021f0f84
    mov r0, #23
    bl native_fn_021f2e70
    mov r0, #4
    str r0, [sp]
    mov r1, #28
    ldr r0, [pc, #0x1ac]
    str r1, [sp, #0x4]
    ldr r0, [r0, #0x8]
    mov r1, #3
    add r0, r0, #16
    mov r2, #6
    mov r3, #1
    bl native_fn_021f2fcc
    mov r0, #224
    bl native_fn_021f2a48
    ldr r0, [pc, #0x184]
    ldr r1, [r0, #0x8]
    ldr r0, [r1, #0x104]
    str r0, [r1, #0x10]
    b L_021f0f84
    mov r0, #23
    bl native_fn_021f2e70
    ldr r0, [pc, #0x168]
    ldr r1, [pc, #0x16c]
    ldr r0, [r0, #0x8]
    add r0, r0, #4096
    ldrb r0, [r0, #0x921]
    mov r0, r0, lsl #2
    ldrh r0, [r1, r0]
    bl native_fn_021f2edc
    ldr r0, [pc, #0x148]
    mov r1, #7
    ldr r2, [r0, #0x8]
    mov r0, #28
    str r1, [sp]
    str r0, [sp, #0x4]
    add r0, r2, #6400
    ldrh r1, [r0, #24]
    add r0, r2, #16
    mov r2, #6
    mov r3, #1
    bl native_fn_021f2fcc
    bl native_fn_021f2f4c
    mov r0, #1
    bl native_fn_021f2a7c
    mov r0, #224
    bl native_fn_021f2a48
    ldr r1, [pc, #0x104]
    mov r0, #14
    ldr r3, [r1, #0x8]
    mov r1, #1
    ldr r2, [r3, #0x108]
    str r2, [r3, #0x10]
    bl native_fn_020620e8
    bl native_fn_02205580
    bl native_fn_021f26b4
    b L_021f0f84
    mov r0, #24
    bl native_fn_021f2e70
    mov r1, #4
    str r1, [sp]
    mov r2, #28
    ldr r0, [pc, #0xc8]
    str r2, [sp, #0x4]
    ldr r0, [r0, #0x8]
    mov r2, #6
    add r0, r0, #16
    mov r3, #1
    bl native_fn_021f2fcc
    mov r0, #224
    bl native_fn_021f2a48
    ldr r0, [pc, #0xa4]
    ldr r1, [r0, #0x8]
    ldr r0, [r1, #0x104]
    str r0, [r1, #0x10]
    b L_021f0f84
    mov r0, #24
    bl native_fn_021f2e70
    ldr r0, [pc, #0x88]
    ldr r1, [pc, #0x90]
    ldr r0, [r0, #0x8]
    add r0, r0, #4096
    ldrb r0, [r0, #0x921]
    mov r0, r0, lsl #2
    ldrh r0, [r1, r0]
    bl native_fn_021f2edc
    ldr r0, [pc, #0x68]
    mov r1, #7
    ldr r2, [r0, #0x8]
    mov r0, #28
    str r1, [sp]
    str r0, [sp, #0x4]
    add r0, r2, #6400
    ldrh r1, [r0, #24]
    add r0, r2, #16
    mov r2, #6
    mov r3, #1
    bl native_fn_021f2fcc
    bl native_fn_021f2f4c
    mov r0, #1
    bl native_fn_021f2a7c
    mov r0, #224
    bl native_fn_021f2a48
    ldr r1, [pc, #0x24]
    mov r0, #15
    ldr r2, [r1, #0x8]
    ldr r1, [r2, #0x108]
    str r1, [r2, #0x10]
    bl native_fn_020620b4
    bl native_fn_021f26b4
L_021f0f84:
    mov r0, #1
    bl native_fn_021f2a64
    add sp, sp, #8
    ldmia sp!, {r3, pc}
    dcd 0x02236d98
    dcd native_data_0222b942
    dcd native_data_0222b926
    dcd native_data_0222b932
}
