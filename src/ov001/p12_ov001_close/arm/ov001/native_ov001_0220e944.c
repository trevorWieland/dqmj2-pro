/* ov001 row 0x0220e944: 580 bytes.
 *
 * What it does: 145 instructions; 27 call(s) to 0x021dcda8, 0x02209490, 0x0220e910, +24 more; loops (back edge at +0x1c); returns through pop {r3, r4, r5, r6, r7, r8, pc}
 *
 * Decoded shape: loop with 27 calls (145 instructions, 27 calls, 5 branches, 19 back edges, 0 literal slots).
 *
 *   branch +0x40 -> +0x238
 *   branch +0x6c -> +0xd0
 *   branch +0xb0 -> +0xd0
 *   branch +0xe4 -> +0x148
 *   branch +0x128 -> +0x148
 *   branch +0x15c -> +0x1c0
 *   branch +0x1a0 -> +0x1c0
 *   branch +0x1d4 -> +0x238
 *   branch +0x218 -> +0x238
 *   test +0x20 cmp r0, #0
 *   test +0x3c cmp r6, #0
 *   test +0x68 cmp r0, #0
 *   test +0xac cmp r0, #0
 *   test +0xe0 cmp r0, #0
 *   test +0x124 cmp r0, #0
 *   test +0x158 cmp r0, #0
 *   test +0x19c cmp r0, #0
 *   test +0x1d0 cmp r0, #0
 *   test +0x214 cmp r0, #0
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220e944; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity fixes the instruction stream, not the field, block and callee semantics behind the addresses and strides it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_021dcda8(void);
extern void native_fn_02209490(void);
extern void native_fn_0220e910(void);
extern void native_fn_0207b674(void);
extern void native_fn_0220e3a8(void);
extern void native_fn_021d908c(void);
extern void native_fn_02210ad0(void);
extern void native_fn_021dbf98(void);


asm u32 native_ov001_0220e944 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, lr}
    sub sp, sp, #4
    mov r7, r1
    mov r8, r0
    mov r0, r7
    mov r6, r2
    mov r4, #0
    bl native_fn_021dcda8
    cmp r0, #0
    addne sp, sp, #4
    movne r0, r4
    ldmneia sp!, {r3, r4, r5, r6, r7, r8, pc}
    add r0, r7, #556
    bl native_fn_02209490
    mov r5, r0
    cmp r6, #0
    bne ov001_0220e944_L238
    ldrb r0, [r7, #0x31e]
    mov r1, #12
    mov r2, #9
    bl native_fn_0220e910
    ldr r1, [r8, #0x1e8]
    mov r6, r0
    add r1, r1, #70
    mov r0, #34
    bl native_fn_0207b674
    cmp r0, #0
    ble ov001_0220e944_Ld0
    ldr r1, [r7, #0x1e8]
    mov r0, r8
    ldrb r3, [r1, #0x91]
    mov r2, r4
    mov r1, #11
    str r2, [sp]
    bl native_fn_0220e3a8
    mov r1, r0
    mov r0, r6
    mov r2, r5
    bl native_fn_021d908c
    mov r2, r0
    mov r0, r8
    mov r1, #100
    bl native_fn_02210ad0
    cmp r0, #0
    beq ov001_0220e944_Ld0
    mov r3, r4
    mov r0, r7
    mov r1, #6
    mov r2, #1
    str r3, [sp]
    bl native_fn_021dbf98
    orr r4, r4, r0
ov001_0220e944_Ld0:
    ldr r1, [r8, #0x1e8]
    mov r0, #33
    add r1, r1, #70
    bl native_fn_0207b674
    cmp r0, #0
    ble ov001_0220e944_L148
    ldr r1, [r7, #0x1e8]
    mov r0, r8
    ldrb r3, [r1, #0x98]
    mov r2, #0
    mov r1, #18
    str r2, [sp]
    bl native_fn_0220e3a8
    mov r1, r0
    mov r0, r6
    mov r2, r5
    bl native_fn_021d908c
    mov r2, r0
    mov r0, r8
    mov r1, #100
    bl native_fn_02210ad0
    cmp r0, #0
    beq ov001_0220e944_L148
    mov r3, #0
    mov r0, r7
    mov r1, #9
    mov r2, #1
    str r3, [sp]
    bl native_fn_021dbf98
    orr r4, r4, r0
ov001_0220e944_L148:
    ldr r1, [r8, #0x1e8]
    mov r0, #35
    add r1, r1, #70
    bl native_fn_0207b674
    cmp r0, #0
    ble ov001_0220e944_L1c0
    ldr r1, [r7, #0x1e8]
    mov r0, r8
    ldrb r3, [r1, #0x96]
    mov r2, #0
    mov r1, #16
    str r2, [sp]
    bl native_fn_0220e3a8
    mov r1, r0
    mov r0, r6
    mov r2, r5
    bl native_fn_021d908c
    mov r2, r0
    mov r0, r8
    mov r1, #100
    bl native_fn_02210ad0
    cmp r0, #0
    beq ov001_0220e944_L1c0
    mov r3, #0
    mov r0, r7
    mov r1, #11
    mov r2, #1
    str r3, [sp]
    bl native_fn_021dbf98
    orr r4, r4, r0
ov001_0220e944_L1c0:
    ldr r1, [r8, #0x1e8]
    mov r0, #36
    add r1, r1, #70
    bl native_fn_0207b674
    cmp r0, #0
    ble ov001_0220e944_L238
    ldr r1, [r7, #0x1e8]
    mov r0, r8
    ldrb r3, [r1, #0x99]
    mov r2, #0
    mov r1, #19
    str r2, [sp]
    bl native_fn_0220e3a8
    mov r1, r0
    mov r0, r6
    mov r2, r5
    bl native_fn_021d908c
    mov r2, r0
    mov r0, r8
    mov r1, #100
    bl native_fn_02210ad0
    cmp r0, #0
    beq ov001_0220e944_L238
    mov r3, #0
    mov r0, r7
    mov r1, #10
    mov r2, #1
    str r3, [sp]
    bl native_fn_021dbf98
    orr r4, r4, r0
ov001_0220e944_L238:
    mov r0, r4
    add sp, sp, #4
    ldmia sp!, {r3, r4, r5, r6, r7, r8, pc}
}
