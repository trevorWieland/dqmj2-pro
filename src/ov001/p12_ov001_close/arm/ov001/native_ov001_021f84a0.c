/* ov001 row 0x021f84a0: 632 bytes.
 *
 * What it does: 156 instructions; 21 call(s) to 0x021db8d0, 0x021f4210, 0x021f1bbc, +18 more; loops (back edge at +0x1c); returns through pop {r3, r4, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 21 calls (156 instructions, 21 calls, 19 branches, 16 back edges, 2 literal slots).
 *
 *   pool +0x270 -> constant 0x0223989c (image word 0x0223989c)
 *   pool +0x274 -> constant 0x66666667 (image word 0x66666667)
 *   branch +0x14 -> +0x78
 *   branch +0x24 -> +0x40
 *   branch +0x4c -> +0x6c
 *   branch +0x74 -> +0x264
 *   branch +0x7c -> +0xb4
 *   branch +0x88 -> +0x264
 *   branch +0xb0 -> +0x264
 *   branch +0xb8 -> +0x208
 *   branch +0xc4 -> +0x138
 *   branch +0xd4 -> +0x124
 *   branch +0xec -> +0x100
 *   branch +0x120 -> +0x180
 *   branch +0x134 -> +0x180
 *   branch +0x13c -> +0x180
 *   branch +0x204 -> +0x264
 *   branch +0x20c -> +0x24c
 *   branch +0x224 -> +0x264
 *   branch +0x238 -> +0x264
 *   branch +0x248 -> +0x264
 *   branch +0x250 -> +0x264
 *   test +0x10 cmp r1, #0
 *   test +0x20 cmp r0, #0
 *   test +0x48 cmp r1, #0
 *   test +0x78 cmp r1, #5
 *   test +0x84 cmp r0, #0
 *   test +0xb4 cmp r1, #10
 *   test +0xc0 cmp r1, #151
 *   test +0xd0 cmp r0, #0
 *   test +0xe4 cmp r0, #1
 *   test +0x138 cmp r1, #152
 *   test +0x208 cmp r1, #20
 *   test +0x220 cmp r1, #30
 *   test +0x234 cmp r0, #0
 *   test +0x24c cmp r1, #100
 *   0 block transfer(s), 12 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f84a0; the literal pool and
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

extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_021f4210(void);
extern void native_fn_021f1bbc(void);
extern void native_fn_021f82d8(void);
extern void native_fn_021ee9fc(void);
extern void native_fn_021dc9d4(void);
extern void native_fn_021dbd24(void);
extern void native_fn_021d9494(void);
extern void native_fn_021f949c(void);
extern void native_fn_021ee78c(void);
extern void native_fn_021f0eb4(void);
extern void native_fn_022024d4(void);
extern void native_fn_021dbb14(void);
extern void native_fn_021dbb9c(void);


asm u32 native_ov001_021f84a0 (register u32 a0)
{
    stmdb sp!, {r3, r4, lr}
    sub sp, sp, #4
    ldr r0, =0x0223989c
    ldrb r1, [r0, #0x27]
    cmp r1, #0
    bne ov001_021f84a0_L78
    ldr r0, [r0, #0x78]
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    bne ov001_021f84a0_L40
    ldr r0, =0x0223989c
    mov r1, #27
    strb r1, [r0, #0x1b]
    add sp, sp, #4
    mov r0, #0
    ldmia sp!, {r3, r4, pc}
ov001_021f84a0_L40:
    ldr r0, =0x0223989c
    ldrb r1, [r0, #0x10]
    cmp r1, #0
    beq ov001_021f84a0_L6c
    bl native_fn_021f4210
    ldr r0, =0x0223989c
    mov r1, #3
    strb r1, [r0, #0x1b]
    add sp, sp, #4
    mov r0, #0
    ldmia sp!, {r3, r4, pc}
ov001_021f84a0_L6c:
    mov r1, #5
    strb r1, [r0, #0x27]
    b ov001_021f84a0_L264
ov001_021f84a0_L78:
    cmp r1, #5
    bne ov001_021f84a0_Lb4
    bl native_fn_021f1bbc
    cmp r0, #0
    bne ov001_021f84a0_L264
    ldr r0, =0x0223989c
    ldr r0, [r0, #0x78]
    bl native_fn_021f82d8
    ldr r0, =0x0223989c
    ldr r0, [r0, #0x78]
    bl native_fn_021ee9fc
    ldr r0, =0x0223989c
    mov r1, #10
    strb r1, [r0, #0x27]
    b ov001_021f84a0_L264
ov001_021f84a0_Lb4:
    cmp r1, #10
    bne ov001_021f84a0_L208
    ldrh r1, [r0, #80]
    cmp r1, #151
    bne ov001_021f84a0_L138
    ldr r0, [r0, #0x78]
    bl native_fn_021dc9d4
    cmp r0, #0
    beq ov001_021f84a0_L124
    ldr r0, =0x0223989c
    ldr r0, [r0, #0x78]
    bl native_fn_021dbd24
    cmp r0, #1
    moveq r4, #1
    beq ov001_021f84a0_L100
    ldr r0, =0x0223989c
    ldr r0, [r0, #0x78]
    bl native_fn_021dbd24
    sub r4, r0, #1
ov001_021f84a0_L100:
    ldr r0, =0x0223989c
    mov r1, #4
    ldr r0, [r0, #0x78]
    mov r2, #1
    bl native_fn_021d9494
    mov r0, #238
    mov r1, #1
    bl native_fn_021f949c
    b ov001_021f84a0_L180
ov001_021f84a0_L124:
    mov r0, #242
    mov r1, #1
    mov r4, #0
    bl native_fn_021f949c
    b ov001_021f84a0_L180
ov001_021f84a0_L138:
    cmp r1, #152
    bne ov001_021f84a0_L180
    ldr r0, [r0, #0x78]
    bl native_fn_021dbd24
    mov r3, r0, lsl #3
    ldr r1, =0x66666667
    ldr r2, =0x0223989c
    smull r0, r4, r1, r3
    mov r0, r3, lsr #31
    add r4, r0, r4, asr #2
    ldr r0, [r2, #0x78]
    mov r1, #4
    mov r2, #1
    add r4, r4, #1
    bl native_fn_021d9494
    mov r0, #238
    mov r1, #1
    bl native_fn_021f949c
ov001_021f84a0_L180:
    ldr r0, =0x0223989c
    ldr r0, [r0, #0x78]
    bl native_fn_021ee9fc
    ldr r0, =0x0223989c
    mov r3, #0
    ldr r2, [r0, #0x78]
    mov r1, r4
    strb r3, [r2, #0x357]
    str r3, [sp]
    ldrh r2, [r0, #80]
    ldr r0, [r0, #0x78]
    mov r3, #1
    bl native_fn_021ee78c
    ldr r0, =0x0223989c
    mov r1, r4
    ldrh r2, [r0, #80]
    ldr r0, [r0, #0x78]
    bl native_fn_021f0eb4
    ldr r0, =0x0223989c
    mov r2, r4
    ldr r1, [r0, #0x78]
    ldrb r0, [r1, #0x31e]
    ldrb r1, [r1, #0x31f]
    bl native_fn_022024d4
    ldr r0, =0x0223989c
    ldr r0, [r0, #0x78]
    ldrb r1, [r0, #0x31e]
    bl native_fn_021dbb14
    ldr r0, =0x0223989c
    mov r1, #20
    strb r1, [r0, #0x27]
    mov r1, #0
    strb r1, [r0, #0x26]
    b ov001_021f84a0_L264
ov001_021f84a0_L208:
    cmp r1, #20
    bne ov001_021f84a0_L24c
    ldrb r1, [r0, #0x26]
    add r2, r1, #1
    and r1, r2, #255
    strb r2, [r0, #0x26]
    cmp r1, #30
    blo ov001_021f84a0_L264
    ldr r0, [r0, #0x78]
    ldrb r1, [r0, #0x31e]
    bl native_fn_021dbb9c
    cmp r0, #0
    beq ov001_021f84a0_L264
    ldr r0, =0x0223989c
    mov r1, #100
    strb r1, [r0, #0x27]
    b ov001_021f84a0_L264
ov001_021f84a0_L24c:
    cmp r1, #100
    bne ov001_021f84a0_L264
    mov r1, #0
    strb r1, [r0, #0x27]
    mov r1, #27
    strb r1, [r0, #0x1b]
ov001_021f84a0_L264:
    mov r0, #0
    add sp, sp, #4
    ldmia sp!, {r3, r4, pc}
}
