import	gtk

__keys = {
	gtk.keysyms.a : 'A',
	gtk.keysyms.A : 'A',
	gtk.keysyms.b : 'B',
	gtk.keysyms.B : 'B',
	gtk.keysyms.c : 'C',
	gtk.keysyms.C : 'C',
	gtk.keysyms.d : 'D',
	gtk.keysyms.D : 'D',
	gtk.keysyms.e : 'E',
	gtk.keysyms.E : 'E',
	gtk.keysyms.f : 'F',
	gtk.keysyms.F : 'F',
	gtk.keysyms.g : 'G',
	gtk.keysyms.G : 'G',
	gtk.keysyms.h : 'H',
	gtk.keysyms.H : 'H',
	gtk.keysyms.i : 'I',
	gtk.keysyms.I : 'I',
	gtk.keysyms.j : 'J',
	gtk.keysyms.J : 'J',
	gtk.keysyms.k : 'K',
	gtk.keysyms.K : 'K',
	gtk.keysyms.l : 'L',
	gtk.keysyms.L : 'L',
	gtk.keysyms.m : 'M',
	gtk.keysyms.M : 'M',
	gtk.keysyms.n : 'N',
	gtk.keysyms.N : 'N',
	gtk.keysyms.o : 'O',
	gtk.keysyms.O : 'O',
	gtk.keysyms.p : 'P',
	gtk.keysyms.P : 'P',
	gtk.keysyms.q : 'Q',
	gtk.keysyms.Q : 'Q',
	gtk.keysyms.r : 'R',
	gtk.keysyms.R : 'R',
	gtk.keysyms.s : 'S',
	gtk.keysyms.S : 'S',
	gtk.keysyms.t : 'T',
	gtk.keysyms.T : 'T',
	gtk.keysyms.u : 'U',
	gtk.keysyms.U : 'U',
	gtk.keysyms.v : 'V',
	gtk.keysyms.V : 'V',
	gtk.keysyms.w : 'W',
	gtk.keysyms.W : 'W',
	gtk.keysyms.x : 'X',
	gtk.keysyms.X : 'X',
	gtk.keysyms.y : 'Y',
	gtk.keysyms.Y : 'Y',
	gtk.keysyms.z : 'Z',
	gtk.keysyms.Z : 'Z',

}


def get_key_name(keycode):
	if keycode in __keys:
		return __keys[keycode]
	
	return ''


def is_cancel_key(key):
	return key == gtk.keysyms.Escape

