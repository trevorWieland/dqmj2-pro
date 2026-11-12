/* ov000 row 0x0221ff50: 512 bytes.
 *
 * What it does: Moves 4-register chunks between two pointers with writeback block moves (2 loads, 2 stores).
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x1f0 -> constant 0x022463b0 (image word 0x022463b0)
 *   pool +0x1f4 -> constant 0x2aaaaaab (image word 0x2aaaaaab)
 *   pool +0x1f8 -> constant 0x022463f6 (image word 0x022463f6)
 *   pool +0x1fc -> constant 0x022463e2 (image word 0x022463e2)
 *   branch +0x28 -> +0x5c
 *   back edge +0x58 -> +0x30
 *   branch +0xa4 -> +0x12c
 *   branch +0xb0 -> +0x134
 *   branch +0xf0 -> +0x11c
 *   branch +0xfc -> +0x118
 *   back edge +0x124 -> +0xc0
 *   branch +0x128 -> +0x134
 *   back edge +0x194 -> +0x188
 *   back edge +0x1dc -> +0x1d0
 *   test +0x24 cmp r0, #0
 *   test +0x40 cmp r0, r6
 *   test +0x54 cmp r5, r0
 *   test +0x5c cmp r9, #0
 *   test +0xa0 cmp r0, #0
 *   test +0xa8 cmp r9, #0
 *   test +0xec cmp r1, r0
 *   test +0xf8 cmp r10, #5
 *   test +0x120 cmp r10, r9
 *   9 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221ff50; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_0221f6e8(void);
extern void native_fn_0221c8dc(void);
extern void native_fn_0207cd98(void);
extern void native_fn_02062a10(void);
extern void native_fn_02049008(void);
extern void native_fn_02008e0c(void);


asm u32 native_ov000_0221ff50 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, lr}
    sub sp, sp, #8
    mov r4, r0
    ldr r0, [r4]
    ldr r7, =0x022463b0
    mov r9, #0
    str r0, [r7, #0xc]
    ldr r0, [r7, #0x10]
    mov r5, r9
    cmp r0, #0
    ble ov000_0221ff50_L5c
    mvn r6, #0
ov000_0221ff50_L30:
    ldr r1, [r7, #0xc]
    mov r0, r5
    and r1, r1, #255
    bl native_fn_0221f6e8
    cmp r0, r6
    addne r0, r9, #1
    andne r9, r0, #255
    ldr r0, [r7, #0x10]
    add r5, r5, #1
    cmp r5, r0
    blt ov000_0221ff50_L30
ov000_0221ff50_L5c:
    cmp r9, #0
    moveq r9, #1
    mov r2, #0
    str r2, [sp]
    mov r5, #1
    mov r0, r4
    mov r1, r9
    mov r2, #6
    mov r3, #20
    str r5, [sp, #0x4]
    bl native_fn_0221c8dc
    ldr r8, =0x022463b0
    mov r0, #132
    ldr r2, [r8, #0x1c]
    ldr r1, [r8, #0xc]
    mla r0, r1, r0, r2
    ldr r0, [r0, #0x14]
    cmp r0, #0
    beq ov000_0221ff50_L12c
    cmp r9, #0
    mov r10, #0
    ble ov000_0221ff50_L134
    ldr r6, =0x2aaaaaab
    mov r5, #6
    mov r7, #132
ov000_0221ff50_Lc0:
    ldr r1, [r8, #0xc]
    mov r0, r10
    and r1, r1, #255
    bl native_fn_0221f6e8
    bl native_fn_0207cd98
    bl native_fn_02062a10
    ldr r1, [r8, #0x1c]
    ldr r2, [r8, #0xc]
    ldr r0, [r0, #0x14]
    mla r1, r2, r7, r1
    ldr r1, [r1, #0x14]
    cmp r1, r0
    bne ov000_0221ff50_L11c
    str r10, [r4]
    cmp r10, #5
    ble ov000_0221ff50_L118
    smull r0, r1, r6, r10
    add r1, r1, r10, lsr #31
    smull r0, r1, r5, r1
    sub r1, r10, r0
    sub r0, r10, r1
    str r0, [r4, #0x4]
ov000_0221ff50_L118:
    mov r10, r9
ov000_0221ff50_L11c:
    add r10, r10, #1
    cmp r10, r9
    blt ov000_0221ff50_Lc0
    b ov000_0221ff50_L134
ov000_0221ff50_L12c:
    mov r0, #0
    str r0, [r4]
ov000_0221ff50_L134:
    mov r5, #2
    mov r0, r4
    mov r1, #20
    mov r2, #0
    mov r3, #1
    str r5, [sp]
    bl native_fn_02049008
    ldr r0, =0x022463b0
    ldr r3, =0x022463f6
    ldr r1, [r0, #0xc]
    mov r2, #20
    mla r0, r1, r2, r3
    ldr r1, =0x022463e2
    bl native_fn_02008e0c
    ldr r1, =0x022463b0
    mov r0, #132
    ldr r7, [r1, #0xc]
    ldr r2, [r1, #0x1c]
    ldr r6, [r1, #0x24]
    mla r5, r7, r0, r2
    mov r4, #8
ov000_0221ff50_L188:
    ldmia r5!, {r0, r1, r2, r3}
    stmia r6!, {r0, r1, r2, r3}
    subs r4, r4, #1
    bne ov000_0221ff50_L188
    ldr r2, [r5]
    and r1, r7, #255
    mov r0, #0
    str r2, [r6]
    bl native_fn_0221f6e8
    bl native_fn_0207cd98
    bl native_fn_02062a10
    ldr r2, =0x022463b0
    mov r1, #132
    ldr r3, [r2, #0x1c]
    ldr r2, [r2, #0xc]
    mov r6, r0
    mla r5, r2, r1, r3
    mov r4, #8
ov000_0221ff50_L1d0:
    ldmia r6!, {r0, r1, r2, r3}
    stmia r5!, {r0, r1, r2, r3}
    subs r4, r4, #1
    bne ov000_0221ff50_L1d0
    ldr r0, [r6]
    str r0, [r5]
    add sp, sp, #8
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
}
