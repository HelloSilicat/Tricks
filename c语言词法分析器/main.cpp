#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <vector>
#include "utils.h"
#include "analyzer.h"
#include <iostream>
using namespace std;

int main(void)
{
	string filename = "program.txt";
	RESULT* output = (RESULT *)malloc(sizeof(RESULT)); // contain result&error
	FILE *fp = fopen(filename.c_str(),"r");
	
	printf("´Ê·¨·ÖÎöÖÐ......\n");
	analysis(fp,output);
	showTokenInfo(output->tokens,output->line,output->char_num,output->comment);
	getchar(); 
	return 0;
}
