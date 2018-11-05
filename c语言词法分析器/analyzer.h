#define BACK fseek(fp,-1L,1);token.pop_back();col--;
#define ZERO state = 0


int initialize(RESULT *output) {
	output->char_num = 0;
	output->line = 1;
	output->comment = 0;
} 

RESULT* analysis(FILE *fp, RESULT* output) {
	char cur_c = ' ';
	int state = 0;
	string token = "";
	initialize(output);
	int col = 0;
	int line = 1;
	
	
	while ((cur_c = nextChar(fp,&col)) && !feof(fp)) {
		int c_type = getCharacterType(cur_c);
		token += cur_c;
		col += 1;
		switch (state) {
			case 0: {
				token = "";
				token += cur_c;
				switch (c_type) {
					case Alphabet: state=1; break;
					case Underline: state = 1; break;
					case Digit: state = 2; break;
					case Border: addResult(output,"",cur_c,TOKENS,Border,line,col); break;
					case Operator: {
						switch (cur_c) {
							case '<': state = 8; break;
							case '>': state = 10; break;
							case '&': state = 12; break;
							case '+': state = 13; break;
							case '-': state = 14; break;
							case '*': state = 16; break;
							case '/': state = 17; break;
							case '^': state = 21; break;
							case '!': state = 22; break; 
							case '=': state = 23; break;
							case '|': state = 24; break;
							case '%': state = 25; break; 
							case ',':
							case '.':
							case '?':
							case ':':state = 0; addResult(output,"",cur_c,TOKENS,Operator,line,col); break;
						}
						break;
					}
					case Others: {
						switch (cur_c) {
							case '#': state = 15; break;
							case '\'': state = 26; break;
							case '\"': state = 27; break;
							case '\n': line++;col = 1; break;
							case ' ':
							case '\t': break;
							default: {
								addResult(output,"未知符号",cur_c,ERROR,0,line,col); 
								break;
							}
						}
						break;
					}
				}		
				break;
			}
			case 1: {
				switch (c_type) {
					case Alphabet:
					case Underline:
					case Digit: state = 1; break;
					default: {
						BACK; 
						ZERO; addResult(output,token,' ',TOKENS,ID,line,col);
						break;
					}
				}
				break;
			}
			case 2: {
				switch (c_type) {
					case Digit: state = 2; break;
					default: {
						if (cur_c == 'E' || cur_c == 'e')
							state = 5;
						else if (cur_c == '.')
							state = 3;
						else {
							BACK; 			
							ZERO; addResult(output,token,' ',TOKENS,Digit,line,col);
						}
						break;
					}
				}
				break;
			}
			case 3: {
				if (c_type != Digit) {
					BACK; 
					ZERO; addResult(output,"小数点后非法字符",cur_c,ERROR,' ',line,col);
				}
				else {
					state = 4;
				}
				break;
			}
			case 4: {
				if (c_type != Digit && cur_c != 'E' && cur_c != 'e') {
					BACK; 
					ZERO; addResult(output,token,' ',TOKENS,Digit,line,col);
				}
				else if (c_type == Digit)
					state = 4;
				else 
					state = 5;
				break;
			}
			case 5: {
				if (c_type == Digit) 
					state = 7;
				else if (cur_c == '+' || cur_c == '-')
					state = 6;
				else {
					BACK; 
					ZERO; addResult(output,"指数后非法符号",cur_c,ERROR,' ',line,col);
				}
				break;
			}
			case 6: {
				if (c_type == Digit) 
					state = 7;
				else {
					BACK; 
					ZERO; addResult(output,"尾数后非法符号",cur_c,ERROR,' ',line,col);
				}
				break;
			}
			case 7: {
				if (c_type == Digit) 
					state = 7;
				else {
					BACK; 
					ZERO; addResult(output,token,' ',TOKENS,Digit,line,col);
				}
				break;
			}
			case 8: {
				if (cur_c == '=') {
					ZERO;
					addResult(output,token,' ',TOKENS,Operator,line,col);
				}
				else if (cur_c == '<')
					state = 9;
				else {
					BACK; ZERO;
					addResult(output,token,' ',TOKENS,Operator,line,col);
				}
				break;
			}
			case 10: {
				if (cur_c == '=') {
					ZERO;
					addResult(output,token,' ',TOKENS,Operator,line,col);
				}
				else if (cur_c == '>')
					state = 11;
				else {
					BACK; ZERO;
					addResult(output,token,' ',TOKENS,Operator,line,col);
				}
				break;
				break;
			}
			case 9:
			case 11: {
				if (cur_c != '=') BACK;
				ZERO; addResult(output,token,' ',TOKENS,Operator,line,col);
				break;
			}
			case 12: {
				if (cur_c == '&' || cur_c == '=') {
					ZERO;
					addResult(output,token,' ',TOKENS,Operator,line,col);
				}
				else {
					BACK; ZERO;
					addResult(output,token,' ',TOKENS,Operator,line,col);
				}
				break;
			}
			case 24: {
				if (cur_c == '|' || cur_c == '=') {
					ZERO;
					addResult(output,token,' ',TOKENS,Operator,line,col);
				}
				else {
					BACK; ZERO;
					addResult(output,token,' ',TOKENS,Operator,line,col);
				}
				break;
				break;
			}
			case 13: {
				if (cur_c == '+' || cur_c == '=') {
					ZERO;
					addResult(output,token,' ',TOKENS,Operator,line,col);
				}
				else {
					BACK; ZERO;
					addResult(output,token,' ',TOKENS,Operator,line,col);
				}
				break;
			}
			case 14: {
				if (cur_c == '-' || cur_c == '=' || cur_c == '>') {
					ZERO;
					addResult(output,token,' ',TOKENS,Operator,line,col);
				}
				else {
					BACK; ZERO;
					addResult(output,token,' ',TOKENS,Operator,line,col);
				}
				break;
			}
			case 15: {
				while (cur_c != '\n' && !feof(fp)) {
					cur_c = nextChar(fp,&col); 
					token += cur_c;
				}
				BACK; ZERO;
				addResult(output,token,' ',TOKENS,Macro,line,col);
				break;
			}
			case 16: 
			case 21:
			case 22:
			case 25:
			case 23: {
				if (cur_c != '=') BACK;
				ZERO;
				addResult(output,token,' ',TOKENS,Operator,line,col);
				break;
			}
			case 17: {
				if (cur_c == '*') state = 18,output->comment += 2;
				else if (cur_c == '/') state = 20,output->comment += 2;
				else if (cur_c == '=') {
					ZERO;
					addResult(output,token,' ',TOKENS,Operator,line,col);
				}
				else {
					BACK;
					ZERO;
					addResult(output,token,' ',TOKENS,Operator,line,col);
				}
				break;
			}
			case 18: {
				if (cur_c != ' ' && cur_c != '\t' && cur_c != '\n' && cur_c != '\r') output->comment++;
				if (cur_c == '\n') line++;
				if (cur_c == '*') state = 19;
				break;
			}
			case 19: {
				if (cur_c != ' ' && cur_c != '\t' && cur_c != '\n' && cur_c != '\r') output->comment++;
				if (cur_c == '\n') line++;
				if (cur_c == '/') ZERO;
				else state = 18;
				break;
			}
			case 20: {
				if (cur_c != ' ' && cur_c != '\t' && cur_c != '\n' && cur_c != '\r') output->comment++;
				if (cur_c == '\n')  {
					BACK;
					ZERO;
				}
				break;
			}
			case 26: {
				if (cur_c == '\\') state = 28;
				else if (cur_c == '\'') {
					ZERO;
					addResult(output,token,' ',TOKENS,String,line,col);
				}
				break;
			}
			case 27: {
				if (cur_c == '\\') state = 29;
				else if (cur_c == '\"') {
					ZERO;
					addResult(output,token,' ',TOKENS,String,line,col);
				}
				break;
			}
			case 28: {
				state = 26;
				break;
			}
			case 29: {
				state = 27;
				break;
			}
		}
	}
	return output;
}
