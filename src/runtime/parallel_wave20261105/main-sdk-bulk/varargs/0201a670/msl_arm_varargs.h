#ifndef _MSL_STDARG_ARM_H
#define _MSL_STDARG_ARM_H
#define __std(x) x
#define _MSL_STDARG_ARM_H
#define __fourbytealign(n) ((((unsigned long)(n)) + 3U) & ~3U)
#define __va_start(parm) ((__std(va_list)) ((char *)((unsigned long)(&parm) & ~3U) + __fourbytealign(sizeof(parm))))
#define va_start(ap, parm) ((ap) = __va_start(parm))
#define va_arg(ap, type) (*(type *)((ap += __fourbytealign(sizeof(type))) - __fourbytealign(sizeof(type))))
#define va_end(ap) ((void)0)
#define va_copy(dest, src) dest = src
#endif
