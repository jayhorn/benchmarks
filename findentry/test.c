extern int __VERIFIER_nondet_int();

extern void __VERIFIER_error();
void assert (int v) {
	if (!v) __VERIFIER_error();
}

int equals(int m) {
	for (int i = 0; i < m - 1; i++) {
		if (__VERIFIER_nondet_int()) {
			return 0;
		}
	}
	return 1;
}

int main() {
	int n = __VERIFIER_nondet_int();
	int m = __VERIFIER_nondet_int();
	assume(n > 0); assume (m > 0);
	int r = n*m;
	for (int i = 0; i < n; i++) {
		
		r = r - 1;
		assert(r >= 0);
		
		if (equals(m) == 1) {
			return 0;
		}
	}
	return 0;
}
