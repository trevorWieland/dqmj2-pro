#include "context000.h"

double native_main_02023790(const decimal *d)
{
	if (d->sig.length <= 0) {
		return native_fn_0202263c(0.0, d->sign == 0 ? 1.0 : -1.0);
    }
	switch (d->sig.text[0]) {
	case '0':
		return native_fn_0202263c(0.0, d->sign == 0 ? 1.0 : -1.0);
	case 'I':
		return native_fn_0202263c(native_fn_02025930(native_data_020dceb8 ), d->sign == 0 ? 1.0 : -1.0);
	case 'N':
		{
            double result;
            long long *ll = (long long*)&result;
            *ll = 0x7FF0000000000000ULL;
            if (d->sign)
                *ll |= 0x8000000000000000ULL;
            *ll |= 0x0008000000000000ULL;
            return result;
		}
	}
	{
        decimal dec = *d;
        unsigned char *i = dec.sig.text;
        unsigned char *e = i + dec.sig.length;
        double first_guess;
        int exponent;
        for (; i < e; ++i) {
            *i -= '0';
        }
        dec.exponent += dec.sig.length - 1;
        exponent = dec.exponent;
        {
            decimal max;
            native_fn_02022ce4(&max, native_data_020dd2a0, 308);
            if (native_fn_020231e4(&max, &dec)) {
                return native_fn_0202263c(native_fn_02025930(native_data_020dceb8 ), d->sign == 0 ? 1.0 : -1.0);
            }
        }
        i = dec.sig.text;
        first_guess = *i++;
        while (i < e) {
            unsigned long ival = 0;
            int j;
            double temp1, temp2;
            int ndig = (int)(e - i) % 8;
            if (ndig == 0) {
                ndig = 8;
            }
            for (j = 0; j < ndig; ++j, ++i) {
                ival = ival * 10 + *i;
            }
            temp1 = first_guess * native_data_020dd18c[ndig - 1];
            temp2 = temp1 + ival;
            if (ival != 0 && temp1 == temp2) {
                break;
            }
            first_guess = temp2;
            exponent -= ndig;
        }
        if (exponent < 0) {
            first_guess /= native_fn_0202298c(5.0, -exponent);
        }
        else {
            first_guess *= native_fn_0202298c(5.0, exponent);
        }
        first_guess = native_fn_02022740(first_guess, exponent);
        if (native_fn_02023e5c(first_guess) == 2) {
            first_guess = 1.7976931348623157e308;
        }
        {
            decimal feedback1, feedback2, difflow, diffhigh;
            double next_guess;
            long long *ull = (long long*)&next_guess;
            int guessed_low = 0;
            native_fn_02023568(&feedback1, first_guess);
            if (native_fn_02023104(&feedback1, &dec)) {
                goto done;
            }
            if (native_fn_020231e4(&feedback1, &dec)) {
                guessed_low = 1;
            }
            next_guess = first_guess;
            while (1) {
                if (guessed_low) {
                    ++*ull;
                    if (native_fn_02023e5c(next_guess) == 2) {
                        goto done;
                    }
                }
                else {
                    --*ull;
                }
                native_fn_02023568(&feedback2, next_guess);
                if (guessed_low && !native_fn_020231e4(&feedback2, &dec)) {
                    break;
                }
                else if (!guessed_low && !native_fn_020231e4(&dec, &feedback2)) {
                    difflow = feedback1;
                    feedback1 = feedback2;
                    feedback2 =  difflow;
                    {
                        double temp = first_guess;
                        first_guess = next_guess;
                        next_guess = temp;
                    }
                    break;
                }
                feedback1 = feedback2;
                first_guess = next_guess;
            }
            native_fn_020232c4(&difflow, &dec, &feedback1);
            native_fn_020232c4(&diffhigh, &feedback2, &dec);
            if (native_fn_02023104(&difflow, &diffhigh)) {
                if (*(long long*)&first_guess & 1) {
                    first_guess = next_guess;
                }
            }
            else if (!native_fn_020231e4(&difflow, &diffhigh)) {
                first_guess = next_guess;
            }
        }
        done:
            if (dec.sign) {
                first_guess = -first_guess;
            }
            return first_guess;
	}
}
