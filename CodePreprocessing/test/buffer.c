#include <stdio.h>

int main(){
	int buffer[2];
	int a, b, c, d, cur = 0, carry = 0;
	a = 7l / 10;
	b = 71 % 10;
	c = 43 / 10;
	d = 43 % 10;
	int sum = b + d + carry;
	buffer[cur++] = sum % 10;
	carry = sum / 10;
	sum = a + c + carry;
	buffer[cur++] = sum % 10;
	carry = sum / 10;
	if(carry > 0)
		buffer[cur++] = carry;
	return 0;
}
