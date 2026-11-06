#include "context000.h"

double native_main_020212f8(double x, double y)
{
	double z, ax, z_h, z_l, p_h, p_l;
	double y1, t1, t2, r, s, t, u, v, w;
	int i0, i1, i, j, k, yisint, n;
	int hx, hy, ix, iy;
	unsigned int lx, ly;
	i0 = ((*(int*)&one) >> 29) ^ 1;
	i1 = 1 - i0;
	hx = (((int *)&(x))[1]) ;
	lx = (((unsigned int *)&(x))[0]) ;
	hy = (((int *)&(y))[1]) ;
	ly = (((unsigned int *)&(y))[0]) ;
	ix = hx & 0x7fffffff;
	iy = hy & 0x7fffffff;
	if ((iy | ly) == 0)
		return one;
	if (ix > 0x7ff00000 || ((ix == 0x7ff00000) && (lx != 0)) || iy > 0x7ff00000 || ((iy == 0x7ff00000) && (ly != 0)))
		return x + y;
	yisint = 0;
	if (hx < 0) {
		if (iy >= 0x43400000)
			yisint = 2;
		else if (iy >= 0x3ff00000) {
			k = (iy >> 20) - 0x3ff;
			if (k > 20) {
				j = ly >> (52 - k);
				if ((j << (52 - k)) == ly)
					yisint = 2 - (j & 1);
			} else if (ly == 0) {
				j = iy >> (20 - k);
				if ((j << (20 - k)) == iy)
					yisint = 2 - (j & 1);
			}
		}
	}
	if (ly == 0) {
		if (iy == 0x7ff00000) {
			if (((ix - 0x3ff00000) | lx) == 0)
				return y - y;
			else if (ix >= 0x3ff00000)
				return (hy >= 0) ? y : zero;
			else
				return (hy < 0) ? -y : zero;
		}
		if (iy == 0x3ff00000) {
			if (hy < 0)
				return one / x;
			else
				return x;
		}
		if (hy == 0x40000000)
			return x * x;
		if (hy == 0x3fe00000) {
			if (hx >= 0)
				return native_fn_020248a4(x);
		}
	}
	ax  = native_fn_02022664(x);
	if (lx == 0) {
		if (ix == 0x7ff00000 || ix == 0 || ix == 0x3ff00000) {
			z = ax;
			if (hy < 0)
				z = one / z;
			if (hx < 0) {
				if (((ix - 0x3ff00000) | yisint) == 0) {
					z = (z - z) / (z - z);
				} else if (yisint == 1)
					z = -z;
			}
			return z;
		}
	}
	if (((((int)hx >> 31) + 1) | yisint) == 0) {
		native_data_020ec9b0 = 33 ;
		return (double)native_data_020dcebc ;
	};
	if (iy > 0x41e00000) {
		if (iy > 0x43f00000) {
			if (ix <= 0x3fefffff)
				return (hy < 0) ? huge * huge : tiny * tiny;
			if (ix >= 0x3ff00000)
				return (hy > 0) ? huge * huge : tiny * tiny;
		}
		if (ix < 0x3fefffff)
			return (hy < 0) ? huge * huge : tiny * tiny;
		if (ix > 0x3ff00000)
			return (hy > 0) ? huge * huge : tiny * tiny;
		t        = x - 1;
		w        = (t * t) * (0.5 - t * (0.3333333333333333333333 - t * 0.25));
		u        = ivln2_h * t;
		v        = t * ivln2_l - w * ivln2;
		t1       = u + v;
		(((unsigned int *)&(t1))[0]) = 0;
		t2       = v - (t1 - u);
	} else {
		double s2, s_h, s_l, t_h, t_l;
		n = 0;
		if (ix < 0x00100000) {
			ax *= two53;
			n -= 53;
			ix = (((int *)&(ax))[1]) ;
		}
		n += ((ix) >> 20) - 0x3ff;
		j = ix & 0x000fffff;
		ix = j | 0x3ff00000;
		if (j <= 0x3988E)
			k = 0;
		else if (j < 0xBB67A)
			k = 1;
		else {
			k = 0;
			n += 1;
			ix -= 0x00100000;
		}
		(((int *)&(ax))[1]) = ix;
		u         = ax - native_data_020d9024[k];
		v         = one / (ax + native_data_020d9024[k]);
		s         = u * v;
		s_h       = s;
		(((unsigned int *)&(s_h))[0]) = 0;
		t_h       = zero;
		(((int *)&(t_h))[1]) = ((ix >> 1) | 0x20000000) + 0x00080000 + (k << 18);
		t_l       = ax - (t_h - native_data_020d9024[k]);
		s_l       = v * ((u - s_h * t_h) - s_h * t_l);
		s2 = s * s;
		r  = s2 * s2 * (L1 + s2 * (L2 + s2 * (L3 + s2 * (L4 + s2 * (L5 + s2 * L6)))));
		r += s_l * (s_h + s);
		s2        = s_h * s_h;
		t_h       = 3.0 + s2 + r;
		(((unsigned int *)&(t_h))[0]) = 0;
		t_l       = r - ((t_h - 3.0) - s2);
		u = s_h * t_h;
		v = s_l * t_h + t_l * s;
		p_h       = u + v;
		(((unsigned int *)&(p_h))[0]) = 0;
		p_l       = v - (p_h - u);
		z_h       = cp_h * p_h;
		z_l       = cp_l * p_h + p_l * cp + native_data_020d9034[k];
		t        = (double)n;
		t1       = (((z_h + z_l) + native_data_020d9014[k]) + t);
		(((unsigned int *)&(t1))[0]) = 0;
		t2       = z_l - (((t1 - t) - native_data_020d9014[k]) - z_h);
	}
	s = one;
	if (((((int)hx >> 31) + 1) | (yisint - 1)) == 0)
		s = -one;
	y1       = y;
	(((unsigned int *)&(y1))[0]) = 0;
	p_l      = (y - y1) * t1 + y * t2;
	p_h      = y1 * t1;
	z        = p_l + p_h;
	j        = (((int *)&(z))[1]) ;
	i        = (((unsigned int *)&(z))[0]) ;
	if (j >= 0x40900000) {
		if (((j - 0x40900000) | i) != 0)
			return s * huge * huge;
		else {
			if (p_l + ovt > z - p_h)
				return s * huge * huge;
		}
	} else if ((j & 0x7fffffff) >= 0x4090cc00) {
		if (((j - 0xc090cc00) | i) != 0)
			return s * tiny * tiny;
		else {
			if (p_l <= z - p_h)
				return s * tiny * tiny;
		}
	}
	i = j & 0x7fffffff;
	k = (i >> 20) - 0x3ff;
	n = 0;
	if (i > 0x3fe00000) {
		n       = j + (0x00100000 >> (k + 1));
		k       = ((n & 0x7fffffff) >> 20) - 0x3ff;
		t       = zero;
		(((int *)&(t))[1]) = (n & ~(0x000fffff >> k));
		n       = ((n & 0x000fffff) | 0x00100000) >> (20 - k);
		if (j < 0)
			n = -n;
		p_h -= t;
	}
	t       = p_l + p_h;
	(((unsigned int *)&(t))[0]) = 0;
	u       = t * lg2_h;
	v       = (p_l - (t - p_h)) * lg2 + t * lg2_l;
	z       = u + v;
	w       = v - (z - u);
	t       = z * z;
	t1      = z - t * (P1 + t * (P2 + t * (P3 + t * (P4 + t * P5))));
	r       = (z * t1) / (t1 - two) - (w + z * w);
	z       = one - (r - z);
	j       = (((int *)&(z))[1]) ;
	j += (n << 20);
	if ((j >> 20) <= 0)
		z = native_fn_02023ecc(z, n);
	else
		(((int *)&(z))[1]) += (n << 20);
	return s * z;
}
