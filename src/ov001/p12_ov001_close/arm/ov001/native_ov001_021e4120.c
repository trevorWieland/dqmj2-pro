/* ov001 row 0x021e4120: 992 bytes.
 *
 * What it does: 248 instructions; 44 call(s) to 0x02062a10, 0x02044cdc, 0x02044a14, +41 more; loops (back edge at +0x14); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: block fill (248 instructions, 44 calls, 5 branches, 38 back edges, 0 literal slots).
 *
 *   branch +0x44 -> +0x58
 *   branch +0x4c -> +0x64
 *   branch +0x54 -> +0x70
 *   branch +0x60 -> +0x78
 *   branch +0x6c -> +0x78
 *   test +0x40 cmp r0, #0
 *   test +0x48 cmp r0, #1
 *   test +0x50 cmp r0, #2
 *   5 block transfer(s), 27 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021e4120; the literal pool and
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

extern void native_fn_02062a10(void);
extern void native_fn_02044cdc(void);
extern void native_fn_02044a14(void);
extern void native_fn_021e8e08(void);
extern void native_fn_02026144(void);
extern void native_fn_021e404c(void);
extern void native_fn_021e409c(void);
extern void native_fn_02044a58(void);
extern void native_fn_02044a9c(void);
extern void native_fn_02044ae0(void);
extern void native_fn_02044b24(void);
extern void native_fn_02044b68(void);


asm u32 native_ov001_021e4120 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #40
    mov r10, r0
    mov r0, r1
    mov r9, r2
    bl native_fn_02062a10
    ldrsh r1, [r0, #24]
    ldrb r6, [r0, #0x1a]
    str r1, [sp, #0xc]
    ldrsh r1, [r0, #64]
    str r1, [sp, #0x10]
    ldrb r7, [r0, #0x4c]
    ldrsh r11, [r0, #66]
    ldrb r8, [r0, #0x4d]
    ldr r0, [sp, #0xc]
    bl native_fn_02044cdc
    cmp r0, #0
    beq ov001_021e4120_L58
    cmp r0, #1
    beq ov001_021e4120_L64
    cmp r0, #2
    beq ov001_021e4120_L70
ov001_021e4120_L58:
    mov r4, #1
    mov r5, r4
    b ov001_021e4120_L78
ov001_021e4120_L64:
    mov r4, #3
    mov r5, #2
    b ov001_021e4120_L78
ov001_021e4120_L70:
    mov r4, #2
    mov r5, #1
ov001_021e4120_L78:
    ldr r0, [sp, #0xc]
    mov r1, r6
    mov r2, r9
    bl native_fn_02044a14
    mov r1, r9
    bl native_fn_021e8e08
    sub r1, r5, #1
    mla r0, r4, r0, r1
    mov r1, r5
    bl native_fn_02026144
    mov r1, r0
    mov r0, r6
    bl native_fn_021e404c
    ldrsh r3, [r10]
    mov r1, r7
    mov r2, r9
    add r0, r3, r0
    strh r0, [r10]
    ldr r0, [sp, #0x10]
    bl native_fn_02044a14
    str r0, [sp, #0x14]
    mov r0, r11
    mov r1, r8
    mov r2, r9
    bl native_fn_02044a14
    ldr r1, [sp, #0x14]
    mov r2, r7
    str r1, [sp]
    stmib sp, {r0, r9}
    ldr r0, [sp, #0x10]
    mov r1, r11
    mov r3, r8
    bl native_fn_021e409c
    ldrsh r3, [r10]
    mov r1, r6
    mov r2, r9
    add r0, r3, r0
    strh r0, [r10]
    ldr r0, [sp, #0xc]
    bl native_fn_02044a58
    mov r1, r9
    bl native_fn_021e8e08
    sub r1, r5, #1
    mla r0, r4, r0, r1
    mov r1, r5
    bl native_fn_02026144
    mov r1, r0
    mov r0, r6
    bl native_fn_021e404c
    ldrsh r3, [r10, #2]
    mov r1, r7
    mov r2, r9
    add r0, r3, r0
    strh r0, [r10, #2]
    ldr r0, [sp, #0x10]
    bl native_fn_02044a58
    str r0, [sp, #0x18]
    mov r0, r11
    mov r1, r8
    mov r2, r9
    bl native_fn_02044a58
    ldr r1, [sp, #0x18]
    mov r2, r7
    str r1, [sp]
    str r0, [sp, #0x4]
    ldr r0, [sp, #0x10]
    mov r1, r11
    str r9, [sp, #0x8]
    mov r3, r8
    bl native_fn_021e409c
    ldrsh r3, [r10, #2]
    mov r1, r6
    mov r2, r9
    add r0, r3, r0
    strh r0, [r10, #2]
    ldr r0, [sp, #0xc]
    bl native_fn_02044a9c
    mov r1, r9
    bl native_fn_021e8e08
    sub r1, r5, #1
    mla r0, r4, r0, r1
    mov r1, r5
    bl native_fn_02026144
    mov r1, r0
    mov r0, r6
    bl native_fn_021e404c
    ldrsh r3, [r10, #4]
    mov r1, r7
    mov r2, r9
    add r0, r3, r0
    strh r0, [r10, #4]
    ldr r0, [sp, #0x10]
    bl native_fn_02044a9c
    str r0, [sp, #0x1c]
    mov r0, r11
    mov r1, r8
    mov r2, r9
    bl native_fn_02044a9c
    ldr r1, [sp, #0x1c]
    mov r2, r7
    str r1, [sp]
    stmib sp, {r0, r9}
    ldr r0, [sp, #0x10]
    mov r1, r11
    mov r3, r8
    bl native_fn_021e409c
    ldrsh r3, [r10, #4]
    mov r1, r6
    mov r2, r9
    add r0, r3, r0
    strh r0, [r10, #4]
    ldr r0, [sp, #0xc]
    bl native_fn_02044ae0
    mov r1, r9
    bl native_fn_021e8e08
    sub r1, r5, #1
    mla r0, r4, r0, r1
    mov r1, r5
    bl native_fn_02026144
    mov r1, r0
    mov r0, r6
    bl native_fn_021e404c
    ldrsh r3, [r10, #6]
    mov r1, r7
    mov r2, r9
    add r0, r3, r0
    strh r0, [r10, #6]
    ldr r0, [sp, #0x10]
    bl native_fn_02044ae0
    str r0, [sp, #0x20]
    mov r0, r11
    mov r1, r8
    mov r2, r9
    bl native_fn_02044ae0
    ldr r1, [sp, #0x20]
    mov r2, r7
    str r1, [sp]
    stmib sp, {r0, r9}
    ldr r0, [sp, #0x10]
    mov r1, r11
    mov r3, r8
    bl native_fn_021e409c
    ldrsh r3, [r10, #6]
    mov r1, r6
    mov r2, r9
    add r0, r3, r0
    strh r0, [r10, #6]
    ldr r0, [sp, #0xc]
    bl native_fn_02044b24
    mov r1, r9
    bl native_fn_021e8e08
    sub r1, r5, #1
    mla r0, r4, r0, r1
    mov r1, r5
    bl native_fn_02026144
    mov r1, r0
    mov r0, r6
    bl native_fn_021e404c
    ldrsh r3, [r10, #8]
    mov r1, r7
    mov r2, r9
    add r0, r3, r0
    strh r0, [r10, #8]
    ldr r0, [sp, #0x10]
    bl native_fn_02044b24
    str r0, [sp, #0x24]
    mov r0, r11
    mov r1, r8
    mov r2, r9
    bl native_fn_02044b24
    ldr r1, [sp, #0x24]
    mov r2, r7
    str r1, [sp]
    stmib sp, {r0, r9}
    ldr r0, [sp, #0x10]
    mov r1, r11
    mov r3, r8
    bl native_fn_021e409c
    ldrsh r3, [r10, #8]
    mov r1, r6
    mov r2, r9
    add r0, r3, r0
    strh r0, [r10, #8]
    ldr r0, [sp, #0xc]
    bl native_fn_02044b68
    mov r1, r9
    bl native_fn_021e8e08
    sub r1, r5, #1
    mla r0, r4, r0, r1
    mov r1, r5
    bl native_fn_02026144
    mov r1, r0
    mov r0, r6
    bl native_fn_021e404c
    ldrsh r3, [r10, #10]
    mov r1, r7
    mov r2, r9
    add r0, r3, r0
    strh r0, [r10, #10]
    ldr r0, [sp, #0x10]
    bl native_fn_02044b68
    mov r4, r0
    mov r0, r11
    mov r1, r8
    mov r2, r9
    bl native_fn_02044b68
    str r4, [sp]
    stmib sp, {r0, r9}
    ldr r0, [sp, #0x10]
    mov r1, r11
    mov r2, r7
    mov r3, r8
    bl native_fn_021e409c
    ldrsh r1, [r10, #10]
    add r0, r1, r0
    strh r0, [r10, #10]
    add sp, sp, #40
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
