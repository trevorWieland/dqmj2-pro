#ifndef P6_OV006_BLX_AUTH_CONTEXT_H
#define P6_OV006_BLX_AUTH_CONTEXT_H

typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;

/* Nineteen ov006 Thumb rows that call ARM functions through an R_ARM_THM_CALL
   relocation. The original linker expanded that relocation to a BLX immediate
   (second halfword bit 12 clear). mwccarm emits the BL placeholder for every
   interworking call, so the mode has to come from the target:
   docs/authoring/2026-11-11-blx-mode-fix.md. */

#endif
